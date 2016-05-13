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

// This sketch needs the AccelStepper Library from
// http://www.airspayce.com/mikem/arduino/AccelStepper/
#include <MultiStepper.h>
#include <AccelStepper.h>

const int endstop_pin = 3;
const int endstop_invert = 1;
const float home_speed = 1000;
const float main_speed = 6000.0 * 2;
const float accel = 1000.0 * 4;

const long int total_steps = 9900 * 2;
const long int touchoff_steps = total_steps / 100;

// System is resetting, no input accepted.
const int STATE_RESETTING = 0;
// System is idle, input is accepted to start a window.
const int STATE_IDLE = 1;
// System is receiving data for a bit.
const int STATE_DATA_INPUT = 2;
// Input received, system is moving to show the output
const int STATE_DISPLAYING = 3;

// Number of MS to leave the data input window open.
const int DATA_INPUT_WINDOW_MS = 1000;

// Number of MS to display window.
const int DISPLAY_WINDOW_MS = 3000;

// TODO: Do this more efficiently with just one object bit twiddling twice
// instead of doing the math twice; this affects max step rate *significantly*
// if enabled.
//#define USE_SECOND_STEPPER

AccelStepper stepper_x(AccelStepper::DRIVER, 54, 55);
#ifdef USE_SECOND_STEPPER
AccelStepper stepper_y(AccelStepper::DRIVER, 60, 61);
#endif

int readEndstop() { return digitalRead(endstop_pin) ^ endstop_invert; }

int state = STATE_RESETTING;

long int target = 0;
long int last_target = 0;
long last_state_time = -1;
bool moving;

/* This doesn't totally work for stopping immediately!  Note the run loop. */
void stop() {
  if (stepper_x.isRunning()) {
    stepper_x.stop();
#ifdef USE_SECOND_STEPPER
    stepper_y.stop();
#endif
    while (stepper_x.isRunning()) {
      stepper_x.run();
#ifdef USE_SECOND_STEPPER
      stepper_y.run();
#endif
    }
  }
}

void goHome() {
  setState(STATE_RESETTING);
  Serial.println("Starting home.");
  stop();
  stepper_x.setMaxSpeed(home_speed);
  stepper_x.enableOutputs();
  stepper_x.moveTo(-total_steps * 2);
#ifdef USE_SECOND_STEPPER
  stepper_y.setMaxSpeed(home_speed);
  stepper_y.enableOutputs();
  stepper_y.moveTo(-total_steps * 2);
#endif
  Serial.println("2");
  while (!readEndstop() && stepper_x.isRunning()) {
    stepper_x.run();
#ifdef USE_SECOND_STEPPER
    stepper_y.run();
#endif
  }

  Serial.println("3");
  // side effect: sets speed to 0, getting ready for a direction change.
  stepper_x.setCurrentPosition(0);
#ifdef USE_SECOND_STEPPER
  stepper_y.setCurrentPosition(0);
#endif

  // Touch off
  stepper_x.moveTo(total_steps);
#ifdef USE_SECOND_STEPPER
  stepper_y.moveTo(total_steps);
#endif
  while (readEndstop() && stepper_x.isRunning()) {
    stepper_x.run();
#ifdef USE_SECOND_STEPPER
    stepper_y.run();
#endif
  }
  stepper_x.moveTo(touchoff_steps);
#ifdef USE_SECOND_STEPPER
  stepper_y.moveTo(touchoff_steps);
#endif
  while (stepper_x.isRunning()) {
    stepper_x.run();
#ifdef USE_SECOND_STEPPER
    stepper_y.run();
#endif
  }
  Serial.println("4");

  stepper_x.setCurrentPosition(0);
  stepper_x.setMaxSpeed(main_speed);
#ifdef USE_SECOND_STEPPER
  stepper_y.setCurrentPosition(0);
  stepper_y.setMaxSpeed(main_speed);
#endif
  Serial.println("Homed.");
  moving = false;
  setState(STATE_IDLE);
}

// TODO: check and reject long lines.
char line[10];
char *line_pos;

void setup() {
  Serial.begin(115200);
  Serial.println("Waiting before homing...");
  delay(200);
  stepper_x.setAcceleration(accel);
  stepper_x.setEnablePin(38);
  stepper_x.setPinsInverted(true, false, true);
  stepper_x.setMinPulseWidth(0);
#ifdef USE_SECOND_STEPPER
  stepper_y.setAcceleration(accel);
  stepper_y.setEnablePin(56);
  stepper_y.setPinsInverted(true, false, true);
  stepper_y.setMinPulseWidth(0);
#endif

  pinMode(endstop_pin, INPUT);
  digitalWrite(endstop_pin, HIGH);

  goHome();
  line_pos = line;
}

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

void loop() {
  int potential_target = 0;
  char *line = getLine();
  if (line != NULL) {
    Serial.print("Read line: ");
    Serial.println(line);
    if (*line == 'x') {
      Serial.print("Endstop status: ");
      Serial.println(readEndstop());
      return;
    } else if (*line == 'h') {
      goHome();
      return;
    }

    int num = atoi(line);
    if (num < 0) num = 0;
    if (num > 100) num = 100;
    potential_target = num * total_steps / 100;
    if (state == STATE_IDLE) {
      target = potential_target;
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
  
  if ((state == STATE_DISPLAYING || state == STATE_RESETTING)
      && (target != last_target) && !stepper_x.isRunning()) {
    Serial.print("Moving to: ");
    Serial.println(target);
    moving = true;
    stepper_x.moveTo(target);
    stepper_x.enableOutputs();
#ifdef USE_SECOND_STEPPER
    stepper_y.moveTo(target);
    stepper_y.enableOutputs();
#endif
    last_target = target;
  }

  if (state == STATE_DISPLAYING && millis() - last_state_time > DISPLAY_WINDOW_MS) {
    setState(STATE_RESETTING);
  }
  
  if (moving && !stepper_x.isRunning()) {
    // If you want to save power between moves, uncomment.
    /*stepper_x.disableOutputs();
    stepper_y.disableOutputs();
    */
    Serial.println("Done moving.");
    moving = false;
    if (state == STATE_RESETTING) {
      setState(STATE_IDLE);
    }
  }

  stepper_x.run();
#ifdef USE_SECOND_STEPPER
  stepper_y.run();
#endif
  if (readEndstop()) {
    // TODO: recover more gracefully
    Serial.println("endstop triggered! Press reset.");
    while (1) delay(100);
  }
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
}

void startDataInputLedAnimation() {
}

void startMovingLedAnimation() {
}

void startResettingLedAnimation() {
}

