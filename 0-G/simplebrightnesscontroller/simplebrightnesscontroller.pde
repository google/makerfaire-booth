import processing.net.*; 

import com.heroicrobot.dropbit.registry.*;
import com.heroicrobot.dropbit.devices.pixelpusher.Pixel;
import com.heroicrobot.dropbit.devices.pixelpusher.Strip;
import java.util.*;


import com.heroicrobot.dropbit.registry.*;
import com.heroicrobot.dropbit.devices.pixelpusher.Pixel;
import com.heroicrobot.dropbit.devices.pixelpusher.Strip;
import java.util.*;

private Random random = new Random();

DeviceRegistry registry;

class TestObserver implements Observer {
  public boolean hasStrips = false;
  public void update(Observable registry, Object updatedDevice) {
    println("Registry changed!");
    if (updatedDevice != null) {
      println("Device change: " + updatedDevice);
    }
    this.hasStrips = true;
  }
}

TestObserver testObserver;

Client myClient; 
int dataIn; 
String inString;

void setup() { 
  size(200, 200); 
  myClient = new Client(this, "127.0.0.1", 6000);

  registry = new DeviceRegistry();
  testObserver = new TestObserver();
  registry.addObserver(testObserver);
} 

color r = color(255, 0, 0);
color y = color(127, 127, 0);
color g = color(0, 255, 0);
color b = color(0, 0, 255);
color black = color(0, 0, 0);
color white = color(255,255,255);

boolean active = false;
long idleStart = 0;

void stateMachine(int value) {
  if (active) {
    if (value == 0) {
      if (idleStart == 0) {
        idleStart = millis();
      } else if (millis() - idleStart > 10000) {
        active = false;
        idleStart = 0;
      }
    }
  } else {
    if (value > 0) {
      active = true;
      idleStart = 0;
    }
  }
}

void draw() {
  int value;
  if (myClient.available() > 0) { 
    inString = myClient.readStringUntil(10); 
    if (inString != null) {
      value = Integer.parseInt(trim(inString));
    
      stateMachine(value);
      if (active) draw_dek(value);
      else {
        draw_white();
      }
    }
  }
}

void draw_dek(int value) {
  if (value < 0) value = 0;
  if (value > 1023) value = 1023;
  int scaleValue = (int) (value / 9.1);
  //println("Value=" + value);
  //println("ScaleValue=" + scaleValue);

  if (testObserver.hasStrips) {
    registry.startPushing();
    registry.setAutoThrottle(true);
    registry.setAntiLog(true);
    List<Strip> strips = registry.getStrips();

    if (strips.size() > 0) {
      for (Strip strip : strips) {
        for (int stripx = 0; stripx < scaleValue; stripx++) {
          if (stripx < 28) 
            strip.setPixel(b, stripx);
          else if (stripx < 56)
            strip.setPixel(g, stripx);
          else if (stripx < 84)
            strip.setPixel(y, stripx);
          else
            strip.setPixel(r, stripx);
        }
        for (int stripx = scaleValue; stripx < 240; stripx++) {
          strip.setPixel(black, stripx);
        }
      }
    }
  }
}


void draw_white() {
  if (testObserver.hasStrips) {
    registry.startPushing();
    registry.setAutoThrottle(true);
    registry.setAntiLog(true);
    List<Strip> strips = registry.getStrips();

    if (strips.size() > 0) {
      for (Strip strip : strips) {
        for (int stripx = 0; stripx < strip.getLength(); stripx++) {  
          strip.setPixel(white, stripx);
        }
      }
    }
  }
}