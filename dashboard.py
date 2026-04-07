import tkinter as tk
from tkinter import scrolledtext
import threading
import time
import os

# Create window
root = tk.Tk()
root.title("IoT Security Monitoring Dashboard")
root.geometry("700x500")

# Title
title = tk.Label(root, text="IoT Security Dashboard", font=("Arial", 18, "bold"))
title.pack(pady=10)

# Status label
status_label = tk.Label(root, text="System Status: SECURE", font=("Arial", 14))
status_label.pack(pady=5)

# Log display area
log_area = scrolledtext.ScrolledText(root, width=80, height=20)
log_area.pack(pady=10)

# Function to update logs
def update_logs():
    while True:
        if os.path.exists("logs/alerts.log"):
            with open("logs/alerts.log", "r") as file:
                logs = file.readlines()

                log_area.delete(1.0, tk.END)

                for log in logs[-20:]:  # show last 20 logs
                    log_area.insert(tk.END, log)

                # Update system status
                if any("High traffic" in log or "Blocked" in log for log in logs[-5:]):
                    status_label.config(text="System Status: UNDER THREAT", fg="red")
                else:
                    status_label.config(text="System Status: SECURE", fg="green")

        time.sleep(3)

# Run log update in background thread
thread = threading.Thread(target=update_logs, daemon=True)
thread.start()

# Run GUI
root.mainloop()