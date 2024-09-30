import requests
import time
import json
from flask import Flask, jsonify, send_from_directory
from datetime import datetime
import os
import threading
from flask_cors import CORS

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Chicken.gg API key (hardcoded into the script)
api_key = "316a2f45bff17a887b8a37748e61ac06"

# Base URL for Chicken.gg API
url_template = f"https://affiliates.chicken.gg/v1/referrals?key={api_key}&minTime={{min_time}}&maxTime={{max_time}}"

# Define current and end time in milliseconds
min_time = int(datetime.now().timestamp() * 1000)  # Start from now
end_time = int(datetime(2024, 10, 8).timestamp() * 1000)  # End on October 8, 2024 in milliseconds

# Data cache for storing fetched data
data_cache = {}

# Function to fetch data from Chicken.gg API
def fetch_data():
    global data_cache
    try:
        # Get current time in milliseconds
        max_time = int(time.time() * 1000) - 60000  # Subtract 1 minute

        # Ensure we don't go past the end date
        if max_time > end_time:
            max_time = end_time

        # Format the API URL with dynamic time parameters
        url = url_template.format(min_time=min_time, max_time=max_time)

        # Fetch the data from Chicken.gg API
        response = requests.get(url)

        if response.status_code == 200:
            # Cache the API response if successful
            data_cache = response.json()
            print("Data fetched:", data_cache)  # Debugging: print the fetched data
        else:
            # Cache an error message if the API call fails
            data_cache = {"error": f"Failed to fetch data. Status code: {response.status_code}"}
            print("API Error:", data_cache)  # Debugging: print API error message
    except Exception as e:
        # Cache any exception as an error
        data_cache = {"error": str(e)}
        print("Error fetching data:", e)  # Debugging: print any exceptions

# Schedule data fetching every 5 minutes (300 seconds)
def schedule_data_fetch():
    fetch_data()  # Fetch data immediately when the script starts
    threading.Timer(300, schedule_data_fetch).start()  # Schedule the next fetch in 5 minutes

# Flask route to serve the cached data
@app.route("/data")
def get_data():
    return jsonify(data_cache)

# Route to serve the HTML file
@app.route("/")
def serve_index():
    return send_from_directory(os.getcwd(), 'index.html')

# Start the data fetching thread
schedule_data_fetch()

# Run the Flask app on port 8080 (use environment variable for the port)
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))  # Default to port 8080
    app.run(host="0.0.0.0", port=port)
