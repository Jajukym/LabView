/*
  Heart beat plotting!
  By: Nathan Seidle @ SparkFun Electronics
  Date: October 20th, 2016
  https://github.com/sparkfun/MAX30105_Breakout

  Hardware Connections (Breakoutboard to Arduino):
  -5V = 5V (3.3V is allowed)
  -GND = GND
  -SDA = A4 (or SDA)
  -SCL = A5 (or SCL)
  -INT = Not connected

  The MAX30105 Breakout can handle 5V or 3.3V I2C logic. We recommend powering the board with 5V
  but it will also run at 3.3V.
*/
/*
------------------------------------
Auther: Koji Ohashi
Copyright (c) 2020 Japan LabVIEW Users Group, Volunteer  members.
This VI is released under the MIT License.
http://opensource.org/licenses/mit-license.php
------------------------------------
 */

#include <Wire.h>
#include "MAX30105.h"

MAX30105 HR_Sensor;

void setup()
{
  Serial.begin(115200);
  Serial.println("my_HeartBeat10ms");

  // Initialize sensor
  if (!HR_Sensor.begin(Wire, I2C_SPEED_FAST)) //Use default I2C port, 400kHz speed
  {
    Serial.println("MAX30105 was not found. Please check wiring/power. ");
    while (1);
  }

  byte ledBrightness = 0x1F;  //Options: 0=Off to 255=50mA---default is 0x1F
  byte sampleAverage = 8;     //Options: 1, 2, 4, 8, 16, 32---default is 8
  byte ledMode = 1;           //Options: 1 = Red only, 2 = Red + IR, 3 = Red + IR + Green---default is 3
  int sampleRate = 1000;      //Options: 50, 100, 200, 400, 800, 1000, 1600, 3200---default is 100
  int pulseWidth = 411;       //Options: 69, 118, 215, 411---default is 411
  int adcRange = 16384;       //Options: 2048, 4096, 8192, 16384---default is 4096

  HR_Sensor.setup(ledBrightness, sampleAverage, ledMode, sampleRate, pulseWidth, adcRange); //Configure sensor with these settings
}

void loop()
{
  float t=micros();
  Serial.println(HR_Sensor.getRed()); //Send raw data to plotter
  while((micros()-t)<10000){}
}
