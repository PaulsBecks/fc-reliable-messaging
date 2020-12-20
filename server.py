from http.server import HTTPServer,BaseHTTPRequestHandler
import signal
import sys

class Server(BaseHTTPRequestHandler) :
  def _set_response(self):
      self.send_response(200)
      self.send_header('Content-type', 'text/html')
      self.end_headers()

  def do_POST(self):
    content_length = int(self.headers['Content-Length']) 
    data = self.rfile.read(content_length).decode('utf-8')
    with open("server.log", "a") as f:
        f.write(str(data) + "\n")
        f.close()
    print(data)
    self._set_response()

def stop_server(server):
  print("Stop server.")
  server.server_close()
  sys.exit(0)

def run(server_class=HTTPServer, handler_class=Server):
  print("Start server on port 8000.")
  server_address = ('', 8000)
  httpd = server_class(server_address, handler_class)
  httpd.handle_request()
  try:
    httpd.serve_forever()
  except KeyboardInterrupt :
    stop_server(httpd)




if __name__ == "__main__":
  print("Create server")
  run() 