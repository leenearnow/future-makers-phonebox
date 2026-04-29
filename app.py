{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww16940\viewh11060\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import json\
import sqlite3\
import time\
import threading\
from datetime import datetime\
from flask import Flask, render_template, jsonify, Response\
\
# Load config\
with open("config.json") as f:\
    config = json.load(f)\
\
app = Flask(__name__)\
\
# \uc0\u9472 \u9472  Database setup \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
DB_PATH = "deposits.db"\
\
def init_db():\
    with sqlite3.connect(DB_PATH) as conn:\
        conn.execute("""\
            CREATE TABLE IF NOT EXISTS deposits (\
                id        INTEGER PRIMARY KEY AUTOINCREMENT,\
                timestamp TEXT NOT NULL\
            )\
        """)\
\
def record_deposit():\
    with sqlite3.connect(DB_PATH) as conn:\
        conn.execute("INSERT INTO deposits (timestamp) VALUES (?)",\
                     (datetime.now().isoformat(),))\
\
def get_total():\
    with sqlite3.connect(DB_PATH) as conn:\
        row = conn.execute("SELECT COUNT(*) FROM deposits").fetchone()\
        return row[0]\
\
def get_recent(limit=10):\
    with sqlite3.connect(DB_PATH) as conn:\
        rows = conn.execute(\
            "SELECT timestamp FROM deposits ORDER BY id DESC LIMIT ?", (limit,)\
        ).fetchall()\
        return [r[0] for r in rows]\
\
# \uc0\u9472 \u9472  Server-Sent Events (real-time push) \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
event_subscribers = []\
event_lock = threading.Lock()\
\
def push_event(data: dict):\
    """Broadcast a JSON event to all connected dashboards."""\
    msg = f"data: \{json.dumps(data)\}\\n\\n"\
    with event_lock:\
        for queue in event_subscribers:\
            queue.append(msg)\
\
@app.route("/stream")\
def stream():\
    def generate():\
        q = []\
        with event_lock:\
            event_subscribers.append(q)\
        try:\
            while True:\
                if q:\
                    yield q.pop(0)\
                else:\
                    yield ": keep-alive\\n\\n"   # prevents timeout\
                time.sleep(0.5)\
        finally:\
            with event_lock:\
                event_subscribers.remove(q)\
    return Response(generate(), mimetype="text/event-stream",\
                    headers=\{"Cache-Control": "no-cache",\
                             "X-Accel-Buffering": "no"\})\
\
# \uc0\u9472 \u9472  Routes \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
@app.route("/")\
def dashboard():\
    return render_template("dashboard.html",\
                           config=config,\
                           total=get_total(),\
                           recent=get_recent())\
\
@app.route("/api/status")\
def api_status():\
    """Polled by the GitHub Pages dashboard."""\
    return jsonify(\{\
        "total": get_total(),\
        "recent": get_recent(5),\
        "installation_name": config["installation_name"]\
    \})\
\
@app.route("/api/trigger", methods=["POST"])\
def api_trigger():\
    """Called by sensor.py (or simulate_drop.py for testing)."""\
    record_deposit()\
    total = get_total()\
    push_event(\{"type": "deposit", "total": total,\
                "timestamp": datetime.now().isoformat()\})\
    return jsonify(\{"ok": True, "total": total\})\
\
# \uc0\u9472 \u9472  Start \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \u9472 \
if __name__ == "__main__":\
    init_db()\
    # Import sensor only on real Pi hardware\
    try:\
        import sensor\
        sensor.start(on_drop=lambda: app.test_client().post("/api/trigger"))\
    except (ImportError, RuntimeError):\
        print("No GPIO hardware found \'97 running in software-only mode.")\
    app.run(host="0.0.0.0", port=5000, threaded=True)}