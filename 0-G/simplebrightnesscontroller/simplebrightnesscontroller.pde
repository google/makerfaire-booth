  

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
 
void draw() { 
  if (myClient.available() > 0) { 
    inString = myClient.readStringUntil(10); 
    if (inString != null) {
      int value = Integer.parseInt(trim(inString));
      int scaleValue = int(value / 365. * 255);
      color c = color(scaleValue, scaleValue, scaleValue);
      if (testObserver.hasStrips) {
        registry.startPushing();
        registry.setAutoThrottle(true);
        registry.setAntiLog(true);
        int stripy = 0;
        List<Strip> strips = registry.getStrips();
  
        if (strips.size() > 0) {
          for(Strip strip : strips) {
            for (int stripx = 0; stripx < strip.getLength(); stripx++) {
              strip.setPixel(c, stripx);
            }
            stripy++;
          }
        }
      }
    }
  }
}