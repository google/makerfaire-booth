#include <Keyboard.h>
int buttonZPin = 2;  // Set a button to any pin
int buttonXPin = 3;  // Set a button to any pin
int buttonRPin = 4;  // Set a button to any pin
int buttonPPin = 5;  // Set a button to any pin


void setup()
{
  pinMode(buttonZPin, INPUT);  // Set the button as an input
  digitalWrite(buttonZPin, HIGH);  // Pull the button high
  pinMode(buttonXPin, INPUT);  // Set the button as an input
  digitalWrite(buttonXPin, HIGH);  // Pull the button high
  pinMode(buttonRPin, INPUT);  // Set the button as an input
  digitalWrite(buttonRPin, HIGH);  // Pull the button high
  pinMode(buttonPPin, INPUT);  // Set the button as an input
  digitalWrite(buttonPPin, HIGH);  // Pull the button high
}

void loop()
{  
  if (digitalRead(buttonZPin) == 0)  // if the button goes low
  {
    Keyboard.write('z');  // send a 'z' to the computer via Keyboard HID
    delay(1000);  // delay so there aren't a kajillion z's
  }
  if (digitalRead(buttonXPin) == 0)  // if the button goes low
  {
    Keyboard.write('x');  // send a 'x' to the computer via Keyboard HID
    delay(1000);  // delay so there aren't a kajillion x's
  }
  if (digitalRead(buttonRPin) == 0)  // if the button goes low
  {
    Keyboard.write('r');  // send a 'r' to the computer via Keyboard HID
    delay(1000);  // delay so there aren't a kajillion r's
  }
  if (digitalRead(buttonPPin) == 0)  // if the button goes low
  {
    Keyboard.write('p');  // send a 'p' to the computer via Keyboard HID
    delay(1000);  // delay so there aren't a kajillion p's
  }
}

