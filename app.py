from flask import Flask, render_template, send_file, request, jsonify
import speedtest
import csv
import os
from datetime import datetime

app = Flask(__name__)

# Define the CSV file path
CSV_FILE = os.path.join(os.path.dirname(__file__), 'speed_test_results.csv')

# Function to perform speed test
def perform_speed_test():
    try:
        st = speedtest.Speedtest()
        best_server = st.get_best_server()
        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000      # Convert to Mbps
        ping = best_server['latency']
        return download_speed, upload_speed, ping, best_server['sponsor']
    except Exception as e:
        print(f"Error during speed test: {e}")
        return 0, 0, 0, "Error"
        
# Function to save results to CSV
def save_to_csv(download, upload, ping, server):
    header = ['Timestamp', 'Download Speed (Mbps)', 'Upload Speed (Mbps)', 'Ping (ms)', 'Server']
    data = [datetime.now().strftime('%Y-%m-%d %H:%M:%S'), download, upload, ping, server]

    # Check if the CSV file exists
    file_exists = os.path.isfile(CSV_FILE)

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)

    # Open the file in append mode
    with open(CSV_FILE, mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(header)  # Write header if the file is new
        writer.writerow(data)      # Append the new data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/speedtest', methods=['POST'])
def speedtest_route():
    download, upload, ping, server = perform_speed_test()
    save_to_csv(download, upload, ping, server)
    return jsonify({
        'download': download,
        'upload': upload,
        'ping': ping,
        'server': server
    })

@app.route('/download')
def download_file():
    if os.path.exists(CSV_FILE):
        return send_file(CSV_FILE, as_attachment=True)
    else:
        return "CSV file not found.", 404

if __name__ == '__main__':
    app.run(debug=True)

















