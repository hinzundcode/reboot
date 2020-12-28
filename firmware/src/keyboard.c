#include <keyboard.h>
#include <keymap.h>
#include <ps2_keyboard.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdio.h>

#define KEY_COUNT 512
#define KEYBOARD_BUFFER_SIZE 16
#define KEYBOARD_BUFFER_MASK (KEYBOARD_BUFFER_SIZE-1)

static bool key_states[KEY_COUNT] = { 0 };

static uint8_t buffer[KEYBOARD_BUFFER_SIZE];
static unsigned int buffer_produce;
static unsigned int buffer_consume;

static void key_press(uint16_t key) {
	if (key >= KEY_COUNT) return;
	key_states[key] = 1;
	
	char c = keymap_get_input(key, key_states);
	if (c) {
		unsigned int buffer_produce_next = (buffer_produce + 1) & KEYBOARD_BUFFER_MASK;
		if (buffer_produce_next != buffer_consume) {
			buffer[buffer_produce] = c;
			buffer_produce = buffer_produce_next;
		}
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

char keyboard_read() {
	if (buffer_consume == buffer_produce) {
		return 0;
	}
	
	char key = buffer[buffer_consume];
	buffer_consume = (buffer_consume + 1) & KEYBOARD_BUFFER_MASK;
	return key;
}

char keyboard_read_blocking() {
	while (buffer_consume == buffer_produce) {
		keyboard_service();
	}
	
	return keyboard_read();
}
