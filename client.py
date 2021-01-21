import time
import psutil
import requests 
import os
from sys import exit, argv 

BACKEND_URL = "http://localhost:8000"

def write_client_count(count, file_name):
  with open(file_name, "w") as f:
    f.write(str(count))
    f.close()

def read_client_count(file_name):
  count = 0
  try:
    with open(file_name, "r") as f:
      count = int(f.read()) + 1
      f.close()
  except:
    print("file does not exists")
  return count

def write_data_to_log_file(data, log_file):
  print("Could not send info to server. Store locally.")
  with open(log_file, "a") as f:
        f.write(data + "\n")
        f.close()

def file_is_empty(file_path):
  try:
    return os.path.getsize(file_path) == 0
  except OSError:
    return True

def run(name):
  log_file = 'client-'+name+'.log'
  count_log_file = 'client-count-'+name+'.log'

  print("Start client.")
  count = read_client_count(count_log_file)
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

    data = (name + " " + str(cpu) + " " +str(ram) + " "+ str(now)+ " "+ str(count))

    # try to send data to the server+
    if file_is_empty(log_file):  
      try:
          response = requests.post(BACKEND_URL, data.encode('utf-8'))
          print(response.text)
      except requests.exceptions.RequestException as err:
        write_data_to_log_file(data, log_file)
    else:
      write_data_to_log_file(data, log_file)
    time.sleep(1)
    count += 1
    write_client_count(count, count_log_file)


if __name__ == "__main__":
  if len(argv) != 2:
    print("Client not called correctly. Use: [ python client.py <client-name> ]")
    exit(1)
  try:
    run(argv[1]) 
  except KeyboardInterrupt :
    exit(0)

