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

// Puts input into a window. If the majority of window values
// are between LOW and HIGH, then inflate. Otherwise, deflate.

const int WINDOW_SIZE = 10;

const int STATE_IDLE = 0;
const int STATE_INFLATING = 1;
const int STATE_DEFLATING = 2;

int[] values = new int[WINDOW_SIZE];
int value_index = 0;

int state = STATE_IDLE;

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
}

void loop() {
  char *line = getLine();
  if (line != NULL) {
    int num = atoi(line);
    if (num < 0) num = 0;
    if (num > 100) num = 100;
  }

  // Add window values and process them.
  
  // Change state if necessary.
   
}

void setState(newState) {
  if (state != newState) {
    state = newState;
  }
}

