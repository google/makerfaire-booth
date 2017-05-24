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


s = serial.Serial("/dev/ttyACM0", 9600)
s.timeout = 1

ready = True

def read_from_port():
  global ready
  print("Starting to read")
  while True:
    reading = s.readline()
    if "woot." == reading:
      print("ready!")
      ready = True 
    #print(reading)


def client():
  prev = None
  client_socket = gevent.socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect(("127.0.0.1", 6000))
  t0 = time.time()
  num_zeroes = 0
  zero_threshold = 20
  while True:
    data = client_socket.recv(1024)
    try:
        value = int(data)
    except:
        print "failed to parse", data
    else:
        if prev:
          d = derivative(value, prev)
          if ready:
            if abs(d) > 5:
              print prev, value, d
              s.write("%d\r\n" % d)
              s.flush()
              num_zeroes = 0
            else:
              num_zeroes += 1
              if num_zeroes >= zero_threshold:
                print "ZERO"
                s.write("%d\r\n" % 0)
                s.flush()

        prev = value

client = gevent.spawn(client)
readthread = gevent.spawn(read_from_port)

gevent.joinall([client, readthread])
