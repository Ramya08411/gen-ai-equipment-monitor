import csv, time, requests

with open("sensor_data.csv") as f:
    for row in csv.DictReader(f):
        payload = {k: float(v) for k, v in row.items()}
        r = requests.post("http://localhost:5000/data", json=payload)
        print("Sent", payload, "->", r.status_code)
        time.sleep(2)