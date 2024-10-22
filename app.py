import speedtest
import csv
import os
from flask import Flask, jsonify, render_template
import datetime

app = Flask(__name__)

# CSV file to store speed test results
csv_file = "speedtest_results.csv"

# Check if the CSV file exists; if not, create it with headers
if not os.path.exists(csv_file):
    print(f"CSV file '{csv_file}' does not exist. Creating file...")
    try:
        with open(csv_file, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Time", "Download Speed (Mbps)", "Upload Speed (Mbps)", "Ping (ms)"])
        print(f"CSV file '{csv_file}' created successfully.")
    except Exception as e:
        print(f"Error creating CSV file: {e}")
else:
    print(f"CSV file '{csv_file}' already exists.")

# Function to run the speed test and save results
def run_speedtest():
    try:
        print("Running speed test...")
        st = speedtest.Speedtest()
        st.get_best_server()
        download_speed = round(st.download() / 1_000_000, 2)  # Convert to Mbps
        upload_speed = round(st.upload() / 1_000_000, 2)  # Convert to Mbps
        ping = round(st.results.ping, 2)  # Ping in ms

        # Get current date and time
        now = datetime.datetime.now()
        date = now.strftime("%Y-%m-%d")
        time = now.strftime("%H:%M:%S")

        # Append result to CSV file
        print(f"Saving results to '{csv_file}'...")
        with open(csv_file, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, time, download_speed, upload_speed, ping])
        print("Results saved successfully.")

        return {
            "download_speed": download_speed,
            "upload_speed": upload_speed,
            "ping": ping,
            "date": date,
            "time": time
        }
    except Exception as e:
        print(f"Error running speed test or saving results: {e}")
        return {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_test', methods=['GET'])
def run_test():
    result = run_speedtest()
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
