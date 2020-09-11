#!/usr/bin/env python3

from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus
from urllib.parse import urlsplit, unquote
import json
import unicodedata
import shutil

from charindex import build_index, search


class SearchHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        query = unquote(urlsplit(self.path).query).strip()
        if query:
            self.search(query)
        else:
            self.form()

    def search(self, query):
        self.send_header("Content-type", "application/json")
        self.end_headers()
        chars = search(index, query)
        results = []
        for char in chars:
            name = unicodedata.name(char)
            results.append({"char": char, "name": name})
        data = json.dumps(results).encode("UTF-8")
        self.wfile.write(data)

    def form(self):
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        with open("form.html", "rb") as fp:
            shutil.copyfileobj(fp, self.wfile)


def main(port):
    address = ("", port)
    httpd = ThreadingHTTPServer(address, SearchHandler)
    host, port = httpd.server_address
    print(f"Serving on: http://{host}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    index = build_index()
    main(8000)
