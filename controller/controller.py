import time
import gevent
import gevent.monkey
gevent.monkey.patch_all()
import socket
import serial

s = serial.Serial("/dev/ttyUSB0", 115200)
time.sleep(10)
def client():
  client_socket = gevent.socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect(("127.0.0.1", 6000))
  t0 = time.time()
  values = []
  while True:
    data = client_socket.recv(1024)
    value = int(data)
    adj = value / 3
    values.append(adj)
    t1 = time.time()
    if (t1 - t0) > 1:
      print values
      mean = sum(values) / len(values)
      print mean
      values = []
      t0 = time.time()
      s.read()
      s.write("%d\r\n" % mean)
      s.flush()

client = gevent.spawn(client)

gevent.joinall([client])
