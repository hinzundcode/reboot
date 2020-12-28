#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <irq.h>
#include <uart.h>
#include <console.h>
#include <generated/csr.h>

#include <rgb.h>
#include <ps2_keyboard.h>
#include <keyboard.h>

void isr() {
	__attribute__((unused)) unsigned int irqs;

	irqs = irq_pending() & irq_getmask();
	
#ifndef UART_POLLING
	if (irqs & (1 << UART_INTERRUPT))
		uart_isr();
#endif
	
	if (irqs & (1 << PS2_KEYBOARD_INTERRUPT))
		ps2_keyboard_isr();
}

// from adafruit, https://learn.adafruit.com/florabrella/test-the-neopixel-strip
void rgb_wheel(uint8_t led, uint8_t pos) {
	if (pos < 85) {
		rgb_set(led, pos * 3, 255 - pos * 3, 0);
	} else if (pos < 170) {
		pos -= 85;
		rgb_set(led, 255 - pos * 3, 0, pos * 3);
	} else {
		pos -= 170;
		rgb_set(led, 0, pos * 3, 255 - pos * 3);
	}
}
void rgb_rainbow() {
	uint8_t i = 0;
	for (;;) {
		i++;
		
		for (uint8_t led = 0; led < 4; led++) {
			rgb_wheel(led, i + (4-led)*10);
		}
		busy_wait(20);
	}
}

int main() {
	irq_setmask(0);
	irq_setie(1);
	
	uart_init();
	
	ps2_keyboard_init();
	
	//rgb_rainbow();
	
	for (;;) {
		char c = keyboard_read_blocking();
		printf("%c", c);
	}
	
	for (;;) {}
}
