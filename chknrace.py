import requests
import time
import json
from flask import Flask, jsonify, send_from_directory
from datetime import datetime
import os
import threading
from flask_cors import CORS  # For handling CORS issues

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS to allow cross-origin requests

# Chicken.gg API key and base URL (Replace with the correct API key)
api_key = os.getenv("API_KEY", "default_key")  # Use environment variable for the API key
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
        max_time = int(time.time() * 1000) - 60000  # Subtract 1 minute

        if max_time > end_time:
            max_time = end_time

        url = url_template.format(min_time=min_time, max_time=max_time)
        response = requests.get(url)

        if response.status_code == 200:
            data_cache = response.json()  # Cache the API response
            print("Data fetched:", data_cache)  # Debugging: print the fetched data
        else:
            data_cache = {"error": f"Failed to fetch data. Status code: {response.status_code}"}
            print("API Error:", data_cache)  # Debugging: print API error message
    except Exception as e:
        data_cache = {"error": str(e)}
        print("Error fetching data:", e)  # Debugging: print any exceptions

# Schedule data fetching every 15 minutes (900 seconds)
def schedule_data_fetch():
    fetch_data()  # Fetch data immediately when the script starts
    threading.Timer(900, schedule_data_fetch).start()  # Schedule the next fetch in 15 minutes

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
