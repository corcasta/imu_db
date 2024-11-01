#ifndef BNO08X_setup_H
#define BNO08X_setup_H

#define BNO08X_CS 5
#define BNO08X_INT 4
#define BNO08X_RESET 3

#include <Adafruit_BNO08x.h>
#include <sh2_SensorValue.h>  
#include <iostream>
#include <Arduino.h>
#include <Adafruit_BNO08x.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>
#include "shtp.h"
#include "sh2_err.h"
#include "sh2_util.h"
#include <sh2.h>
#include <stdint.h>
#include <stddef.h>
#include <stdio.h>

extern sh2_SensorValue_t sensorValue;
extern Adafruit_BNO08x bno08x;

extern unsigned long startTime; 


void serial_begin();
void setReports(sh2_SensorId_t sensorID, uint32_t interval_ms);

#endif 


