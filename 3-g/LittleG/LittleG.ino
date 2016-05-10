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

#include <Servo.h>  // We'll use the Arduino's built-in Servo library to control an ESC

//Configure the pins:
const int escPin = 10;
const int buttonPin = 11;
const int greenPin = 12;
const int redPin = 13;

// Setup variables:
const int motorOff = 700;  // Configure the timing command that corresponds to motor "stop" - on my ESC, it's 700 microseconds
int value = -1; // Set the initial read to negative 1, which prevents the ESC from arming
int buttonState = 0; // Set the initial button state to zero
int lastButtonState = 0; // Set the last button state to zero
int motorArm = 0; // Set the motor arm state to zero
Servo esc; // Create a servo object to address as "esc"

// Setup to read from serial, using the same code from letter 'L'
char line[10];
char *line_pos;

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
  esc.attach(escPin); // Attach the esc to the escPin
  pinMode(buttonPin, INPUT_PULLUP); // Set button mode to use internal pullup (no resistors needed!)
  pinMode(greenPin, OUTPUT); // Set greenPin to output for green LED
  pinMode(redPin, OUTPUT); // Set redPin to output for red LED
  Serial.begin(9600); // Start serial at 9600 baud for input from phone
  esc.writeMicroseconds(motorOff); // Write the "motorOff" value to the ESC, since the ESC needs to receive a throttle command of "off" as soon as it boots
  digitalWrite(redPin, HIGH);  // Turn on the red LED to indicate that we're ready with the motor off
}

// Note: Now that the setup() commands have completed and the Arduino is sending a "motorOff" command, it's now okay to manually power on the ESC

void loop() {
  char *line = getLine();
  if (line != NULL) {
    int num = atoi(line);
    if (num < 0) num = 0;
    if (num > 100) num = 100;
    
    if (motorArm == 1) { // If the motor state is 1 or "armed":
      int value = map(num, 1, 100, 1200, 1400); // Map the value from serial to a throttle value the ESC understands - my motor runs well from 1200-1400
      value = constrain(value, 1200, 1400); // Constrain the throttle to 1200-1400 range, just in case
      if (num == 0) value = motorOff;  // Special case: if the value is zero, use the "off" value instead
      esc.writeMicroseconds(value); // Write the mapped value to the ESC as a throttle command
    }
  } 
    
  buttonState = digitalRead(buttonPin); // Read the button input pin
  if (buttonState == LOW && lastButtonState == HIGH) { // Compare the pin to its previous state to determine if it's been pressed
    delay(1);
    if (motorArm == 0) {  // If motorArm is currently 0, then light up green and set the new motorArm value to 1, ready for input
      digitalWrite(greenPin, HIGH);
      digitalWrite(redPin, LOW);
      motorArm = 1;
    } else {  // If motorArm is currently 1, then light up red and set the new motorArm value to 0
      digitalWrite(greenPin, LOW);
      digitalWrite(redPin, HIGH);
      esc.writeMicroseconds(motorOff); // Also write the "motorOff" value to the ESC, which turns the motor off.
      motorArm = 0;
    }
  }
  lastButtonState = buttonState; // Save the current state as the last state before repeating  
}
