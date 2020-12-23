#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <irq.h>
#include <uart.h>
#include <console.h>
#include <generated/csr.h>

#include <rgb.h>

void isr() {
	__attribute__((unused)) unsigned int irqs;

	irqs = irq_pending() & irq_getmask();

#ifndef UART_POLLING
	if(irqs & (1 << UART_INTERRUPT))
		uart_isr();
#endif
}

int main() {
	irq_setmask(0);
	irq_setie(1);
	
	rgb_init();
	uart_init();
	
	rgb_set(RGB_LED0, 255, 0, 0);
	rgb_set(RGB_LED1, 0, 255, 0);
	rgb_set(RGB_LED2, 0, 0, 255);
	rgb_set(RGB_LED3, 255, 255, 255);
	
	for (;;) {}
		
	//busy_wait(1000);
}
