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

#include <Wire.h>

// This sketch needs the AccelStepper Library from
// http://www.airspayce.com/mikem/arduino/AccelStepper/
#include <MultiStepper.h>
#include <AccelStepper.h>

const int i2c_master          = 1;
const int i2c_slave           = 2;

const int endstop_pin         = 3;
const int endstop_invert      = 1;
const float home_speed        = 1000;
const float main_speed        = 6500.0 * 2;
const float accel             = 1500.0 * 4;

const long int total_steps    = 44200;
const long int touchoff_steps = total_steps / 100;

// TODO: Do this more efficiently with just one object bit twiddling twice
// instead of doing the math twice; this affects max step rate *significantly*
// if enabled.
//#define USE_SECOND_STEPPER

AccelStepper stepper_x(AccelStepper::DRIVER, 54, 55);

int readEndstop() { return digitalRead(endstop_pin) ^ endstop_invert; }

long int target = 0;
long int last_target = 0;
long int recvNumber = -1;
long int current_pos = -1;
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
}


// the callback fired when we receive new i2c commands
 void receiveCallback(int count) {
  while (Wire.available()) {
    int receivedValue  = Wire.read();
    Serial.print("i2c recv: ");
    Serial.println(receivedValue);
    if (receivedValue < 0) receivedValue = 0;
    if (receivedValue > 100) receivedValue = 100;
    target = receivedValue * total_steps / 100;
  }
}

void setup() {
  Serial.begin(115200);
  Serial.println("Waiting before homing...");

  // join the i2c bus
  Wire.begin(i2c_slave);
  Wire.onReceive(receiveCallback);

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
}


void loop() {
  if ((target != last_target) && !stepper_x.isRunning()) {
    Serial.print("Moving to: ");
    Serial.println(target);
    stepper_x.moveTo(target);
    stepper_x.enableOutputs();
#ifdef USE_SECOND_STEPPER
    stepper_y.moveTo(target);
    stepper_y.enableOutputs();
#endif
    last_target = target;
  }
  if (moving && !stepper_x.isRunning()) {
    Serial.println("Done moving.");
    moving = false;
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
