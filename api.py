import sqlite3, datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
DB = "readings.db"

def init():
    with sqlite3.connect(DB) as c:
        c.execute("""CREATE TABLE IF NOT EXISTS readings
                     (ts TEXT, temperature REAL, voltage REAL, current REAL)""")

@app.post("/data")
def data():
    d = request.get_json()
    with sqlite3.connect(DB) as c:
        c.execute("INSERT INTO readings VALUES (?,?,?,?)",
                  (datetime.datetime.now().isoformat(timespec="seconds"),
                   d["temperature"], d["voltage"], d["current"]))
    print("Received:", d)
    return jsonify(ok=True)

if __name__ == "__main__":
    init()
    app.run(port=5000)