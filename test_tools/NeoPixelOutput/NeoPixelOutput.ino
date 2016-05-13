/*
Copyright 2015 Google Inc. All Rights Reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
*/

#include <Adafruit_NeoPixel.h>

#define LEDPIN 6
#define NUM_PIXELS 40

Adafruit_NeoPixel strip = Adafruit_NeoPixel(NUM_PIXELS, LEDPIN, NEO_GRB + NEO_KHZ800);

int red = 255;
int blue = 255;
int green = 255;
int brightness = 30;
String accum;

void draw() {
  bool pixel = 0;
  strip.setBrightness(brightness);
 
  for (uint64_t i = 0; i < NUM_PIXELS; i++) {
      strip.setPixelColor(i, strip.Color(red, green, blue));
  }
  strip.show();
}


void setup() {
  Serial.begin(115200);

  accum.reserve(200);
  strip.begin();
  draw();
}

void loop() {
  while (Serial.available()) {
    int ret = Serial.read();
    if (ret == -1) break;
    char c = char(ret);
    if (c == '\r') {
      if (accum[0] == 'V') {
        Serial.println("ArduinoNeoPixelShutter");
      } else {
        int val = accum.substring(1).toInt();
        if (val < 0) val = 0;
        if (val > 99) val = 99;
        brightness = val * 2;
      }
      accum = "";
    } else {
      accum += char(ret);
    }
  }
  draw();
}
