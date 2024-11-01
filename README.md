Chicken.gg Wager Tracker

This project tracks and displays the top wagers on Chicken.gg for a specific timeframe. The Python script uses Flask to host a simple web server and pull live wager data from the Chicken.gg API every 2 minutes. It updates a JSON cache, which is displayed on a webpage with a podium layout for the top three wagerers and standings for the top 11.
Key Features

    Flask Server: Hosts a webpage showing live wager standings.
    API Integration: Fetches wager data from Chicken.gg’s API, showing real-time rankings.
    Dynamic Standings: JavaScript dynamically updates the standings without needing a page refresh.

Dependencies

    Python 3.8+
    Flask: For hosting the web server
    Flask-CORS: To handle cross-origin requests
    Requests: For making HTTP requests to the Chicken.gg API

Installation Instructions

    Clone the Repository:

    bash

git clone <repository_url>
cd <repository_folder>

Install Dependencies:

bash

pip install -r requirements.txt

Run the Application:

bash

    python chknrace.py

This will start the Flask server on port 8080, and you can view the wager standings by navigating to http://localhost:8080 in your browser.
