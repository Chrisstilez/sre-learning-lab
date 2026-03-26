# Flask web app that serves HTML and calls the backend API
# Demonstrates service-to-service communication inside Kubernetes

import os
import requests                                         # Library for making HTTP calls
from flask import Flask

app = Flask(__name__)

# Backend URL uses the Kubernetes Service name
# CoreDNS resolves "backend" to the Service's ClusterIP
# This is service discovery — no hardcoded IPs
BACKEND_URL = os.environ.get("BACKEND_URL", "http://backend:8080")

@app.route("/")
def home():
    """Main page — calls the backend API and displays the result"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/data", timeout=3)  # 3 second timeout
        data = response.json()                          # Parse JSON response from backend
        return f"""
        <html>
        <head><title>SRE Lab - Week 4</title></head>
        <body style="font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto;">
            <h1>Frontend</h1>
            <p><strong>Backend says:</strong> {data['message']}</p>
            <p><strong>Served by pod:</strong> {data['pod']}</p>
            <p><strong>API version:</strong> {data['version']}</p>
            <hr>
            <p style="color: gray;">Frontend pod: {os.environ.get('HOSTNAME', 'unknown')}</p>
        </body>
        </html>
        """
    except requests.exceptions.ConnectionError:
        return "<h1>Frontend</h1><p style='color:red;'>Cannot reach backend!</p>", 503
    except requests.exceptions.Timeout:
        return "<h1>Frontend</h1><p style='color:red;'>Backend timed out!</p>", 504

@app.route("/health")
def health():
    return "OK"

if __name__ == "__main__":
    print("Frontend starting on port 80...")
    app.run(host="0.0.0.0", port=80)                   # Frontends traditionally run on port 80
