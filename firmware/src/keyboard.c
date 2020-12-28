#include <keyboard.h>
#include <keymap.h>
#include <ps2_keyboard.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>

#define KEY_COUNT 512

static bool key_states[KEY_COUNT] = { 0 };

static void key_press(uint16_t key) {
	if (key >= KEY_COUNT) return;
	key_states[key] = 1;
	
	char c = keymap_get_input(key, key_states);
	if (c) {
		printf("%c", c);
	}
}

static void key_up(uint16_t key) {
	if (key >= KEY_COUNT) return;
	key_states[key] = 0;
}

void keyboard_service() {
	uint8_t data;
	uint16_t extended;
	
	while (data = ps2_keyboard_read()) {
		if (data == 0xE0) {
			extended = 1 << 8;
			data = ps2_keyboard_read_blocking();
		} else {
			extended = 0;
		}
		
		if (data == 0xF0) {
			uint8_t data2 = ps2_keyboard_read_blocking();
			key_up(extended | data2);
		} else {
			key_press(extended | data);
		}
	}
}
