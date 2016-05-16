import processing.net.*; 

import com.heroicrobot.dropbit.registry.*;
import com.heroicrobot.dropbit.devices.pixelpusher.Pixel;
import com.heroicrobot.dropbit.devices.pixelpusher.Strip;
import com.heroicrobot.dropbit.devices.pixelpusher.PixelPusher;
import com.heroicrobot.dropbit.devices.pixelpusher.PusherCommand;
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
  size(640, 480, P3D); 
  myClient = new Client(this, "127.0.0.1", 6000);

  registry = new DeviceRegistry();
  testObserver = new TestObserver();
  registry.addObserver(testObserver);
   colorMode(HSB, 100);
  frameRate(60);
  prepareExitHandler();
} 



void mousePressed() {
  List<PixelPusher> pushers = registry.getPushers();
  println(mouseY);
    for (PixelPusher p: pushers) {
       PusherCommand pc = new PusherCommand(PusherCommand.GLOBALBRIGHTNESS_SET, (short)((65536.0 * mouseY) / height));
       spamCommand(p,  pc);
    }
 
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
    } else {
      idleStart = 0;
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
  if (!active) {
            draw_colourcycle();
  }
  
  if (myClient.available() > 0) { 
    inString = myClient.readStringUntil(10); 
    if (inString != null) {
      value = Integer.parseInt(trim(inString));
    
      stateMachine(value);
      println(value + " " + active);
      if (active) draw_dek(value);
      
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

/* From pixelpusher_colourcycle */

int[][] colors = {
  {
    127, 0, 0
  }
  , 
  {
    0, 127, 0
  }
  , 
  {
    0, 0, 127
  }
};

void spamCommand(PixelPusher p, PusherCommand pc) {
   for (int i=0; i<3; i++) {
    p.sendCommand(pc);
  }
}

public Pixel generateRandomPixel() {
  //return new Pixel((byte)(random.nextInt(scaling)),(byte)(random.nextInt(scaling)),(byte)(random.nextInt(scaling)));
  //return new Pixel((byte)(15), (byte)0, (byte)0);
  int[] colour = colors[random.nextInt(colors.length)];
  return new Pixel((byte)colour[0], (byte)colour[1], (byte)colour[2]);
}
int c = 0;


void draw_colourcycle() {
  int x=0;
  int y=0;
  if (testObserver.hasStrips) {   
    registry.startPushing();
    registry.setExtraDelay(0);
    registry.setAutoThrottle(true);
    registry.setAntiLog(true);    
    int stripy = 0;
    List<Strip> strips = registry.getStrips();
    
    if (++c > 99)
      c = 0;
    int numStrips = strips.size();
    //println("Strips total = "+numStrips);
    if (numStrips == 0)
      return;
    for (int stripNo = 0; stripNo < numStrips; stripNo++) {
      fill(c+(stripNo*2), 100, 100);
      rect(0, stripNo * (height/numStrips), width/2, (stripNo+1) * (height/numStrips)); 
      fill(c+((numStrips - stripNo)*2), 100, 100);
      rect(width/2, stripNo * (height/numStrips), width, (stripNo+1) * (height/numStrips));
    }    


    int yscale = height / strips.size();
    for (Strip strip : strips) {
      int xscale = width / strip.getLength();
      for (int stripx = 0; stripx < strip.getLength(); stripx++) {
        x = stripx*xscale + 1;
        y = stripy*yscale + 1; 
        color c = get(x, y);

        strip.setPixel(c, stripx);
      }
      stripy++;
    }
  }
}
private void prepareExitHandler () {

  Runtime.getRuntime().addShutdownHook(new Thread(new Runnable() {

    public void run () {

      System.out.println("Shutdown hook running");

      List<Strip> strips = registry.getStrips();
      for (Strip strip : strips) {
        for (int i=0; i<strip.getLength(); i++)
          strip.setPixel(#000000, i);
      }
      for (int i=0; i<100000; i++)
        Thread.yield();
    }
  }
  ));
}