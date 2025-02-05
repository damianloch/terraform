from http.server import SimpleHTTPRequestHandler, HTTPServer

PORT = 8000

class MyHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello from Terraform-provisioned EC2!")

server = HTTPServer(("0.0.0.0", PORT), MyHandler)
print(f"Serving on port {PORT}")
server.serve_forever()
