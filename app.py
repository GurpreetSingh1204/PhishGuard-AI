"""
Flask web app + REST API.

    python app.py         -> open http://127.0.0.1:5000

API:
    POST /api/scan/url    {"url": "...", "use_llm": true}
    POST /api/scan/email  {"text": "...", "use_llm": true}
    GET  /api/metrics
    GET  /api/history
"""
import json
import os
import sqlite3
import sys
from datetime import datetime

from flask import Flask, jsonify, render_template, request

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))
from detector import PhishingDetector  # noqa: E402

app = Flask(__name__)
detector = PhishingDetector()
DB = os.path.join(ROOT, "scan_history.db")


def db():
    con = sqlite3.connect(DB)
    con.execute("""CREATE TABLE IF NOT EXISTS scans(
        id INTEGER PRIMARY KEY AUTOINCREMENT, ts TEXT, type TEXT,
        input TEXT, verdict TEXT, score REAL)""")
    return con


def log_scan(result, raw):
    with db() as con:
        con.execute("INSERT INTO scans(ts,type,input,verdict,score) VALUES(?,?,?,?,?)",
                    (datetime.now().isoformat(timespec="seconds"), result["type"],
                     raw[:300], result["verdict"], result["score"]))


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/api/scan/url")
def scan_url():
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()
    if not url:
        return jsonify(error="url is required"), 400
    result = detector.scan_url(url, use_llm=data.get("use_llm", True))
    log_scan(result, url)
    return jsonify(result)


@app.post("/api/scan/email")
def scan_email():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify(error="text is required"), 400
    result = detector.scan_email(text, use_llm=data.get("use_llm", True))
    log_scan(result, text)
    return jsonify(result)


@app.get("/api/metrics")
def metrics():
    path = os.path.join(ROOT, "models", "metrics.json")
    with open(path) as f:
        return jsonify(json.load(f))


@app.get("/api/history")
def history():
    with db() as con:
        rows = con.execute("SELECT ts,type,input,verdict,score FROM scans ORDER BY id DESC LIMIT 25").fetchall()
    return jsonify([dict(zip(["ts", "type", "input", "verdict", "score"], r)) for r in rows])


if __name__ == "__main__":
    app.run(debug=True)
