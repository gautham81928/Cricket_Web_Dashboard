# Cricket_Web_Dashboard

This is a web dashboard where you can view live scores of all types of cricket matches such as T20, ODI, and Tests. This web application was built using Python, with the Flask framework, and Tailwind CSS. The data is collected from CricAPI, and is stored locally in an SQLite database. To conserve the daily API rate limit, a caching layer has been implemented so when the website is refreshed, the response time is instant. With this, the external API consumption has been reduced by over 90%.

Tech Stack:
- Backend: Python, Flask
- Caching and local storage: SQLite3
- HTTP and API integration: Requests, Python-Dotenv, CricAPI
- Frontend: HTML, JavaScript, Tailwind CSS

How to Use:
# 1. Setup Virtual Environment:
- macOS/Linux:

python3 -m venv venv
source venv/bin/activate

- Windows:

python -m venv venv
venv\Scripts\activate

# 2. Install Dependencies:
pip install flask 
pip install requests 
pip install python-dotenv

# 3. Open the .env file and replace "your_actual_api_key_here" with your API key
CRICAPI_KEY=your_actual_api_key_here

# 4. Run client.py to make sure the matches and their scores are showing up in the CLI
python client.py

# 5. Run app.py to view the data in a web interface.
python app.py

# 6. Open your web browser and copy paste the local host web url:
http://127.0.0.1:5000

