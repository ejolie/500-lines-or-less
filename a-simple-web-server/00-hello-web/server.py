from http.server import BaseHTTPRequestHandler, HTTPServer


# BaseHTTPRequestHandler
# - HTTP 요청 파싱
# - HTTP 메서드에 따라 수행할 작업 정의
class RequestHandler(BaseHTTPRequestHandler):
    """Handle HTTP requests by returning a fixed 'page'."""

    # Page to send back.
    Page = """\
<html>
<body>
<p>Hello, web!</p>
</body>
</html>
"""

    # Handle a GET request.
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(self.Page)))
        self.end_headers()  # 헤더와 페이지 자체를 구분하는 blank line 삽입
        self.wfile.write(self.Page.encode("utf-8"))


if __name__ == "__main__":
    server_address = ("", 8080)  # localhost:8080
    server = HTTPServer(server_address, RequestHandler)
    server.serve_forever()
