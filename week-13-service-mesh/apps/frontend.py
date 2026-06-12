from http.server import HTTPServer, BaseHTTPRequestHandler
import json, os
from urllib.request import urlopen

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:8080")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            try:
                resp = urlopen(f"{BACKEND_URL}/api/data", timeout=5)
                backend_data = json.loads(resp.read().decode())
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "source": "frontend",
                    "backend_response": backend_data
                }).encode())
            except Exception as e:
                self.send_response(502)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({
                    "source": "frontend",
                    "error": str(e)
                }).encode())
        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        print(f"[frontend] {args[0]}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"Frontend listening on port {port}")
    server.serve_forever()
