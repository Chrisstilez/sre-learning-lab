from http.server import HTTPServer, BaseHTTPRequestHandler
import json, os, random, time, logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)
logger = logging.getLogger("sre-app")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
            logger.info("Health check passed")
        elif self.path == "/api/data":
            # Simulate occasional errors
            if random.random() < 0.3:
                logger.error("Database connection timeout after 30s")
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": "database timeout"}).encode())
            else:
                latency = random.uniform(0.01, 0.5)
                time.sleep(latency)
                logger.info(f"Request processed in {latency:.3f}s")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"data": "ok", "latency": f"{latency:.3f}s"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress default access logs

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    server = HTTPServer(("0.0.0.0", port), Handler)
    logger.info(f"Logger app listening on port {port}")
    server.serve_forever()
