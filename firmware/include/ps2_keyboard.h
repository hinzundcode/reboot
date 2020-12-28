#ifndef __PS2_KEYBOARD_H
#define __PS2_KEYBOARD_H

#include <stdint.h>

void ps2_keyboard_init();
void ps2_keyboard_isr();
uint8_t ps2_keyboard_read();

#endif
