from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    if os.path.exists("logs/alerts.log"):
        with open("logs/alerts.log", "r") as file:
            logs = file.readlines()
    else:
        logs = ["No logs yet"]

    html = "<h2>IoT Security Alerts</h2><hr>"
    for log in logs:
        html += f"<p>{log}</p>"

    return html

if __name__ == "__main__":
    app.run(debug=True)