from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus
import time


HOURGLASS = '\u23F3'  # ⏳ HOURGLASS WITH FLOWING SAND

HTML = '''
<html>
    <head>
        <meta http-equiv="refresh" content="1">
    </head>
    <body>
        <h1>{text}</h1>
    </body>
</html>
'''


class TimeHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        now = time.strftime('%H:%M:%S')
        text = HTML.format(text=f'{HOURGLASS} {now}')
        data = text.encode('UTF-8')
        self.wfile.write(data)


def main(port):
    address = ('', port)
    httpd = ThreadingHTTPServer(address, TimeHandler)
    host, port = httpd.server_address
    print(f'Serving on: http://{host}:{port}')
    httpd.serve_forever()


if __name__ == '__main__':
    main(8000)
