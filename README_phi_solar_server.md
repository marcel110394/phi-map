
φ-SolarServer – Raumzeitresonanz & Sonnenwinddaten

Willkommen beim φ-SolarServer!  
Dieses Projekt verbindet Echtzeit-Raumzeitresonanzdaten (φ(t, r)) mit aktuellen Sonnenwetterdaten – lokal oder weltweit nutzbar.

🔧 Funktionen

- Flask-Server zur Bereitstellung von:
 - φ(t, r)-Werten (aus ESP32 oder Simulation)
 - Sonnenwinddaten (live z. B. von NOAA)
 - JSON-Ausgabe zur Integration in Frontends (z. B. φ-Weltkarte)
 - Einfache Erweiterbarkeit für:
 - Trigger-Logik
 - Telegram-Benachrichtigungen
 - Weltkarten-Visualisierung

---

## 📂 Projektstruktur

```
phi-solar-server/
├── app.py                  # Haupt-Flask-Server
├── update_solar_data.py    # Holt Sonnenwinddaten (NOAA)
├── phi_daten_log.json      # φ(t, r)-Wert (live)
├── sonnenwind.json         # Sonnenaktivitätsdaten
├── requirements.txt        # benötigte Python-Pakete
└── README.md               # diese Anleitung
```

🚀 Schnellstart

1. 🔧 Python-Umgebung vorbereiten:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. ▶ Flask-Server starten:
```bash
python app.py
```

3. 🌞 Sonnenwinddaten manuell updaten:
```bash
python update_solar_data.py
```

Oder: Automatisch per Cronjob oder Hintergrundprozess.

 📡 JSON-Ausgaben

| Endpoint         | Inhalt |
|------------------|--------|
| `/phi`           | φ(t, r)-Daten |
| `/sun`           | Sonnenwinddaten |
| `/status`        | Systemstatus |



📌 Hinweis

- Dieses Projekt dient der Demonstration realer φ(t, r)-Messung und der Korrelation mit kosmischem Einfluss.
- Kann jederzeit mit echten Sensoren, GPS, GSR, Magnetfeld oder weiteren kosmischen Quellen erweitert werden.



Entwickelt von M. Aichmayr 2025  
Die Singularität ist nicht gekommen. Sie wurde entfernt._
