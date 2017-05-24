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
PFont f;

void setup() { 
  size(640, 480); 
  myClient = new Client(this, "127.0.0.1", 6000);

  registry = new DeviceRegistry();
  testObserver = new TestObserver();
  registry.addObserver(testObserver);
  colorMode(HSB, 100);
  frameRate(60);
  prepareExitHandler();
  f = createFont("Arial", 16, true); // Arial, 16 point, anti-aliasing on
} 



color red = color(255, 0, 0);
color yellow = color(255, 255, 0);
color green = color(0, 255, 0);
color blue = color(0, 0, 255);
color black = color(0, 0, 0);
color white = color(255, 255, 255);

boolean active = true;
long idleStart = 0;
boolean fading = false;
boolean victory = true;
long victoryStart = 0;
int fadeTime = 30000;
int value = 0;
int victoryMax = 1000;
int victoryThreshold = 240;
float progress;
int numLeds = 112;

void stateMachine() {
  if (active) {
    if (value == 0) {
      if (fading) {
        if (progress > 1.) {
          // If we're active, reading zero, and already fading and the fade timer has exceeded, enter inactive state
          active = false;
          victory = false;
          victoryStart = 0;
          fading = false;
          idleStart = 0;
        } else {
          // If we're active, reading zero, and already fading and the fade timer has not exceeded, just keep fading
        }
      } else {
        // If we're active, reading zero, and not already fading, start fading
        idleStart = millis();
        fading = true;
        victory = false;
        victoryStart = 0;
      }
    } else if (value > victoryThreshold) {
      // If we're active, reading non-zero, and user is above threshold, enter victory cycle
      victory = true;
      victoryStart = millis();
      idleStart = 0;
      fading = false;
    } else {
      // If we're active, reading non-zero, and user is below threshold, exit victory cycle
      victory = false;
      fading = false;
      victoryStart = 0;
      idleStart = 0;
    }
  } else {
    // if we're inactive and detect activity, enter active state
    if (value > 0) {
      victory = false;
      victoryStart = 0;
      active = true;
      fading = false;
      idleStart = 0;
    }
  }
}

void draw() {
  background(white);


  while (myClient.available() > 0) { 
    inString = myClient.readStringUntil(10); 
    if (inString != null) {
      value = Integer.parseInt(trim(inString));

    }
  }  
  //stateMachine();

  progress = (millis() - idleStart)/(float)fadeTime;
  int fadeValue = (int) (progress * 255);

  if (active) {
    if (victory) {
      text("Victory!", 0, 220);
      draw_victory_loop();
    } else if (fading) {
      text("Fading!", 0, 220);
      draw_fade(fadeValue);
    } else {
      text("dek!", 0, 220);
      draw_dek();
    }
  } else {
    text("colorcycle!", 0, 220);
    draw_colourcycle();
  }


  textFont(f, 36);
  fill(black);

  text("Value: " + value, 0, 36);
  text("Active: " + active, 0, 72);
  text("Victory: " + victory + " ", 0, 108);
  text("Fading: " + fading + " ", 0, 144);
  if (fading)
    text("Fade value: " + fadeValue + " " + nf(progress, 2, 2) + " " + idleStart, 0, 180);
}

void clear_strips() {
  List<Strip> strips = registry.getStrips();
  for (Strip strip : strips) {
    for (int i=0; i<strip.getLength(); i++)
      strip.setPixel(#000000, i);
  }
}

void setup_registry() {
  registry.startPushing();
  registry.setAutoThrottle(true);
  registry.setAntiLog(true);
}

void draw_dek() {
  clear_strips();
  float scaleValue = numLeds / (float)victoryThreshold;

  if (testObserver.hasStrips) {
    setup_registry();
    List<Strip> strips = registry.getStrips();

    if (strips.size() > 0) {
      for (Strip strip : strips) {
        for (int stripx = 0; stripx < scaleValue*value; stripx++) {
          if (stripx < (victoryThreshold*scaleValue*0.25)) 
            strip.setPixel(blue, stripx);
          else if (stripx < (victoryThreshold*scaleValue*0.5))
            strip.setPixel(green, stripx);
          else if (stripx < (victoryThreshold*scaleValue*0.75))
            strip.setPixel(yellow, stripx);
          else if (stripx < (victoryThreshold*scaleValue*1.0))
            strip.setPixel(red, stripx);
        }
      }
    }
  }
}

int victory_loop = 0;

void draw_victory_loop() {
    float scaleValue = numLeds / (float)victoryThreshold;

  if (testObserver.hasStrips) {
    setup_registry();
    List<Strip> strips = registry.getStrips();

    if (strips.size() > 0) {
      for (Strip strip : strips) {
        for (int stripx = 0; stripx < numLeds; stripx++) {
          int cycle_pos = (stripx + victory_loop) % numLeds; 
          if (cycle_pos < (victoryThreshold * scaleValue * 0.25))
            strip.setPixel(blue, stripx);
          else if (cycle_pos < (victoryThreshold *scaleValue * 0.5))
            strip.setPixel(green, stripx);
          else if (cycle_pos < (victoryThreshold * scaleValue * 0.75))
            strip.setPixel(yellow, stripx);
          else
            strip.setPixel(red, stripx);
        }
      }
    }
  }
  victory_loop++;
  if (victory_loop > victoryMax) victory_loop=0;
}

void draw_fade(int value) {
  if (testObserver.hasStrips) {
    setup_registry();
    List<Strip> strips = registry.getStrips();

    color fade = color(value,0,0); //<>//
    if (strips.size() > 0) {
      for (Strip strip : strips) {
        for (int stripx = 0; stripx < numLeds; stripx++) {  
          strip.setPixel(fade, stripx);
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
