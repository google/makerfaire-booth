import time
import gevent
import gevent.monkey
gevent.monkey.patch_all()
import socket
import serial

#r = (0,1,5,9,14,18,23,27,32,36,41,45,50,54,59,63,68,72,77,81,86,90,95,99)

THRESHOLD_LOW = -2
THRESHOLD_HIGH = 2

WINDOW_SIZE = 10

STATE_IDLE = "idle"
STATE_INFLATING = "inflating"
STATE_DEFLATING = "deflating"

last_state_time = -1
state = STATE_IDLE

values = []
value_index = 0;

for i in range(WINDOW_SIZE):
    values.append(THRESHOLD_LOW)
    
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
          addValue(adj)
          if (shouldInflate()):
              setState(STATE_INFLATING)
          elif (state == STATE_INFLATING):
              setState(STATE_DEFLATING)

      t0 = time.time()
      
def addValue(value):
    global value_index
    values[value_index] = value
    value_index = value_index + 1
    if (value_index >= WINDOW_SIZE):
        value_index=0
      
def setState(newState):
    global state
    global last_state_time
    if (state != newState):
        state = newState;
        last_state_time = time.time()
        print "New state", state

        if (state == STATE_INFLATING):
            doInflate()
        elif (state == STATE_DEFLATING):
            doDeflate()
        elif (state == STATE_IDLE):
            doIdle()

def shouldInflate():
    return sum(1 if isLevel(value) else 0 for value in values) > WINDOW_SIZE * 0.8;

def isLevel(value):
    return value > THRESHOLD_LOW and value < THRESHOLD_HIGH

def doInflate():
    print "Should inflate here"

def doDeflate():
    print "Should deflate here"

def doIdle():
    print "Should do nothing here"
      
client = gevent.spawn(client)

gevent.joinall([client])
