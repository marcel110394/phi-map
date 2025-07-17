from flask import Flask, jsonify
import requests
import pandas as pd
import threading
import time
import os

app = Flask(__name__)
CSV_FILE = "phi_sonnenwind.csv"
FETCH_INTERVAL = 600  # alle 10 Minuten

def fetch_and_store_sonnenwind():
    while True:
        try:
            url = "https://services.swpc.noaa.gov/text/ace-swepam.txt"
            response = requests.get(url, timeout=10)
            lines = response.text.strip().split("\n")
            data_lines = [line for line in lines if line[:4].isdigit()]
            parsed_data = [line.split()[:9] for line in data_lines]

            columns = ["YR", "MO", "DA", "HHMM", "DOY", "Seconds", "Density", "Speed", "Temperature"]
            df = pd.DataFrame(parsed_data, columns=columns)
            df["Density"] = pd.to_numeric(df["Density"], errors="coerce")
            df["Speed"] = pd.to_numeric(df["Speed"], errors="coerce")
            df["Temperature"] = pd.to_numeric(df["Temperature"], errors="coerce")

            df.to_csv(CSV_FILE, index=False)
            print("[φ] Sonnenwind-Daten aktualisiert.")

        except Exception as e:
            print(f"[!] Fehler beim Abrufen der Sonnenwinddaten: {e}")

        time.sleep(FETCH_INTERVAL)

@app.route("/sonnenwind", methods=["GET"])
def serve_sonnenwind():
    if not os.path.exists(CSV_FILE):
        return jsonify({"error": "Noch keine Daten verfügbar."}), 404

    try:
        df = pd.read_csv(CSV_FILE)
        last10 = df.tail(10)
        result = {
            "mean_density": round(last10["Density"].mean(), 2),
            "mean_speed": round(last10["Speed"].mean(), 2),
            "mean_temp": round(last10["Temperature"].mean(), 2)
        }
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    threading.Thread(target=fetch_and_store_sonnenwind, daemon=True).start()
    app.run(host="0.0.0.0", port=5000)