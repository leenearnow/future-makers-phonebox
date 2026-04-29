# future-makers-phonebox
A phone recycling point by Future Makers

Project file structure
recycling-box/
├── app.py               # Flask server + sensor logic
├── sensor.py            # GPIO reading (runs as a background thread)
├── config.json          # ← Edit your messages here
├── deposits.db          # SQLite database (auto-created)
├── templates/
│   └── dashboard.html   # Local kiosk display
├── static/
│   └── style.css
├── simulate_drop.py     # Testing tool (no hardware needed)
└── github-pages/
    └── index.html       # Online public dashboard
