#ifndef __RGB_H
#define __RGB_H

#include <stdint.h>

#define RGB_LED0 0
#define RGB_LED1 1
#define RGB_LED2 2
#define RGB_LED3 3

void rgb_init();
void rgb_set(uint8_t led, uint8_t r, uint8_t g, uint8_t b);

#endif
