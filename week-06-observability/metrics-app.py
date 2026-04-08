# Flask app that exposes custom Prometheus metrics
# Prometheus scrapes the /metrics endpoint every 15 seconds

import os
import time
import random
from flask import Flask, jsonify
from prometheus_client import Counter, Histogram, Gauge, generate_latest

app = Flask(__name__)

# COUNTER — only goes up. Good for: total requests, errors, bytes sent
# Labels let you break down the metric by method, path, status
REQUEST_COUNT = Counter(
    'http_requests_total',                    # Metric name (Prometheus convention: snake_case)
    'Total HTTP requests received',           # Description
    ['method', 'path', 'status']              # Labels for filtering
)

# HISTOGRAM — tracks distribution of values. Good for: response times, request sizes
# Buckets define the ranges: how many requests took <0.1s, <0.25s, <0.5s, etc.
REQUEST_DURATION = Histogram(
    'http_request_duration_seconds',
    'Time spent processing request',
    buckets=[0.01, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5]
)

# GAUGE — goes up and down. Good for: temperature, queue size, active connections
ACTIVE_REQUESTS = Gauge(
    'http_active_requests',
    'Number of requests currently being processed'
)

@app.route("/")
def home():
    ACTIVE_REQUESTS.inc()                     # +1 active request
    start = time.time()                        # Start timer
    
    # Simulate variable response time (0-500ms)
    time.sleep(random.uniform(0, 0.5))
    
    duration = time.time() - start
    REQUEST_DURATION.observe(duration)         # Record how long it took
    REQUEST_COUNT.labels(method="GET", path="/", status="200").inc()  # Count it
    ACTIVE_REQUESTS.dec()                     # -1 active request
    
    hostname = os.environ.get("HOSTNAME", "unknown")
    return jsonify({
        "message": "Hello from metrics app!",
        "pod": hostname,
        "response_time_ms": round(duration * 1000, 2)
    })

@app.route("/error")
def error():
    """Endpoint that always fails — generates error metrics"""
    REQUEST_COUNT.labels(method="GET", path="/error", status="500").inc()
    return jsonify({"error": "Something went wrong!"}), 500

@app.route("/slow")
def slow():
    """Endpoint that's deliberately slow — shows up in duration histograms"""
    ACTIVE_REQUESTS.inc()
    start = time.time()
    
    time.sleep(random.uniform(1, 3))          # Sleep 1-3 seconds
    
    duration = time.time() - start
    REQUEST_DURATION.observe(duration)
    REQUEST_COUNT.labels(method="GET", path="/slow", status="200").inc()
    ACTIVE_REQUESTS.dec()
    return jsonify({"message": "That was slow!", "duration_seconds": round(duration, 2)})

@app.route("/metrics")
def metrics():
    """Prometheus scrapes this endpoint to collect all metrics"""
    return generate_latest()                   # Returns all metrics in Prometheus format

@app.route("/health")
def health():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    print("Metrics app starting on port 8080...")
    app.run(host="0.0.0.0", port=8080)
