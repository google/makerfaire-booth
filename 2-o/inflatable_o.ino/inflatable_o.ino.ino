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

const int MIN_WINDOW_ADD_DELAY_MS = 200;
const int DEFLATE_TIME_MS = 1000;

const int STATE_IDLE = 0;
const int STATE_INFLATING = 1;
const int STATE_DEFLATING = 2;

const int THRESHOLD_LOW = -2;
const int THRESHOLD_HIGH = 2;

int values[WINDOW_SIZE];
int value_index = 0;

unsigned long last_value_at = 0;
unsigned long last_state_time = 0;

// TODO: check and reject long lines.
char line[10];
char *line_pos;

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
  Serial.begin(115200);
  for (int i = 0; i < WINDOW_SIZE; i++) {
    values[i] = THRESHOLD_LOW;
  }
}

void loop() {

  char *line = getLine();
  if (line != NULL) {
    int num = atoi(line);

    if (millis() - last_value_at > MIN_WINDOW_ADD_DELAY_MS) {
      // Add window values and process them.  
      values[value_index++] = num;
      if (value_index >= WINDOW_SIZE) {
        value_index = 0;
      }
      last_value_at = millis();
    }

    if (shouldInflate()) {
      setState(STATE_INFLATING);
    } else if (STATE == STATE_INFLATING) {
      setState(STATE_DEFLATING);
    }
  }

  // Change state if necessary.
  if (state == STATE_DEFLATING) {
    if (millis() - last_state_time > DEFLATE_TIME_MS) {
      setState(STATE_IDLE);
    }
  } 
}

bool shouldInflate() {
  int countMid = 0;
  for (int i = 0; i < WINDOW_SIZE; i++) {
    if (values[i] > THRESHOLD_LOW && values[i] < THRESHOLD_HIGH) {
      countMid++;
    }
  }
  return countMid > (WINDOW_SIZE - 2);
}

void setState(int newState) {
  if (state != newState) {
    state = newState;
    last_state_time = millis();

    Serial.print("new state: ");
    Serial.println(state);

    if (state == STATE_INFLATING) {
      // Start input motor
      
    } else if (state == STATE_DEFLATING) {
      // Start deflate motor
      
    } else if (state == STATE_IDLE) {
      // Go idle
      
    }
  }
}

