#include <BNo08x_setup.hpp>
#include <subsensortest.hpp>
#include <ROS_data_struct.hpp>
#include <dataloss.hpp> 

    DataSensor3 magField;
    DataSensor3 linAcc;
    DataSensor4 gameRot;

void setup() {
    serial_begin();
    setReports(SH2_LINEAR_ACCELERATION, 20000); // 200 HZ
    setReports(SH2_MAGNETIC_FIELD_CALIBRATED, 20000); // 50 HZ
    setReports(SH2_GAME_ROTATION_VECTOR, 20000); // 200 HZ (5000)

    sensorData["LinearAcc"] = DataSensor3{};
    sensorData["MagField"] = DataSensor3{};
    sensorData["GameRot"] = DataSensor4{};
}


void loop() {
    run_freq_test(false);


/*
    if (bno08x.getSensorEvent(&sensorValue)) {

    switch (sensorValue.sensorId){
        case SH2_MAGNETIC_FIELD_CALIBRATED:
            updateDataSensor3("MagField", LIN_x, LIN_y, LIN_z, 16234589);
            std::cout << LIN_x + LIN_y + LIN_z;
        case SH2_LINEAR_ACCELERATION:
            updateDataSensor3("LinearAcc", MAG_x, MAG_y, MAG_z, 16234589);
        case SH2_GAME_ROTATION_VECTOR:
            updateDataSensor4("GameRot", GAME_i, GAME_j, GAME_k, GAME_real, 16234567);
      }
    }
    */
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

   