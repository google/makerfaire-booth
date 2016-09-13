import time
import gevent
import gevent.monkey
gevent.monkey.patch_all()
import socket
import serial

def derivative(value, prev):
  deriv = value - prev
  if (abs(deriv) < 180):
    print prev, value, deriv
  else:
    deriv = value - (prev-360)
    if (abs(deriv) < 180):
      print prev, value, deriv
    else:
      deriv = (360-value) - prev
  return deriv


# s = serial.Serial("/dev/ttyACM1", 115200)
def client():
  prev = None
  client_socket = gevent.socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect(("127.0.0.1", 6000))
  t0 = time.time()
  while True:
    data = client_socket.recv(1024)
    try:
        value = int(data)
    except:
        print "failed to parse", data
    else:
        if prev:
          d = derivative(value, prev)
          print prev, value, d
        prev = value
    #     s.write("%d\r\n" % adj)
    #     s.flush()

client = gevent.spawn(client)

gevent.joinall([client])
