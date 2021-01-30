import time
import psutil
import requests 
import os
from sys import exit, argv 

def write_data_to_log_file(data, log_file):
  print(data, log_file)
  with open(log_file, "a") as f:
        f.write(data + "\n")
        f.close()

def run(name):
  log_file = 'client-'+name+'.log'

  print("Start sensor.")
  while True:
    # generate data
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    now = time.time()

    data = (name + " " + str(cpu) + " " +str(ram) + " "+ str(now)+ " "+ str(time.time_ns()))
    write_data_to_log_file(data, log_file)
    time.sleep(1)


if __name__ == "__main__":
  if len(argv) != 2:
    print("Sensor not called correctly. Use: [ python sensor.py <client-name> ]")
    exit(1)
  try:
    run(argv[1]) 
  except KeyboardInterrupt :
    exit(0)

