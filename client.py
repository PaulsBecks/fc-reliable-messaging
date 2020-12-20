import time
import psutil
import requests 
from sys import exit, argv 

BACKEND_URL = "http://localhost:8000"

def run(name):
  print("Start client.")
  log_file = 'client-'+name+'.log'
  while True:
    # check if data is in file if so send it line by line to the server
    try:
      with open(log_file, 'r+') as f:
        for line in f:
            requests.post(BACKEND_URL, line.rstrip().encode('utf-8'))
        f.truncate(0)
    except FileNotFoundError:
      print("No log file available.")
    except requests.exceptions.RequestException:
      print("Could not send file info to server.")

    # generate data
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    now = time.time()

    data = (name + " " + str(cpu) + " " +str(ram) + " "+ str(now))

    # try to send data to the server
    try:
      requests.post(BACKEND_URL, data.encode('utf-8'))
    except requests.exceptions.RequestException:
      print("Could not send info to server. Store locally.")
      with open(log_file, "a") as f:
        f.write(data + "\n")
        f.close()
    time.sleep(1)


if __name__ == "__main__":
  if len(argv) != 2:
    print("Client not called correctly. Use: [ python client.py <client-name> ]")
    exit(1)
  try:
    run(argv[1]) 
  except KeyboardInterrupt :
    exit(0)