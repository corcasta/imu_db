#include <BNo08x_setup.hpp>
#include <subsensortest.hpp>
#include <ROS_data_struct.hpp>
#include <dataloss.hpp> 

DataSensor3 magField;
DataSensor3 linAcc;
DataSensor4 gameRot;
int n = 0;

bool linearAccRead = false;
bool gameRotRead = false;

void setup() {
    serial_begin();
    setReports(SH2_LINEAR_ACCELERATION, 20000); // 200 Hz
    setReports(SH2_GAME_ROTATION_VECTOR, 20000); // 200 Hz

    sensorData["LinearAcc"] = DataSensor3{};
    sensorData["MagField"] = DataSensor3{};
    sensorData["GameRot"] = DataSensor4{};

    delay(1000); // Wait for sensor initialization
}

void loop() {
    
    if (bno08x.getSensorEvent(&sensorValue)) {
        // Capture the current timestamp in microseconds
        unsigned long timestampMicros = micros();

        switch (sensorValue.sensorId) {
            case SH2_LINEAR_ACCELERATION:
                Serial.printf("%d", n);
                Serial.println("L");
                Serial.printf("T: %lu us\n", timestampMicros);
                Serial.printf("x = %.6f\n", sensorValue.un.linearAcceleration.x);
                Serial.printf("y = %.6f\n", sensorValue.un.linearAcceleration.y);
                Serial.printf("z = %.6f\n", sensorValue.un.linearAcceleration.z);
                linearAccRead = true;
                break;

            case SH2_GAME_ROTATION_VECTOR:
                Serial.printf("%d", n);
                Serial.println("Q");
                Serial.printf("i = %.8f\n", sensorValue.un.gameRotationVector.i);
                Serial.printf("j = %.8f\n", sensorValue.un.gameRotationVector.j);
                Serial.printf("k = %.8f\n", sensorValue.un.gameRotationVector.k);
                Serial.printf("r = %.8f\n", sensorValue.un.gameRotationVector.real);
                gameRotRead = true;
                break;
        }

        // If both sensors have been read, increment the frame counter and reset flags
        if (linearAccRead && gameRotRead) {
            n++;                  // Increment counter only after both sensors are read
            linearAccRead = false; // Reset flags for the next frame
            gameRotRead = false;
        }
    }
}




//MAGNI
/*
  int status = sh2_devSleep();
  status;

        if (bno08x.getSensorEvent(&sensorValue)) {
        switch (sensorValue.sensorId) {
            case SH2_LINEAR_ACCELERATION:
                
                Serial.print("Stability status: ");
                Serial.println(sensorValue.un.linearAcceleration.x);
                break;
        }
    }
*/

   