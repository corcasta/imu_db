#include <dataloss.hpp>

// Checksum. Not needed after 

uint16_t calculate_checksum(uint8_t *data, size_t length) {
    uint16_t checksum = 0;
    for (size_t i = 0; i < length; i++) {
        checksum += data[i];  
    }
    return checksum;
} 








