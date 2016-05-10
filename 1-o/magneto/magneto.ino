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
 
#include "TimerOne.h"

#define PULSE_PIN 9
#define DIR_PIN 4
#define ENABLE_PIN 7

#define DIR_CW LOW
#define DIR_CCW HIGH

#define KICK_INTERVAL 15000

#define LOW_SPEED 8000
#define HIGH_SPEED 3600

int currentDir = DIR_CW;
int currentSpeed = 0;
unsigned long time;

void disengage()
{
  digitalWrite(ENABLE_PIN, LOW);
  Serial.println("Motor disengaged");
}

void engage()
{
  digitalWrite(ENABLE_PIN, HIGH);
  Serial.println("Motor engaged");
}

void setDirection(int dir)
{
  Serial.print("Set direction to ");
  Serial.println(dir == DIR_CW ? "CW" : "CCW");
  digitalWrite(DIR_PIN, dir);
  currentDir = dir;
}

void flip()
{
  int newDir = currentDir == DIR_CW ? DIR_CCW : DIR_CW;
  setDirection(newDir);
}

void setSpeed(int speed)
{
  Timer1.setPeriod(speed);
  if (speed == 0) {
    disengage();
  }
  else {
    engage();
  }
  Serial.print("Set speed to ");
  Serial.println(speed);
  currentSpeed = speed;
}

void setSpeedPercent(int pct)
{
  if (pct == 0) {
    setSpeed(0);
  }
  else {
    setSpeed(map(pct, 1, 100, LOW_SPEED, HIGH_SPEED));
  }
}

void kick()
{
  disengage();
  delay(100);

  Timer1.setPeriod(0);
  engage();
  delay(100);

  flip();
  Timer1.setPeriod(7000);
  delay(250);

  Timer1.setPeriod(0);
  delay(100);

  flip();
  Timer1.setPeriod(7000);
  delay(250);

  Timer1.setPeriod(0);
  delay(100);

  flip();
  Timer1.setPeriod(7000);
  delay(250);

  // ramp up
  Timer1.setPeriod(6000);
  delay(100);
  Timer1.setPeriod(5000);

  setSpeed(currentSpeed);
}

void setup()
{
  pinMode(DIR_PIN, OUTPUT);
  pinMode(ENABLE_PIN, OUTPUT);
  
  time = millis();

  engage();

  Serial.begin(9600);
  while (! Serial);

  Timer1.initialize(7000);
  Timer1.pwm(9, 512);

  kick();

  Serial.println("Ready for commands");
}


void loop()
{
  if (Serial.available())
  {
    String str = Serial.readStringUntil('\n');
    str.trim();
    if (str.length() > 0 && isDigit(str.charAt(0))) {
      int speedPct = str.toInt();
      if (speedPct >= 0 && speedPct <= 100) {
        Serial.print("Speed command ");
        Serial.println(speedPct);
        setSpeedPercent(speedPct);
      }
      else {
        Serial.println("Did not read expected 0-100");
      }
    }
    else if (str == "k")
    {
      Serial.println("Kick");
      kick();
    }
    else if (str == "f")
    {
      Serial.println("Flip direction");
      flip();
    }
    else if (str == "off")
    {
      disengage();
    }
    else if (str == "on")
    {
      engage();
    }
  }
  
  unsigned long now = millis();
  if (now < time || now > time + KICK_INTERVAL) {
    kick();
    time = millis();
  }
}
