from http.server import HTTPServer, BaseHTTPRequestHandler
import json, os

VERSION = os.getenv("APP_VERSION", "v1")

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/data":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({
                "source": "backend",
                "version": VERSION,
                "message": f"Hello from backend {VERSION}"
            }).encode())
        elif self.path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok", "version": VERSION}).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        print(f"[backend-{VERSION}] {args[0]}")

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8080"))
    server = HTTPServer(("0.0.0.0", port), Handler)
    print(f"Backend {VERSION} listening on port {port}")
    server.serve_forever()
