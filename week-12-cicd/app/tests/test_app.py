import unittest
import json
import sys
import os
import threading
import time
from http.client import HTTPConnection

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app import Handler, HTTPServer

class TestApp(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = HTTPServer(("127.0.0.1", 9999), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever)
        cls.thread.daemon = True
        cls.thread.start()
        time.sleep(0.5)

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def test_root_returns_200(self):
        conn = HTTPConnection("127.0.0.1", 9999)
        conn.request("GET", "/")
        resp = conn.getresponse()
        self.assertEqual(resp.status, 200)
        body = resp.read().decode()
        self.assertIn("SRE App", body)

    def test_health_returns_json(self):
        conn = HTTPConnection("127.0.0.1", 9999)
        conn.request("GET", "/health")
        resp = conn.getresponse()
        self.assertEqual(resp.status, 200)
        data = json.loads(resp.read().decode())
        self.assertEqual(data["status"], "ok")
        self.assertIn("version", data)

    def test_404_for_unknown_path(self):
        conn = HTTPConnection("127.0.0.1", 9999)
        conn.request("GET", "/nonexistent")
        resp = conn.getresponse()
        self.assertEqual(resp.status, 404)

if __name__ == "__main__":
    unittest.main()
