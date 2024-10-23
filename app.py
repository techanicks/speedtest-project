from flask import Flask, jsonify, render_template, send_file
import speedtest
import csv
import os
from datetime import datetime

app = Flask(__name__)

# Function to perform speed test
def perform_speed_test():
    st = speedtest.Speedtest()
    st.get_best_server()
    download_speed = st.download() / 1_000_000  # Convert from bits to Mbps
    upload_speed = st.upload() / 1_000_000  # Convert from bits to Mbps
    ping = st.results.ping
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    return download_speed, upload_speed, ping, timestamp

# Route to run the speed test and save results
@app.route('/run_test', methods=['GET'])
def run_test():
    download_speed, upload_speed, ping, timestamp = perform_speed_test()

    # Create or append results to CSV file
    file_exists = os.path.isfile('speedtest_results.csv')
    with open('speedtest_results.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Download Speed (Mbps)', 'Upload Speed (Mbps)', 'Ping (ms)', 'Timestamp'])
        writer.writerow([download_speed, upload_speed, ping, timestamp])

    return jsonify({
        'download_speed': round(download_speed, 2),
        'upload_speed': round(upload_speed, 2),
        'ping': ping,
        'timestamp': timestamp
    })

# Route to download the CSV file
@app.route('/download_csv', methods=['GET'])
def download_csv():
    return send_file('speedtest_results.csv', as_attachment=True)

# Route for the homepage (where the test will be run)
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)


