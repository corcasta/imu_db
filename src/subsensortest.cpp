#include <subsensortest.hpp>
#include <BNo08x_setup.hpp>


bool activate_coordinate_print;
int game_rotation_counter = 0;
int acc_counter = 0;
int magnetic_counter = 0;

void run_freq_test(bool activate_coordinate_print) {
    // Start timer
    unsigned long currentTime = millis();
    
    // Update sensor event
    if (bno08x.getSensorEvent(&sensorValue)) {


    if(activate_coordinate_print){
    switch(sensorValue.sensorId){
      
      case SH2_LINEAR_ACCELERATION:

        Serial.print("X:");
        Serial.println(sensorValue.un.linearAcceleration.x);
        
        Serial.print("Y:");
        Serial.println(sensorValue.un.linearAcceleration.y);

        Serial.print("Z:");
        Serial.println(sensorValue.un.linearAcceleration.z);

break;
    case SH2_MAGNETIC_FIELD_CALIBRATED:
      /* Units are uTesla */

      
        Serial.print("X:");
        Serial.println(sensorValue.un.magneticField.x);
        
        Serial.print("Y:");
        Serial.println(sensorValue.un.magneticField.y);

        Serial.print("Z:");
        Serial.println(sensorValue.un.linearAcceleration.z);
  
    break;

    case SH2_GAME_ROTATION_VECTOR:
  
        Serial.print("i:");
        Serial.println(sensorValue.un.gameRotationVector.i);
        
        Serial.print("j:");
        Serial.println(sensorValue.un.gameRotationVector.j);

        Serial.print("k:");
        Serial.println(sensorValue.un.gameRotationVector.k);

        Serial.print("real:");
        Serial.println(sensorValue.un.gameRotationVector.real);

     break;

    // TRIAL for Magni
      case SH2_STABILITY_DETECTOR:

      Serial.println(sensorValue.un.stabilityDetector.stability);

      break;

    }

    }
        // Here with check for specific sensor types and increment counters
        switch (sensorValue.sensorId) {
            case SH2_LINEAR_ACCELERATION:
                acc_counter ++;
                break;
            case SH2_MAGNETIC_FIELD_CALIBRATED:
                magnetic_counter++;
                break;
            case SH2_GAME_ROTATION_VECTOR:
                game_rotation_counter ++;
                break;
        }
    }
    
    // Print counts every second
    
    if (currentTime - startTime >= 1000) {
        Serial.println("The magnetic counter in one second:"); 
        Serial.println(magnetic_counter);
        Serial.println("The game rotation counter in one second:"); 
        Serial.println(game_rotation_counter);
        Serial.println("The acc counter in one second:"); 
        Serial.println(acc_counter);
  
        // Resetting counters
        magnetic_counter = 0;
        game_rotation_counter = 0;
        acc_counter = 0; 

        // Updating timer
        startTime = currentTime;
        
    }
    
    }
