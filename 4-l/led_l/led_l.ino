/*
 *  Copyright 2016 Google Inc. All Rights Reserved.
 *
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 *  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 *  See the License for the specific language governing permissions and
 *  limitations under the License.
 */

// This sketch needs NeoPixelStripAnimator
// https://github.com/urtubia/NeoPixelStripAnimator
#include <Adafruit_NeoPixel.h>
#include <NeoPixelStripAnimator.h>

const int led_pin              = 13;    // pin number for the leds
const int num_leds             = 60;    // numbetr of LEDs in the strip

const int STATE_RESETTING      = 0;     // System is resetting, no input accepted.
const int STATE_IDLE           = 1;     // System is idle, input is accepted to start a window.
const int STATE_DATA_INPUT     = 2;     // System is receiving data for a bit.
const int STATE_DISPLAYING     = 3;     // Input received, system is moving to show the output
const int DATA_INPUT_WINDOW_MS = 1000;  // Number of MS to leave the data input window open.
const int DISPLAY_WINDOW_MS    = 10000; // Number of MS to display window.

// initialize the LED strip
Adafruit_NeoPixel strip = Adafruit_NeoPixel(num_leds, led_pin, NEO_GRB + NEO_KHZ800);
NeoPixelStripAnimator neoPixelStripAnimator(&strip);

int state = STATE_RESETTING;
long int target = 0;
long int last_target = 0;
long last_state_time = -1;
long completed_move = -1;
bool moving;

// TODO: check and reject long lines.
char line[10];
char *line_pos;

// read a line of input from the serial interface
char *getLine() {
  while (Serial.available() > 0) {
    // NOTE: You need to specify a line ending or arduino ide doesn't send CR
    // or LF.  TODO: Support either, and ignore blank lines.
    char ch = Serial.read();
    if (ch == '\n') {
      *line_pos = '\0';
      line_pos = line;
      return line;
    } else if (ch == '\r') {
      return NULL;  // ignore
    } else {
      *line_pos++ = ch;
      return NULL;
    }
  }
}


/////////////////////////////////////////////////////////////////////////////
// Our animation class
/////////////////////////////////////////////////////////////////////////////
class HammerHitAnimation : public INeoPixelAnimation {
  public:
    HammerHitAnimation(uint32_t color, int pixelInterval, int percentage);
    virtual void loop();
    virtual bool isDone();
    virtual void setup(Adafruit_NeoPixel *strip);

  private:
    unsigned long _lastTimeCheck;
    unsigned long _pixelInterval;
    unsigned long _percentage;
    Adafruit_NeoPixel *_strip;
    bool _done;
    unsigned int _currentPixel;
    uint32_t _color;

};

HammerHitAnimation::HammerHitAnimation(uint32_t color, int pixelInterval, int percentage) {
  _lastTimeCheck = millis();
  _done = false;
  _currentPixel = -1;
  _pixelInterval = pixelInterval;
  _percentage = percentage;
  _color = color;
}

void HammerHitAnimation::setup(Adafruit_NeoPixel *strip) {
  _strip = strip;
  // set the brightness for all pixels in the strip
  for(int i = 0; i < _strip->numPixels();i++) {
    _strip->setBrightness(255);
  }

}

void HammerHitAnimation::loop() {
  if(_done) return;
  unsigned long now = millis();

  // the number pixels for this run
  unsigned long _num_pixels = (unsigned long)(_strip->numPixels() * (_percentage / 100.0));

  if((now - _lastTimeCheck) > _pixelInterval) {
    _currentPixel++;
    if(_currentPixel >= _num_pixels) {
      _done = true;
      return;
    }
    _strip->setPixelColor(_currentPixel, _color);
    _strip->show();
    _lastTimeCheck = now;
  }
}

bool HammerHitAnimation::isDone() {
  return _done;
}
/////////////////////////////////////////////////////////////////////////////

void setup() {
  Serial.begin(115200);
  Serial.println("Waiting...");
  delay(200);
  line_pos = line;

  neoPixelStripAnimator.setup();
  setState(STATE_RESETTING);
  delay(200);
  setState(STATE_IDLE);
}


void loop() {
  long int potential_target = 0;
  char *line = getLine();
  if (line != NULL) {
    Serial.print("Read line: ");
    Serial.println(line);

    int num = atoi(line);
    if (num < 0) num = 0;
    if (num > 100) num = 100;

    if (state == STATE_IDLE) {
      target = num;
      setState(STATE_DATA_INPUT);
    }
  }

  if (state == STATE_DATA_INPUT) {
    if (potential_target > target) {
      target = potential_target;
    }
    if (millis() - last_state_time > DATA_INPUT_WINDOW_MS) {
      setState(STATE_DISPLAYING);
    }
  }

  if ((state == STATE_DISPLAYING || state == STATE_RESETTING) && (target != last_target)) {
    completed_move = -1;

    Serial.print("Moving to: ");
    Serial.println(target);
    moving = true;
    last_target = target;
  }

  if (state == STATE_DISPLAYING && millis() - completed_move > DISPLAY_WINDOW_MS && completed_move != -1) {
    setState(STATE_RESETTING);
  }

  if (moving) {
    Serial.println("Done moving.");
    completed_move = millis();
    moving = false;
    if (state == STATE_RESETTING) {
      setState(STATE_IDLE);
    }
  }

  neoPixelStripAnimator.loop();
}

void setState(int newState) {
  int oldState = state;
  if (state != newState) {
    state = newState;
    last_state_time = millis();
    Serial.print("New state: ");
    Serial.println(state);
    // Now process based on new state.
    if (state == STATE_IDLE) {
      startIdleLedAnimation();
    } else if (state == STATE_DATA_INPUT) {
      Serial.println("Data input window open");
      last_target = -1;
      startDataInputLedAnimation();
    } else if (state == STATE_DISPLAYING) {
      startMovingLedAnimation();
    } else if (state == STATE_RESETTING) {
      target = 0;
      startResettingLedAnimation();
    }
  }
}

void startIdleLedAnimation() {
  Serial.println("start animation");
  neoPixelStripAnimator.startAnimation(new NightRiderAnimation(Adafruit_NeoPixel::Color(0,255,0), 20));
}

void startDataInputLedAnimation() {
  Serial.println("input animation");
  neoPixelStripAnimator.clear();
}

void startMovingLedAnimation() {
  Serial.println("moving animation");
  neoPixelStripAnimator.startAnimation(new HammerHitAnimation(Adafruit_NeoPixel::Color(0,255,0), 100, 50));
}

void startResettingLedAnimation() {
  neoPixelStripAnimator.clear();
}

