import time
import psutil
import requests 
import os
from sys import exit, argv 

BACKEND_URL = "http://localhost:8000"

def file_is_empty(file_path):
  try:
    return os.path.getsize(file_path) == 0
  except OSError:
    return True

def run(name):
  log_file = 'client-'+name+'.log'

  print("Start client.")
  while True:
    # check if data is in file if so send it line by line to the server
    try:
      with open(log_file, 'r+') as f:
        for line in f:
            response = requests.post(BACKEND_URL, line.rstrip().encode('utf-8'))
            print(response.text)
        f.truncate(0)
    except FileNotFoundError:
      print("No log file available.")
    except requests.exceptions.RequestException:
      print("Could not send file info to server.")
    time.sleep(1)

if __name__ == "__main__":
  if len(argv) != 2:
    print("Client not called correctly. Use: [ python client.py <client-name> ]")
    exit(1)
  try:
    run(argv[1]) 
  except KeyboardInterrupt :
    exit(0)

