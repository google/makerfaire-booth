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

#define VALVE_PIN 6
#define LED_PIN 13
#define MIN_HEIGHT_DELAY 30
#define MAX_HEIGHT_DELAY 130

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


void setup() {
  Serial.begin(115200);
  Serial.println("Waiting...");
  line_pos = line;
  pinMode(VALVE_PIN, OUTPUT);
  pinMode(LED_PIN, OUTPUT);
}


void loop() {
  char *line = getLine();
  if (line != NULL) {
    Serial.print("Read line: ");
    Serial.println(line);

    int num = atoi(line);
    if (num < 0) num = 0;
    if (num > 100) num = 100;

    int d = map(num, 0, 100, MIN_HEIGHT_DELAY, MAX_HEIGHT_DELAY);
    Serial.print("Launch ");
    Serial.print(num);
    Serial.print(" for ");
    Serial.print(d);
    Serial.println("ms");

    digitalWrite(VALVE_PIN, HIGH);
    digitalWrite(LED_PIN, HIGH);
    delay(d);
    digitalWrite(VALVE_PIN, LOW);
    digitalWrite(LED_PIN, LOW);
    delay(200); // let the ball fall!
  }
}
