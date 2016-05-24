import time
import gevent
import gevent.monkey
gevent.monkey.patch_all()
import socket
import serial

#r = (0,1,5,9,14,18,23,27,32,36,41,45,50,54,59,63,68,72,77,81,86,90,95,99)

s = serial.Serial("/dev/ttyACM0", 115200)
time.sleep(2)

def client():
  client_socket = gevent.socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect(("127.0.0.1", 6000))
  t0 = time.time()
  maxdelta = 0
  while True:
    data = client_socket.recv(1024)
    for dpart in data.split():    
      try:
        value = int(dpart)
      except:
        print "failed to parse [%s]" % data
        continue
    
      delta = abs(value - 5)
      maxdelta = max(delta, maxdelta)
      
    t1 = time.time()
    if t1 - t0 > 0.05:
          adj = maxdelta
          maxdelta = 0
          if (adj > 2):
              print "PRESCALE: %s" % adj
              scaled = min(100, (adj - 2) * 20)
	      print "BIG: %s" % scaled
	      s.write("%d\r\n" % scaled)
              s.flush()
     	  t0 = time.time()

client = gevent.spawn(client)

gevent.joinall([client])
