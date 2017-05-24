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
int brightness = 255;
int val = 20;
String accum;

void draw() {
  bool pixel = 0;
 
  for (uint64_t i = 0; i < NUM_PIXELS; i++) {
      if (i < val)
        strip.setPixelColor(i, strip.Color(red, green, blue));
      else
        strip.setPixelColor(i, strip.Color(0, 0, 0));
  }
  strip.show();
}


void setup() {
  Serial.begin(115200);

  accum.reserve(200);
  strip.begin();
  strip.setBrightness(brightness);
  draw();
}

void loop() {
  while (Serial.available()) {
    int ret = Serial.read();
    if (ret == -1) break;
    char c = char(ret);
    if (c == '\r') {
        int tmp = accum.substring(1).toInt();
        if (tmp < 0) tmp = 0;
        if (tmp > 99) tmp = 99;
        val = tmp / 2.5;
        accum = "";
    } else {
      accum += char(ret);
    }
  }
  draw();
}
