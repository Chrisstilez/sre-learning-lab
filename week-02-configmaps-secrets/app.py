import os
import json
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    app_env = os.environ.get("APP_ENV", "unknown")
    log_level = os.environ.get("LOG_LEVEL", "unknown")
    app_name = os.environ.get("APP_NAME", "unknown")
    return jsonify({
        "message": "Hello from the config demo app!",
        "environment": app_env,
        "log_level": log_level,
        "app_name": app_name
    })

@app.route("/secret")
def secret():
    db_user = os.environ.get("DB_USERNAME", "not set")
    db_pass = os.environ.get("DB_PASSWORD", "not set")
    return jsonify({
        "db_username": db_user,
        "db_password_set": db_pass != "not set"
    })

@app.route("/features")
def features():
    config_path = "/etc/config/config.json"
    try:
        with open(config_path) as f:
            config = json.load(f)
        return jsonify(config)
    except FileNotFoundError:
        return jsonify({"error": "Config file not found"}), 404

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    port = int(os.environ.get("APP_PORT", 8080))
    print(f"Starting on port {port}, env: {os.environ.get('APP_ENV', 'unknown')}")
    app.run(host="0.0.0.0", port=port)
