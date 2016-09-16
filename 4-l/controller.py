import time
import gevent
import gevent.monkey
gevent.monkey.patch_all()
import socket
import serial

#r = (0,1,5,9,14,18,23,27,32,36,41,45,50,54,59,63,68,72,77,81,86,90,95,99)

STATE_IDLE = 0
STATE_DATA_WINDOW_START = 1
STATE_DATA_WINDOW_END = 2
STATE_LAUNCH = 3
STATE_REST = 4

VALUE_IDLE = 5

DATA_WINDOW_LENGTH_S = .5
REST_LENGTH_S = 4

state = -1
lastStateTime = -1

port = "/dev/ttyACM0"
s = serial.Serial(port, 115200)
time.sleep(2)

def setState(newState):
  global state
  global lastStateTime  
  if (state != newState):  
    state = newState
    lastStateTime = time.time()
    print "Changing state: %s" % newState
    if (state == STATE_REST):
      s.write("r\r\n")
      s.flush()
    elif (state == STATE_IDLE):
      s.write("g\r\n")
      s.flush()        

def client():
  global state
  global lastStateTime  
  client_socket = gevent.socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client_socket.connect(("127.0.0.1", 6000))
  t0 = time.time()
  while True:
    data = client_socket.recv(1024)
    for dpart in data.split():    
      try:
        value = int(dpart)
      except:
        print "failed to parse [%s]" % data
        continue
    
      delta = abs(value - VALUE_IDLE)
      print delta

    t1 = time.time()
    if t1 - t0 > 0.05:
      if (state == STATE_IDLE and delta > 2):
        setState(STATE_DATA_WINDOW_START)
        integrationValue = 0;
      if (state == STATE_DATA_WINDOW_START):
        # gather and integrate data during the window
        integrationValue += delta
        if (t1 - lastStateTime > DATA_WINDOW_LENGTH_S):
          setState(STATE_DATA_WINDOW_END)
      if (state == STATE_DATA_WINDOW_END):
        # take the total data and send it to the arduino
        print "Sending integrationValue %s" % integrationValue
        s.write("%d\r\n" % integrationValue)
        s.flush()
        setState(STATE_REST)

      if (state == STATE_REST):
        if (t1 - lastStateTime > REST_LENGTH_S):
          setState(STATE_IDLE)

      t0 = time.time()

setState(STATE_IDLE)

client = gevent.spawn(client)

gevent.joinall([client])

