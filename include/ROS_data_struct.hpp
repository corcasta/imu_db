#ifndef SERVER_H
#define SERVER_H

// Here we define a data structure for our sensors
#include <map>
#include <variant>
#include <BNo08x_setup.hpp>

#define LIN_x (sensorValue.un.linearAcceleration.x)
#define LIN_y (sensorValue.un.linearAcceleration.y)
#define LIN_z (sensorValue.un.linearAcceleration.z)

#define MAG_x (sensorValue.un.magneticField.x)
#define MAG_y (sensorValue.un.magneticField.y)
#define MAG_z (sensorValue.un.magneticField.z)

#define GAME_i (sensorValue.un.gameRotationVector.i)
#define GAME_j (sensorValue.un.gameRotationVector.j)
#define GAME_k (sensorValue.un.gameRotationVector.k)
#define GAME_real (sensorValue.un.gameRotationVector.real)

// These are timestamps from the RAW sensors. 
//This may be a little flawed, since it does not factor in the calibration overhead.
// We can write own time logic based off of known frequency of sensors.  

#define LIN_timestamp ()
#define MAG_timestamp ()
#define GAME_timestamp ()

struct DataSensor3 {
    uint32_t timestamp = 0;
    float x = 0.0;
    float y = 0.0;
    float z = 0.0;
};

struct DataSensor4 {
    uint32_t timestamp = 0;
    float i = 0.0;
    float j = 0.0;
    float k = 0.0;
    float real = 0.0;
};

// Creating the map for the sensors objects
std::map<std::string, std::variant<DataSensor3, DataSensor4>> sensorData;

void updateDataSensor3(const std::string& sensorName, float x, float y, float z, uint32_t timestamp) {
    auto it = sensorData.find(sensorName);
    if (it != sensorData.end()) {
        // Attempt to retrieve a pointer to DataSensor3 within the variant
        if (auto* data = std::get_if<DataSensor3>(&it->second)) {
            // If successful, update the values
            data->x = x;
            data->y = y;
            data->z = z;
            data -> timestamp = timestamp;
        } else {
            std::cerr << "Error: " << sensorName << " is not of type DataSensor3." << std::endl;
        }
    } else {
        std::cerr << "Error: " << sensorName << " not found in sensorData." << std::endl;
    }
}


void updateDataSensor4(const std::string& sensorName, float i, float j, float k, float real, uint32_t timestamp) {
    if (auto it = sensorData.find(sensorName); it != sensorData.end()) {
        if (auto* data = std::get_if<DataSensor4>(&it->second)) {
            data->i = i;
            data->j = j;
            data->k = k;
            data->real = real;
            data -> timestamp = timestamp;
        } else {
            std::cerr << "Error: " << sensorName << " is not of type DataSensor4." << std::endl;
        }
    } else {
        std::cerr << "Error: " << sensorName << " not found in sensorData." << std::endl;
    }
}

void printDictionary(const std::map<std::string, std::variant<DataSensor3, DataSensor4>>& dictionary) {
    for (const auto& [sensorName, sensorVariant] : dictionary) {
        std::cout << sensorName << ": ";
        if (std::holds_alternative<DataSensor3>(sensorVariant)) {
            const auto& data = std::get<DataSensor3>(sensorVariant);
            std::cout << "x=" << data.x << ", y=" << data.y << ", z=" << data.z;
        } else if (std::holds_alternative<DataSensor4>(sensorVariant)) {
            const auto& data = std::get<DataSensor4>(sensorVariant);
            std::cout << "i=" << data.i << ", j=" << data.j << ", k=" << data.k << ", real=" << data.real;
        }
        std::cout << std::endl;
    }
}




#endif
