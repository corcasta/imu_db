#ifndef DATALOSS_H
#define DATALOSS_H

#include <BNo08x_setup.hpp>

// Function declaration for checksum calculation
uint16_t calculate_checksum(uint8_t *data, size_t length);

#endif // DATALOSS_H
