"""Example app for the platform template: a small web service with no dependencies.

- GET /healthz answers 200 (the compose healthcheck calls it).
- GET / shows the app name and which credential files the platform provided (names only).

Credentials are files under /run/secrets/<NAME>, never environment variables. Read them when
you need them; never print or log their values.
"""

import html
import json
import os
import signal
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

SECRETS_DIR = Path("/run/secrets")
APP_NAME = os.environ.get("APP_NAME", "app")
PORT = 8080


def secret(name):
    """The value of a credential file, or None if the platform didn't provide it."""
    path = SECRETS_DIR / name
    try:
        return path.read_text().strip()
    except OSError:
        return None


def provided_secrets():
    try:
        return sorted(p.name for p in SECRETS_DIR.iterdir() if p.is_file())
    except OSError:
        return []


class Handler(BaseHTTPRequestHandler):
    server_version = "app"
    sys_version = ""

    def do_GET(self):
        if self.path == "/healthz":
            self._send(200, "application/json", json.dumps({"status": "ok"}))
        elif self.path == "/":
            names = "".join("<li>%s</li>" % html.escape(n) for n in provided_secrets())
            user = self.headers.get("X-authentik-username", "")
            body = (
                "<!doctype html><title>%s</title><h1>%s</h1>"
                "<p>Signed in as: %s</p><p>Credential files:</p><ul>%s</ul>"
                % (html.escape(APP_NAME), html.escape(APP_NAME), html.escape(user or "-"), names or "<li>none</li>")
            )
            self._send(200, "text/html; charset=utf-8", body)
        else:
            self._send(404, "application/json", json.dumps({"error": "not found"}))

    def _send(self, status, content_type, body):
        data = body.encode()
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        # One line per request without query strings (they could carry tokens).
        sys.stdout.write("%s %s\n" % (self.command, self.path.split("?", 1)[0]))
        sys.stdout.flush()


def main():
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    signal.signal(signal.SIGTERM, lambda *_: server.shutdown())
    print("listening on :%d" % PORT, flush=True)
    try:
        server.serve_forever()
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
