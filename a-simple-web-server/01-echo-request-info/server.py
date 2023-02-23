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
<table>
<tr>  <td>Header</td>         <td>Value</td>          </tr>
<tr>  <td>Date and time</td>  <td>{date_time}</td>    </tr>
<tr>  <td>Client host</td>    <td>{client_host}</td>  </tr>
<tr>  <td>Client port</td>    <td>{client_port}s</td> </tr>
<tr>  <td>Command</td>        <td>{command}</td>      </tr>
<tr>  <td>Path</td>           <td>{path}</td>         </tr>
</table>
</body>
</html>
"""

    # Handle a GET request.
    def do_GET(self):
        page = self.create_page()
        self.send_page(page)

    def create_page(self):
        values = {
            "date_time": self.date_time_string(),
            "client_host": self.client_address[0],
            "client_port": self.client_address[1],
            "command": self.command,
            "path": self.path,
        }
        page = self.Page.format(**values)
        return page

    def send_page(self, page: str):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(page)))
        self.end_headers()  # 헤더와 페이지 자체를 구분하는 blank line 삽입
        self.wfile.write(page.encode("utf-8"))


if __name__ == "__main__":
    server_address = ("", 8080)  # localhost:8080
    server = HTTPServer(server_address, RequestHandler)
    server.serve_forever()
