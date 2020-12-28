#include <ps2_keyboard.h>
#include <generated/csr.h>
#include <irq.h>

volatile uint8_t keyboard_data = 0;

void ps2_keyboard_init() {
	ps2_keyboard_ev_pending_write(ps2_keyboard_ev_pending_read());
	ps2_keyboard_ev_enable_write(1);
	irq_setmask(irq_getmask() | (1 << PS2_KEYBOARD_INTERRUPT));
}

void ps2_keyboard_isr() {
	if (!ps2_keyboard_status_error_read()) {
		keyboard_data = ps2_keyboard_data_read();
	}
	
	ps2_keyboard_control_write(1);
	
	ps2_keyboard_ev_pending_write(1);
	//ps2_keyboard_ev_enable_write(1);
}

uint8_t ps2_keyboard_read() {
	uint8_t data = keyboard_data;
	keyboard_data = 0;
	return data;
}
