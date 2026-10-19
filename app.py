from flask import Flask, render_template, jsonify
from cache import init_cache_db, get_cached_response, set_cached_response
from client import get_current_matches

app = Flask(__name__)
CACHE_TTL = 180  # 3 minutes

init_cache_db()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/matches", methods=["GET"])
def api_matches():
    cache_key = "current_matches"

    # 1. Attempt retrieval from cache
    cached = get_cached_response(cache_key, ttl_seconds=CACHE_TTL)
    if cached:
        return jsonify(cached)

    # 2. Cache Miss: Fetch using the shared API client module
    try:
        matches = get_current_matches()
        set_cached_response(cache_key, matches)

        return jsonify({
            "source": "CACHE_MISS",
            "ttl_remaining_seconds": CACHE_TTL,
            "data": matches
        })

    except Exception as err:
        return jsonify({"error": str(err)}), 502


if __name__ == "__main__":
    app.run(debug=True, port=5000)