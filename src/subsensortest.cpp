
#include <Arduino.h>
#include <Adafruit_BNO08x.h>
#include <SPI.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>


// For SPI mode, we need a CS pin
#define BNO08X_CS 5
#define BNO08X_INT 4
#define BNO08X_RESET 3

int acc_counter = 0;
int gyro_counter = 0;
int magnetic_counter = 0;

float startTime;
float currentTime; 
sh2_SensorValue_t sensorValue;

// Instantiate the BNO08x object with the reset pin
Adafruit_BNO08x bno08x(BNO08X_RESET); 

// Create BNO08x object
Adafruit_BNO08x bno = Adafruit_BNO08x(BNO08X_RESET);


void setReports(sh2_SensorId_t sensorID, uint32_t interval_ms) {
  if (!bno.enableReport(sensorID, interval_ms)) {
    Serial.println("Failed to enable sensor report!");
  } else {

    Serial.print("Sensor enabled with ID: ");
    Serial.println(sensorID);
  }
}


void setup() {
  Serial.begin(115200);
  while (!Serial) delay(10);  

  // Initialize the BNO08x
  if (!bno08x.begin_SPI(BNO08X_CS, BNO08X_INT)) {
    Serial.println("Failed to initialize BNO08x!");
    while (1);
  }
  
    Serial.println("BNO08x initialized successfully!");

    startTime = millis();
    //enableSensor(SH2_MAGNETIC_FIELD_CALIBRATED, 10000);  // 10 ms / 100 Hz
    //setReports(SH2_GYROSCOPE_CALIBRATED, 2500); 


    setReports(SH2_LINEAR_ACCELERATION, 1000); // CHeck to see real freq
    setReports(SH2_MAGNETIC_FIELD_CALIBRATED, 2000);
    setReports(SH2_GAME_ROTATION_VECTOR,1000); // CHeck to see real freq

}



void loop() {
    // Start timer
    unsigned long currentTime = millis();
    
    // Update sensor event
    if (bno.getSensorEvent(&sensorValue)) {
        // Check for specific sensor types and increment counters
        switch (sensorValue.sensorId) {
            case SH2_GYROSCOPE_CALIBRATED:
                gyro_counter++;
                break;
            case SH2_MAGNETIC_FIELD_CALIBRATED:
                magnetic_counter++;
                break;
            case SH2_ACCELEROMETER:
                acc_counter ++;
                break;
        }
    }
    
    // Print counts every second
    
    if (currentTime - startTime >= 1000) {
        Serial.println("The magnetic counter in one second:"); 
        Serial.println(magnetic_counter);
        Serial.println("The gyroscope counter in one second:"); 
        Serial.println(gyro_counter);
        Serial.println("The acc counter in one second:"); 
        Serial.println(acc_counter);

        // Resetting counters
        gyro_counter = 0;
        magnetic_counter = 0;
        acc_counter = 0; 

        // Updating timer
        startTime = currentTime;

    }
    }



    // ROS data struct: https://docs.ros.org/en/noetic/api/geometry_msgs/html/msg/Pose.html
   
    // I am going to make a check for data loss and/or corruption using this:
    // https://github.com/adafruit/Adafruit_CircuitPython_BNO08x/blob/main/adafruit_bno08x/spi.py




