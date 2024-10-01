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

# Define min_time and end_time in milliseconds
min_time = 1727628116000  # Set to your specified start time
end_time = 1728583200000  # Set to your specified end time

# Data cache for storing fetched data
data_cache = {}

# Function to log detailed output
def log_message(level, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level.upper()}]: {message}")

# Function to fetch data from Chicken.gg API
def fetch_data():
    global data_cache
    try:
        log_message('info', 'Starting data fetch from Chicken.gg API')

        # Format the API URL with dynamic time parameters
        url = url_template.format(min_time=min_time, max_time=end_time)

        # Fetch the data from Chicken.gg API
        response = requests.get(url)

        if response.status_code == 200:
            # Parse the API response
            api_response = response.json()
            log_message('info', f"Raw API response: {json.dumps(api_response)}")

            if 'referrals' in api_response and isinstance(api_response['referrals'], list) and len(api_response['referrals']) > 0:
                data_cache = api_response['referrals']  # Cache the API data from 'referrals'
                log_message('info', 'Data successfully fetched and cached.')
                update_placeholder_data()  # Process the data and update placeholders
            else:
                log_message('warning', 'No valid data found in the API response.')
                data_cache = {"error": "No data found in API response."}
        else:
            log_message('error', f"Failed to fetch data. Status code: {response.status_code}")
            data_cache = {"error": f"Failed to fetch data. Status code: {response.status_code}"}
    except Exception as e:
        log_message('error', f"Exception occurred during data fetch: {e}")
        data_cache = {"error": str(e)}

# Function to update the placeholder data with real API data
def update_placeholder_data():
    global data_cache
    try:
        # Assuming the API response data structure includes displayName and wagerAmount fields
        if isinstance(data_cache, list):
            # Sort the data by wagerAmount in descending order
            sorted_data = sorted(data_cache, key=lambda x: x['wagerAmount'], reverse=True)

            # Replace placeholder data with the top wagerers
            top_wagerers = {}
            for i in range(min(11, len(sorted_data))):  # Get up to the top 11 players
                top_wagerers[f'top{i+1}'] = {
                    'username': sorted_data[i]['displayName'],  # Fetch the displayName field
                    'wager': f"${sorted_data[i]['wagerAmount']:,}"  # Format wagerAmount with commas
                }

            # Update the global data_cache with the top wagerers
            data_cache = top_wagerers
            log_message('info', f"Top wagerers data updated: {top_wagerers}")
        else:
            log_message('warning', 'No valid data structure found in the API response.')
    except KeyError as e:
        log_message('error', f"KeyError during data update: {e}")
    except Exception as e:
        log_message('error', f"An error occurred while updating placeholder data: {e}")

# Schedule data fetching every 5 minutes (300 seconds)
def schedule_data_fetch():
    log_message('info', 'Scheduling the next data fetch in 5 minutes.')
    fetch_data()  # Fetch data immediately when the script starts
    threading.Timer(300, schedule_data_fetch).start()  # Schedule the next fetch in 5 minutes

# Flask route to serve the cached data
@app.route("/data")
def get_data():
    log_message('info', 'Serving cached data to a client')
    return jsonify(data_cache)

# Route to serve the HTML file
@app.route("/")
def serve_index():
    log_message('info', 'Serving index.html')
    return send_from_directory(os.getcwd(), 'index.html')

# Start the data fetching thread
schedule_data_fetch()

# Run the Flask app on port 8080 (use environment variable for the port)
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8080))  # Default to port 8080
    log_message('info', f"Starting Flask app on port {port}")
    app.run(host="0.0.0.0", port=port)
