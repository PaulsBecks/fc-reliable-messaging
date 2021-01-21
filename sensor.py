import time
import psutil
import requests 
import os
from sys import exit, argv 

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
  print(data, log_file)
  with open(log_file, "a") as f:
        f.write(data + "\n")
        f.close()

def run(name):
  log_file = 'client-'+name+'.log'
  count_log_file = 'client-count-'+name+'.log'

  print("Start sensor.")
  count = read_client_count(count_log_file)
  while True:
    # generate data
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    now = time.time()

    data = (name + " " + str(cpu) + " " +str(ram) + " "+ str(now)+ " "+ str(count))
    write_data_to_log_file(data, log_file)
    count += 1
    write_client_count(count, count_log_file)
    time.sleep(1)


if __name__ == "__main__":
  if len(argv) != 2:
    print("Sensor not called correctly. Use: [ python sensor.py <client-name> ]")
    exit(1)
  try:
    run(argv[1]) 
  except KeyboardInterrupt :
    exit(0)

