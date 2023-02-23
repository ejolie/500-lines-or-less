from http.server import BaseHTTPRequestHandler, HTTPServer
import os


class ServerException(Exception):
    """For internal error reporting."""

    pass


class RequestHandler(BaseHTTPRequestHandler):
    """
    If the requested path maps to a file, that file is served.
    If anything goes wrong, an error page is constructed.
    """

    # How to display an error.
    Error_Page = """\
        <html>
        <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
        </body>
        </html>
        """

    # Classify and handle request.
    def do_GET(self):
        try:
            # Figure out what exactly is being requested.
            # - os.getcwd(): 현재 작업 경로
            # - self.path: URL에 있는, 유저가 요청한 파일 경로
            full_path = os.getcwd() + self.path

            # 해당 경로가 존재하지 않는 경우: 에러
            if not os.path.exists(full_path):
                raise ServerException(f"'{self.path}' not found")

            # 파일인 경우: 파일 읽어서 응답
            elif os.path.isfile(full_path):
                self.handle_file(full_path)

            # 그 외: 에러
            else:
                raise ServerException(f"Unknown object '{self.path}'")

        # Handle errors.
        except Exception as msg:
            print(msg)
            self.handle_error(msg)  # 에러 페이지 응답

    def handle_file(self, full_path):
        try:
            with open(full_path, "rb") as reader:
                content = reader.read()
            self.send_content(content)
        except IOError as msg:
            msg = f"'{self.path}' cannot be read: {msg}"
            self.handle_error(msg)

    # Handle unknown objects.
    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.send_content(content.encode("utf-8"), 404)

    # Send actual content.
    def send_content(self, content: bytes, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)


if __name__ == "__main__":
    server_address = ("", 8080)
    server = HTTPServer(server_address, RequestHandler)
    server.serve_forever()
