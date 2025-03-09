/**
 * Copyright (c) 2021 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 *
 */

 #include <stdio.h>
 #include <string.h>
 #include <stdlib.h>
 
 #include "pico/stdlib.h"     ///includes the standard pico library
 #include "hardware/adc.h"     ///includes the library for analogue-to-digital conversion (ADC)
 #include "hardware/rtc.h"     ///inludes the real time clock library
 #include "pico/util/datetime.h"     ///includes the date and time utilities
 
 /* Choose 'C' for Celsius or 'F' for Fahrenheit. */
 #define TEMPERATURE_UNITS 'C'
 
 /* References for this implementation:
  * raspberry-pi-pico-c-sdk.pdf, Section '4.1.1. hardware_adc'
  * pico-examples/adc/adc_console/adc_console.c */
 float read_onboard_temperature(const char unit) {     ///function that reads the onboard temperature
     
     /* 12-bit conversion, assume max value == ADC_VREF == 3.3 V */     ///for analogue-to-digital conversion (ADC)
     const float conversionFactor = 3.3f / (1 << 12);
 
     float adc = (float)adc_read() * conversionFactor;     ///reads the ADC value
     float tempC = 27.0f - (adc - 0.706f) / 0.001721f;     ///converts the ADC value to temperature in Celsius
 
     if (unit == 'C') {
         return tempC;     ///returns the temperatures in temperature in celsius 
     } else if (unit == 'F') {
         return tempC * 9 / 5 + 32;     ///converts the temperature in Farhenheit if needed
     }
 
     return -1.0f;    ///return an error value if the units are invalid
 }
 
 int main() {
 
     stdio_init_all();     ///initalises the standard input and output
 #ifdef PICO_DEFAULT_LED_PIN     
     gpio_init(PICO_DEFAULT_LED_PIN);     ///initialises the onbuard LEDs
     gpio_set_dir(PICO_DEFAULT_LED_PIN, GPIO_OUT);
 #endif
 
     /* Initialize hardware AD converter, enable onboard temperature sensor and
      *   select its channel (do this once for efficiency, but beware that this
      *   is a global operation). */
     adc_init();     ///initialises the ADC hardware
     adc_set_temp_sensor_enabled(true);     ///enables the onboard temperature sensor
     adc_select_input(4);     ///selects the input channel 4 of the ADC as it is the temperature sensor itself
         
     while (true)
     {
         // read the temperature from the ADC, and convert to a float
         float temperature = read_onboard_temperature(TEMPERATURE_UNITS);
 
         // get tche time at which the temperature data was obtained
         uint64_t sample_timestamp = time_us_64();
 
         // send the temperature data along with its timestamp
         printf("%llu %.02f\n", sample_timestamp, temperature); // line for optimised behaviour
         //printf("Onboard temperature @ %llu = %.02f %c\n", sample_timestamp, temperature, TEMPERATURE_UNITS);
     }
 }