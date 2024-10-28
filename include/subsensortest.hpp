#ifndef SUBSENSORTEST_H
#define SUBSENSORTEST_H

#include <BNo08x_setup.hpp>  // Include your BNO08x setup header

// Global variables
extern bool activate_coordinate_print;
extern int game_rotation_counter;
extern int acc_counter;
extern int magnetic_counter;

// Function declaration
void run_freq_test(bool activate_coordinate_print);

#endif // SUBSENSORTEST_H

