#include <Bno08x_setup.hpp>

sh2_SensorValue_t sensorValue;
// Instantiate the BNO08x object with the reset pin
Adafruit_BNO08x bno08x(BNO08X_RESET); 
unsigned long startTime = 0; 

void serial_begin(){
Serial.begin(115200);
  while (!Serial) delay(10);  

  // Initialize the BNO08x
  if (!bno08x.begin_SPI(BNO08X_CS, BNO08X_INT)) {
    Serial.println("Failed to initialize BNO08x!");
    while (1);
  }
  
    Serial.println("BNO08x initialized successfully!");

    startTime = millis();

}

void setReports(sh2_SensorId_t sensorID, uint32_t interval_ms) {
  if (!bno08x.enableReport(sensorID, interval_ms)) {
    // Serial.println("Failed to enable sensor report!");
  } else {
    
    // Serial.print("Sensor enabled with ID: ");
    // Serial.println(sensorID);
  }
}


