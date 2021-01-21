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
    print(data)
    dataSplit = data.split(" ")
    peerId = str(dataSplit[0])
    count = str(dataSplit[-1])
    peerLogFile = "server-"+peerId+".log"
    def send_response():
      self.send_response(200)
      self.send_header("Content-type", "text/html")
      self.end_headers()
      self.wfile.write(("ACK "+count).encode("utf-8"))

    try:
      with open(peerLogFile, "r") as f:
        lastEntry = f.readlines()[-1]
        lastId = str(lastEntry.split(" ")[-1])
        if int(lastId) > int(count):
          send_response()
          return
    except (FileNotFoundError, IndexError):
      print("No server.log file available yet.")

    with open(peerLogFile, "a") as f:
        print("write: "+str(data))
        f.write(str(data) + "\n")
        f.close()
    send_response()
    

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