from flask import Flask, request, jsonify, send_from_directory
import json, os, requests
import pandas as pd
from datetime import datetime

app = Flask(__name__)
LOG_FILE = "phi_daten_log.json"
SOLAR_FILE = "phi_sonnenwind.csv"

@app.route('/phi_receiver', methods=['POST'])
def receive_phi_data():
    try:
        data = request.get_json()
        data["timestamp"] = datetime.utcnow().isoformat() + "Z"

        # Solarwerte einfügen:
        if os.path.exists(SOLAR_FILE):
            df = pd.read_csv(SOLAR_FILE)
            latest = df.tail(1)
            data["solar_density"] = float(latest["Density"].values[0])
            data["solar_speed"] = float(latest["Speed"].values[0])
            data["solar_temp"] = float(latest["Temperature"].values[0])

        if not os.path.exists(LOG_FILE):
            with open(LOG_FILE, "w") as f:
                json.dump([data], f, indent=2)
        else:
            with open(LOG_FILE, "r+") as f:
                try:
                    existing = json.load(f)
                except json.JSONDecodeError:
                    existing = []
                existing.append(data)
                f.seek(0)
                json.dump(existing, f, indent=2)
                f.truncate()

        return jsonify({"status": "success", "received": data}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/phi_gama_heatmap.html')
def serve_heatmap():
    return send_from_directory('.', 'phi_gama_heatmap.html')

@app.route('/phi_daten_log.json')
def serve_data():
    return send_from_directory('.', 'phi_daten_log.json')

@app.route('/phi_sonnenwind.csv')
def serve_solar():
    return send_from_directory('.', 'phi_sonnenwind.csv')

@app.route('/update_solar', methods=['GET'])
def update_solar_data():
    try:
        url = "https://services.swpc.noaa.gov/text/ace-swepam.txt"
        response = requests.get(url, timeout=10)
        lines = response.text.strip().split("\n")
        data_lines = [line for line in lines if line[:4].isdigit()]
        columns = ["YR", "MO", "DA", "HHMM", "DOY", "Seconds", "Density", "Speed", "Temperature"]
        parsed_data = [line.split()[:9] for line in data_lines]
        df = pd.DataFrame(parsed_data, columns=columns)
        df["Density"] = pd.to_numeric(df["Density"], errors="coerce")
        df["Speed"] = pd.to_numeric(df["Speed"], errors="coerce")
        df["Temperature"] = pd.to_numeric(df["Temperature"], errors="coerce")
        df.to_csv(SOLAR_FILE, index=False)
        return jsonify({"status": "solar data updated", "rows": len(df)}), 200
    except Exception as e:
        return jsonify({"status": "solar update failed", "error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

