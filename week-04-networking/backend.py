# Simple Flask API that returns JSON data
# This runs as a separate service that the frontend calls

import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/data")
def get_data():
    """Returns a JSON response with a message and the pod's hostname"""
    hostname = os.environ.get("HOSTNAME", "unknown")  # K8s sets this to the pod name
    return jsonify({
        "message": "Hello from the backend!",
        "pod": hostname,                                # Shows which pod handled the request
        "version": "v1"
    })

@app.route("/api/health")
def health():
    """Health check endpoint — Kubernetes can use this to verify the app is alive"""
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    print("Backend starting on port 8080...")
    app.run(host="0.0.0.0", port=8080)                # Listen on all interfaces, port 8080
