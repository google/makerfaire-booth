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

const float home_speed        = 1000;
const float main_speed        = 1000.0 * 4;
const float accel             = 500;
const float full_rotation     = 200 * 4;

AccelStepper stepper_x(AccelStepper::DRIVER, 9, 4);


long int current_degree = 0;
long int target = 0;
long int last_target = 0;
long int recvNumber = -1;
long int current_pos = -1;
bool moving;

/* This doesn't totally work for stopping immediately!  Note the run loop. */
void stop() {
  if (stepper_x.isRunning()) {
    stepper_x.stop();
    while (stepper_x.isRunning()) {
      stepper_x.run();
    }
  }
}

void setup() {
  Serial.begin(115200);
  stepper_x.setAcceleration(accel);
  stepper_x.setEnablePin(7);
  stepper_x.setPinsInverted(false, false, false);
  stepper_x.setMinPulseWidth(0);
  Serial.println("Woot!");
  moving = false;
}


void loop() {
  if (Serial.available()) {
      String str = Serial.readStringUntil('\n');
      str.trim();
      if (str.length() > 0 && isDigit(str.charAt(0))) {
	int targetDegrees = str.toInt();
	if (targetDegrees >= 0 && targetDegrees <= 360) {
	  Serial.print("Target angle ");
	  Serial.println(targetDegrees);
    current_degree += (360.0 / targetDegrees);
	  target = (full_rotation / 360.) * targetDegrees;
	}
	else {
	  Serial.println("Did not read expected 0-360");
	}

      }
    }
  if ((target != last_target) && !stepper_x.isRunning()) {
    Serial.print("Moving to: ");
    Serial.println(current_degree);
    Serial.print("Number of Steps: ");
    Serial.println(target);
    moving = true;
    stepper_x.moveTo(target);
    last_target = target;
  }
  if (moving && !stepper_x.isRunning()) {
    Serial.println("Done moving.");
    moving = false;
  }

  stepper_x.run();
  stepper_x.enableOutputs();
}
