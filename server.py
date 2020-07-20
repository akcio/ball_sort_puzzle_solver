from http.server import HTTPServer, BaseHTTPRequestHandler


class MyHandler(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        super().__init__(request, client_address, server)
        self._fileContent = ""
        try:
            f = open("index.html", "r")
            self._fileContent = f.read()
            f.close()
        except:
            self.content = "File read error"

    def do_GET(self):
        content_type = "text/html"
        content = ""
        try:
            f = open("index.html", "r")
            content = f.read()
            f.close()
        except:
            content = "File read error"
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(content.encode())

    def do_POST(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        length = int(self.headers['content-length'])
        request =  self.rfile.read(length)
        import json
        print(json.loads(request))
        from solver import Solver
        result = Solver.solve(json.loads(request))
        self.wfile.write(json.dumps(result).encode())


def run(server_class=HTTPServer, handler_class=MyHandler):
    server_address = ('', 8000)
    httpd = server_class(server_address, handler_class)
    try:
        httpd.serve_forever()
    except:
        exit(0)


if __name__ == '__main__':
    run()