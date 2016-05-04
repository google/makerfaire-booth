#include <SoftwareSerial.h>

//#define _DEBUG

// This is our physical panel configuration
#define PANEL_ROWS 7
#define PANEL_COLUMNS 28
#define PANELS 4

// This is the first and last rows that have any pixels set in letterMap, needed to scale SENSOR_MAX to the top row, not above it
// and SENSOR_MIN to the bottom row not below it
#define BASE_ROW 3
#define LAST_ROW 24

const int ROWS = PANEL_ROWS * PANELS;
const int LETTER_ROWS = LAST_ROW+1 - BASE_ROW;
const int COLUMNS = PANEL_COLUMNS;

// These define the range of expected sensor values
#define SENSOR_MIN 0
#define SENSOR_MAX 99
float y_scaling_factor;

// between 0 and 99, the "percentage" of attract mode pixels to turn on
#define ATTRACT_MODE_DENSITY 40

// The pins and BAUD rate to use for the RS485 port
#define RS485_TX 3
#define RS485_RX 2
#define RS485_BAUD 9600
SoftwareSerial panelPort(RS485_RX, RS485_TX);

unsigned long int nextRefreshAt, lastRefreshedAt, lastUpdatedAt, idleAt;

bool letterMap[COLUMNS][ROWS];

// The maximum number of refreshes per second - be careful, the panels can only handle so many refreshes in so much time
#define TARGET_REFRESH_HZ 4
const int REFRESH_FREQUENCY_MS = (1/ TARGET_REFRESH_HZ)*1000;

// Elapsed time after the last sensor update before we go to attract mode
#define IDLE_TIMEOUT_MS 9000

// Details of the flipdots panel protocol
const byte PANEL_HEADER = 0x80u;
const byte  PANEL_WRITE_CMD = 0x84u;
const byte  PANEL_REFRESH_CMD = 0x82u;
const byte  PANEL_END = 0x8Fu;
const int MESSAGE_MAX_SIZE = 4+(PANEL_COLUMNS);

// Track the high watermark for sensor values and expire them after a period of time
int sensorHighWatermark;
unsigned long int highWaterMarkAt;
#define SENSOR_HIGHWATERMARK_TIMEOUT_MS 5000

void refreshDisplay() {
  byte displayMessage[3];
  int messageIndex = 0;
  displayMessage[messageIndex++] = PANEL_HEADER;
  displayMessage[messageIndex++] = PANEL_REFRESH_CMD;
  displayMessage[messageIndex++] =  PANEL_END;
  writeToPanel(displayMessage, messageIndex);
}

byte panelAddress(const int panelIdx) {
  return byte(panelIdx);
}

bool getDot(const bool idle, const int x, const int y) {
  bool letterPixel = letterMap[x][y];
  if (idle == true) {
    if (letterPixel) {
      letterPixel = false;
    } else {
      letterPixel = (random(0,100) < ATTRACT_MODE_DENSITY?true:false);
    }
  }
  return letterPixel;
}

int rowForSensorValue(const int sensorValue) {
  return (LAST_ROW+1) - ((sensorValue==0)?0:int(sensorValue * y_scaling_factor + 1));
}

// Scale the sensor value to the row, flip the orientation as needed.
// Return true if this row should be visible for the current sensorValue
bool showRow(const int row, const int sensorValue) {
  bool visible = (row >= rowForSensorValue(sensorValue));
  return visible;
}

// Put the current message set for setting all panels' dots into displayMessage
// and call writeToPanel to output the message set
void setDisplay(const bool isIdle, const int sensorValue) {
  byte displayMessage[MESSAGE_MAX_SIZE];
  int messageIndex;

  for (int p = 0; p < PANELS; p++) {
    messageIndex = 0;
    displayMessage[messageIndex++] = PANEL_HEADER;
    displayMessage[messageIndex++] = PANEL_WRITE_CMD;
    displayMessage[messageIndex++] = panelAddress(p);
    int currentHWM = currentHighWatermark();
    int hwmRow = rowForSensorValue(currentHWM);
    for (int x = 0; x < PANEL_COLUMNS; x++) {
      byte val = 0x00;
      for (int y = 0; y < PANEL_ROWS; y++) {
        int displayRow = y+(p*PANEL_ROWS);
        // idle == attract mode ignores the sensor and high watermark values
        if (isIdle || showRow(displayRow, sensorValue) || (currentHWM > 0 && (displayRow == hwmRow))) {
          if (getDot(isIdle, x, displayRow)) {
            val = val | (1 << (y+1) - 1);
          }
        }
      }
      displayMessage[messageIndex++] = byte(val);
    }
    displayMessage[messageIndex++] = PANEL_END;
    writeToPanel(displayMessage, messageIndex);
  }
}

void writeToPanel(byte message[], const int messageLength) {
  #ifdef _DEBUG
  Serial.print("message:");
  Serial.println(messageLength);
  int msgPos;
  for (msgPos=0; msgPos < sizeof(PANEL_END)+sizeof(PANEL_WRITE_CMD)+sizeof(byte);msgPos++) {
    Serial.print(message[msgPos], HEX);
  }
  Serial.println();
  int msgBodyStart = msgPos;
  for (int i=0;i<PANEL_ROWS;i++) {
    Serial.print('\t');
    msgPos = msgBodyStart;
    for (;msgPos<messageLength-sizeof(PANEL_END); msgPos++) {
      Serial.print(((message[msgPos] >> i) & 1)?"O":" ");
    }
    Serial.println();
  }
  for (;msgPos<messageLength; msgPos++) {
    Serial.print(message[msgPos],HEX);
  }
  Serial.println();
  #else
  panelPort.write(message, messageLength);
  #endif
}

// Set each pixel of the letter map to one value
void _initLetterMap(const bool val) {
  // Set all dots off
  for (int x = 0; x < COLUMNS; x++) {
    for (int y = 0; y < ROWS; y++) {
      letterMap[x][y] = val;
    }
  }
}

// Set the letter map
void setLetterMap(const bool pixelVal) {
  _initLetterMap(false);
  // Set the dots of an 'e' on
  letterMap[3][11] = pixelVal;
  letterMap[3][12] = pixelVal;
  letterMap[3][13] = pixelVal;
  letterMap[3][14] = pixelVal;
  letterMap[3][15] = pixelVal;
  letterMap[3][16] = pixelVal;
  letterMap[3][17] = pixelVal;
  letterMap[4][9] = pixelVal;
  letterMap[4][10] = pixelVal;
  letterMap[4][11] = pixelVal;
  letterMap[4][12] = pixelVal;
  letterMap[4][13] = pixelVal;
  letterMap[4][14] = pixelVal;
  letterMap[4][15] = pixelVal;
  letterMap[4][16] = pixelVal;
  letterMap[4][17] = pixelVal;
  letterMap[4][18] = pixelVal;
  letterMap[4][19] = pixelVal;
  letterMap[5][7] = pixelVal;
  letterMap[5][8] = pixelVal;
  letterMap[5][9] = pixelVal;
  letterMap[5][10] = pixelVal;
  letterMap[5][11] = pixelVal;
  letterMap[5][12] = pixelVal;
  letterMap[5][13] = pixelVal;
  letterMap[5][14] = pixelVal;
  letterMap[5][15] = pixelVal;
  letterMap[5][16] = pixelVal;
  letterMap[5][17] = pixelVal;
  letterMap[5][18] = pixelVal;
  letterMap[5][19] = pixelVal;
  letterMap[5][20] = pixelVal;
  letterMap[6][6] = pixelVal;
  letterMap[6][7] = pixelVal;
  letterMap[6][8] = pixelVal;
  letterMap[6][9] = pixelVal;
  letterMap[6][10] = pixelVal;
  letterMap[6][11] = pixelVal;
  letterMap[6][12] = pixelVal;
  letterMap[6][13] = pixelVal;
  letterMap[6][14] = pixelVal;
  letterMap[6][15] = pixelVal;
  letterMap[6][16] = pixelVal;
  letterMap[6][17] = pixelVal;
  letterMap[6][18] = pixelVal;
  letterMap[6][19] = pixelVal;
  letterMap[6][20] = pixelVal;
  letterMap[6][21] = pixelVal;
  letterMap[7][5] = pixelVal;
  letterMap[7][6] = pixelVal;
  letterMap[7][7] = pixelVal;
  letterMap[7][8] = pixelVal;
  letterMap[7][9] = pixelVal;
  letterMap[7][10] = pixelVal;
  letterMap[7][11] = pixelVal;
  letterMap[7][12] = pixelVal;
  letterMap[7][13] = pixelVal;
  letterMap[7][14] = pixelVal;
  letterMap[7][15] = pixelVal;
  letterMap[7][16] = pixelVal;
  letterMap[7][17] = pixelVal;
  letterMap[7][18] = pixelVal;
  letterMap[7][19] = pixelVal;
  letterMap[7][20] = pixelVal;
  letterMap[7][21] = pixelVal;
  letterMap[7][22] = pixelVal;
  letterMap[8][4] = pixelVal;
  letterMap[8][5] = pixelVal;
  letterMap[8][6] = pixelVal;
  letterMap[8][7] = pixelVal;
  letterMap[8][8] = pixelVal;
  letterMap[8][9] = pixelVal;
  letterMap[8][10] = pixelVal;
  letterMap[8][11] = pixelVal;
  letterMap[8][12] = pixelVal;
  letterMap[8][13] = pixelVal;
  letterMap[8][14] = pixelVal;
  letterMap[8][15] = pixelVal;
  letterMap[8][16] = pixelVal;
  letterMap[8][17] = pixelVal;
  letterMap[8][18] = pixelVal;
  letterMap[8][19] = pixelVal;
  letterMap[8][20] = pixelVal;
  letterMap[8][21] = pixelVal;
  letterMap[8][22] = pixelVal;
  letterMap[8][23] = pixelVal;
  letterMap[9][3] = pixelVal;
  letterMap[9][4] = pixelVal;
  letterMap[9][5] = pixelVal;
  letterMap[9][6] = pixelVal;
  letterMap[9][7] = pixelVal;
  letterMap[9][8] = pixelVal;
  letterMap[9][9] = pixelVal;
  letterMap[9][13] = pixelVal;
  letterMap[9][14] = pixelVal;
  letterMap[9][15] = pixelVal;
  letterMap[9][16] = pixelVal;
  letterMap[9][17] = pixelVal;
  letterMap[9][18] = pixelVal;
  letterMap[9][19] = pixelVal;
  letterMap[9][20] = pixelVal;
  letterMap[9][21] = pixelVal;
  letterMap[9][22] = pixelVal;
  letterMap[9][23] = pixelVal;
  letterMap[9][24] = pixelVal;
  letterMap[10][3] = pixelVal;
  letterMap[10][4] = pixelVal;
  letterMap[10][5] = pixelVal;
  letterMap[10][6] = pixelVal;
  letterMap[10][7] = pixelVal;
  letterMap[10][8] = pixelVal;
  letterMap[10][13] = pixelVal;
  letterMap[10][14] = pixelVal;
  letterMap[10][15] = pixelVal;
  letterMap[10][16] = pixelVal;
  letterMap[10][17] = pixelVal;
  letterMap[10][18] = pixelVal;
  letterMap[10][19] = pixelVal;
  letterMap[10][20] = pixelVal;
  letterMap[10][21] = pixelVal;
  letterMap[10][22] = pixelVal;
  letterMap[10][23] = pixelVal;
  letterMap[10][24] = pixelVal;
  letterMap[11][2] = pixelVal;
  letterMap[11][3] = pixelVal;
  letterMap[11][4] = pixelVal;
  letterMap[11][5] = pixelVal;
  letterMap[11][6] = pixelVal;
  letterMap[11][7] = pixelVal;
  letterMap[11][13] = pixelVal;
  letterMap[11][14] = pixelVal;
  letterMap[11][15] = pixelVal;
  letterMap[11][16] = pixelVal;
  letterMap[11][17] = pixelVal;
  letterMap[11][20] = pixelVal;
  letterMap[11][21] = pixelVal;
  letterMap[11][22] = pixelVal;
  letterMap[11][23] = pixelVal;
  letterMap[11][24] = pixelVal;
  letterMap[11][25] = pixelVal;
  letterMap[12][2] = pixelVal;
  letterMap[12][3] = pixelVal;
  letterMap[12][4] = pixelVal;
  letterMap[12][5] = pixelVal;
  letterMap[12][6] = pixelVal;
  letterMap[12][12] = pixelVal;
  letterMap[12][13] = pixelVal;
  letterMap[12][14] = pixelVal;
  letterMap[12][15] = pixelVal;
  letterMap[12][16] = pixelVal;
  letterMap[12][17] = pixelVal;
  letterMap[12][21] = pixelVal;
  letterMap[12][22] = pixelVal;
  letterMap[12][23] = pixelVal;
  letterMap[12][24] = pixelVal;
  letterMap[12][25] = pixelVal;
  letterMap[13][2] = pixelVal;
  letterMap[13][3] = pixelVal;
  letterMap[13][4] = pixelVal;
  letterMap[13][5] = pixelVal;
  letterMap[13][6] = pixelVal;
  letterMap[13][12] = pixelVal;
  letterMap[13][13] = pixelVal;
  letterMap[13][14] = pixelVal;
  letterMap[13][15] = pixelVal;
  letterMap[13][16] = pixelVal;
  letterMap[13][21] = pixelVal;
  letterMap[13][22] = pixelVal;
  letterMap[13][23] = pixelVal;
  letterMap[13][24] = pixelVal;
  letterMap[13][25] = pixelVal;
  letterMap[14][2] = pixelVal;
  letterMap[14][3] = pixelVal;
  letterMap[14][4] = pixelVal;
  letterMap[14][5] = pixelVal;
  letterMap[14][6] = pixelVal;
  letterMap[14][11] = pixelVal;
  letterMap[14][12] = pixelVal;
  letterMap[14][13] = pixelVal;
  letterMap[14][14] = pixelVal;
  letterMap[14][15] = pixelVal;
  letterMap[14][16] = pixelVal;
  letterMap[14][21] = pixelVal;
  letterMap[14][22] = pixelVal;
  letterMap[14][23] = pixelVal;
  letterMap[14][24] = pixelVal;
  letterMap[14][25] = pixelVal;
  letterMap[15][2] = pixelVal;
  letterMap[15][3] = pixelVal;
  letterMap[15][4] = pixelVal;
  letterMap[15][5] = pixelVal;
  letterMap[15][6] = pixelVal;
  letterMap[15][11] = pixelVal;
  letterMap[15][12] = pixelVal;
  letterMap[15][13] = pixelVal;
  letterMap[15][14] = pixelVal;
  letterMap[15][15] = pixelVal;
  letterMap[15][21] = pixelVal;
  letterMap[15][22] = pixelVal;
  letterMap[15][23] = pixelVal;
  letterMap[15][24] = pixelVal;
  letterMap[15][25] = pixelVal;
  letterMap[16][2] = pixelVal;
  letterMap[16][3] = pixelVal;
  letterMap[16][4] = pixelVal;
  letterMap[16][5] = pixelVal;
  letterMap[16][6] = pixelVal;
  letterMap[16][11] = pixelVal;
  letterMap[16][12] = pixelVal;
  letterMap[16][13] = pixelVal;
  letterMap[16][14] = pixelVal;
  letterMap[16][15] = pixelVal;
  letterMap[16][21] = pixelVal;
  letterMap[16][22] = pixelVal;
  letterMap[16][23] = pixelVal;
  letterMap[16][24] = pixelVal;
  letterMap[16][25] = pixelVal;
  letterMap[17][2] = pixelVal;
  letterMap[17][3] = pixelVal;
  letterMap[17][4] = pixelVal;
  letterMap[17][5] = pixelVal;
  letterMap[17][6] = pixelVal;
  letterMap[17][10] = pixelVal;
  letterMap[17][11] = pixelVal;
  letterMap[17][12] = pixelVal;
  letterMap[17][13] = pixelVal;
  letterMap[17][14] = pixelVal;
  letterMap[17][21] = pixelVal;
  letterMap[17][22] = pixelVal;
  letterMap[17][23] = pixelVal;
  letterMap[17][24] = pixelVal;
  letterMap[17][25] = pixelVal;
  letterMap[18][3] = pixelVal;
  letterMap[18][4] = pixelVal;
  letterMap[18][5] = pixelVal;
  letterMap[18][6] = pixelVal;
  letterMap[18][7] = pixelVal;
  letterMap[18][10] = pixelVal;
  letterMap[18][11] = pixelVal;
  letterMap[18][12] = pixelVal;
  letterMap[18][13] = pixelVal;
  letterMap[18][14] = pixelVal;
  letterMap[18][21] = pixelVal;
  letterMap[18][22] = pixelVal;
  letterMap[18][23] = pixelVal;
  letterMap[18][24] = pixelVal;
  letterMap[18][25] = pixelVal;
  letterMap[19][3] = pixelVal;
  letterMap[19][4] = pixelVal;
  letterMap[19][5] = pixelVal;
  letterMap[19][6] = pixelVal;
  letterMap[19][7] = pixelVal;
  letterMap[19][8] = pixelVal;
  letterMap[19][9] = pixelVal;
  letterMap[19][10] = pixelVal;
  letterMap[19][11] = pixelVal;
  letterMap[19][12] = pixelVal;
  letterMap[19][13] = pixelVal;
  letterMap[19][20] = pixelVal;
  letterMap[19][21] = pixelVal;
  letterMap[19][22] = pixelVal;
  letterMap[19][23] = pixelVal;
  letterMap[19][24] = pixelVal;
  letterMap[19][25] = pixelVal;
  letterMap[20][4] = pixelVal;
  letterMap[20][5] = pixelVal;
  letterMap[20][6] = pixelVal;
  letterMap[20][7] = pixelVal;
  letterMap[20][8] = pixelVal;
  letterMap[20][9] = pixelVal;
  letterMap[20][10] = pixelVal;
  letterMap[20][11] = pixelVal;
  letterMap[20][12] = pixelVal;
  letterMap[20][13] = pixelVal;
  letterMap[20][19] = pixelVal;
  letterMap[20][20] = pixelVal;
  letterMap[20][21] = pixelVal;
  letterMap[20][22] = pixelVal;
  letterMap[20][23] = pixelVal;
  letterMap[20][24] = pixelVal;
  letterMap[21][5] = pixelVal;
  letterMap[21][6] = pixelVal;
  letterMap[21][7] = pixelVal;
  letterMap[21][8] = pixelVal;
  letterMap[21][9] = pixelVal;
  letterMap[21][10] = pixelVal;
  letterMap[21][11] = pixelVal;
  letterMap[21][12] = pixelVal;
  letterMap[21][18] = pixelVal;
  letterMap[21][19] = pixelVal;
  letterMap[21][20] = pixelVal;
  letterMap[21][21] = pixelVal;
  letterMap[21][22] = pixelVal;
  letterMap[21][23] = pixelVal;
  letterMap[21][24] = pixelVal;
  letterMap[22][6] = pixelVal;
  letterMap[22][7] = pixelVal;
  letterMap[22][8] = pixelVal;
  letterMap[22][9] = pixelVal;
  letterMap[22][10] = pixelVal;
  letterMap[22][11] = pixelVal;
  letterMap[22][12] = pixelVal;
  letterMap[22][18] = pixelVal;
  letterMap[22][19] = pixelVal;
  letterMap[22][20] = pixelVal;
  letterMap[22][21] = pixelVal;
  letterMap[22][22] = pixelVal;
  letterMap[22][23] = pixelVal;
  letterMap[23][7] = pixelVal;
  letterMap[23][8] = pixelVal;
  letterMap[23][9] = pixelVal;
  letterMap[23][10] = pixelVal;
  letterMap[23][11] = pixelVal;
  letterMap[23][19] = pixelVal;
  letterMap[23][20] = pixelVal;
  letterMap[23][21] = pixelVal;
  letterMap[23][22] = pixelVal;
  letterMap[24][8] = pixelVal;
  letterMap[24][9] = pixelVal;
  letterMap[24][10] = pixelVal;
  letterMap[24][11] = pixelVal;
  letterMap[24][20] = pixelVal;
  letterMap[24][21] = pixelVal;
}

void setup() {
  panelPort.begin(RS485_BAUD);
  Serial.begin(9600);
  setLetterMap(true);
  randomSeed(millis());
  y_scaling_factor = (float)(LETTER_ROWS) / (float)(SENSOR_MAX - SENSOR_MIN);
}

int getSensorValue() {
  //TODO(raymond) get a sensor value here from USB and return the int
  //return -1 if no value was read
  int serialCount = 0;
  String sensorString = "";
  while (Serial.available() > 0) {
    int inChar = Serial.read();
    if (isDigit(inChar)) {
      sensorString += (char)inChar;
    }
    if (inChar == '\n' || inChar == '\0') {
      break;
    }
    delay(5);
  }
  int val = -1;
  if (sensorString > "") {
    val = sensorString.toInt();
  }
  //  int val = random(0,10)<1?-1:random(0,100);  // test 1 time out of 10, return no sensor value
  #ifdef _DEBUG
  if (val >= 0) {
    //val = SENSOR_MAX;  // Force full rendering
    #ifdef _DEBUG
    Serial.print("Sensor: ");
    Serial.println(val);
    #endif
  }
  #endif
  if (val >= sensorHighWatermark) {
    sensorHighWatermark = val;
    highWaterMarkAt = millis();
  }
  return val;
}

// Return the high watermark, reset it if it has expired
// This may be the same as the current sensor value which is OK for our usage
int currentHighWatermark() {
  if ((highWaterMarkAt > 0) && (millis() > highWaterMarkAt+SENSOR_HIGHWATERMARK_TIMEOUT_MS)) {
      sensorHighWatermark = 0;
  }
  return sensorHighWatermark;
}

bool setDisplayForSensor() {
  int sensorReading = getSensorValue();
  if (sensorReading < 0) {
    return false;
  }
  setDisplay(false, sensorReading);
  return true;
}

void setDisplayForIdle() {
  setDisplay(true, SENSOR_MAX);
}

void loop() {
  if (nextRefreshAt == 0) {
    nextRefreshAt = millis();
    idleAt = millis() + IDLE_TIMEOUT_MS;
  }
  bool sensorWasRead = setDisplayForSensor();
  if (sensorWasRead) {
    lastUpdatedAt = millis();
    idleAt = lastUpdatedAt + IDLE_TIMEOUT_MS;
  }
  if (idleAt > 0 && millis() > idleAt) {
    #ifdef _DEBUG
    Serial.print ("idle:");
    Serial.println(millis());
    #endif
    setDisplayForIdle();
  }
  if (millis() > nextRefreshAt && nextRefreshAt > 0) {
    #ifdef _DEBUG
    Serial.print ("refresh:");
    Serial.println(millis());
    #endif
    refreshDisplay();
    lastRefreshedAt = millis();
    nextRefreshAt = lastRefreshedAt + REFRESH_FREQUENCY_MS;
  }
}
