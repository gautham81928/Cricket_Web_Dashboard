import sqlite3
import json
import time

DB_PATH = "cricket_cache.db"


def init_cache_db():
    """Create the cache table if it does not exist."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS api_cache (
                endpoint_key TEXT PRIMARY KEY,
                response_data TEXT NOT NULL,
                cached_at REAL NOT NULL
            )
        """)
        conn.commit()


def get_cached_response(endpoint_key: str, ttl_seconds: int = 180):
    """
    Retrieve cached JSON data if it exists and hasn't expired.
    Returns: dict on hit, None on miss or expired TTL.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT response_data, cached_at FROM api_cache WHERE endpoint_key = ?",
            (endpoint_key,)
        )
        row = cursor.fetchone()

        if not row:
            return None  # Cache miss

        response_data, cached_at = row
        current_time = time.time()
        age = current_time - cached_at

        if age > ttl_seconds:
            return None  # Expired TTL

        ttl_remaining = max(0, int(ttl_seconds - age))
        return {
            "source": "CACHE_HIT",
            "ttl_remaining_seconds": ttl_remaining,
            "data": json.loads(response_data)
        }


def set_cached_response(endpoint_key: str, data):
    """Insert or update cached JSON payload with current timestamp."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO api_cache (endpoint_key, response_data, cached_at)
            VALUES (?, ?, ?)
            ON CONFLICT(endpoint_key) DO UPDATE SET
                response_data = excluded.response_data,
                cached_at = excluded.cached_at
        """, (endpoint_key, json.dumps(data), time.time()))
        conn.commit()