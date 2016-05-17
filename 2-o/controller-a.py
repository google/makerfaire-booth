import time
import gevent
import gevent.monkey
gevent.monkey.patch_all()
import socket
import serial

#r = (0,1,5,9,14,18,23,27,32,36,41,45,50,54,59,63,68,72,77,81,86,90,95,99)

s = serial.Serial("/dev/ttyACM0", 115200)
s.timeout = 1

def handle_data(data):
  print(data)

def read_from_port():
  print("Starting to read")
  while True:
    reading = s.readline()
    handle_data(reading)

def client():
  client_socket = gevent.socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect(("127.0.0.1", 6000))
  t0 = time.time()
  while True:
    data = client_socket.recv(1024)
    t1 = time.time()
    if t1 - t0 > 0.2:
      try:
          value = int(data)
      except:
          print "failed to parse", data
      else:
          adj = int(value)
          print adj
          s.write("%d\r\n" % adj)
          s.flush()
      t0 = time.time()

client = gevent.spawn(client)
readthread = gevent.spawn(read_from_port)

gevent.joinall([client, readthread])

