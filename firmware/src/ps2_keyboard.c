#include <ps2_keyboard.h>
#include <generated/csr.h>
#include <irq.h>

#define PS2_KEYBOARD_BUFFER_SIZE 16
#define PS2_KEYBOARD_BUFFER_MASK (PS2_KEYBOARD_BUFFER_SIZE-1)

static uint8_t buffer[PS2_KEYBOARD_BUFFER_SIZE];
static volatile unsigned int buffer_produce;
static unsigned int buffer_consume;

void ps2_keyboard_init() {
	ps2_keyboard_ev_pending_write(ps2_keyboard_ev_pending_read());
	ps2_keyboard_ev_enable_write(1);
	irq_setmask(irq_getmask() | (1 << PS2_KEYBOARD_INTERRUPT));
}

void ps2_keyboard_isr() {
	uint32_t status = ps2_keyboard_status_read();
	
	if (ps2_keyboard_status_valid_extract(status)) {
		uint8_t data = ps2_keyboard_status_data_extract(status);
		
		unsigned int buffer_produce_next = (buffer_produce + 1) & PS2_KEYBOARD_BUFFER_MASK;
		if (buffer_produce_next != buffer_consume) {
			buffer[buffer_produce] = data;
			buffer_produce = buffer_produce_next;
		}
	}
	
	ps2_keyboard_ev_pending_write(1);
	//ps2_keyboard_ev_enable_write(1);
}

uint8_t ps2_keyboard_read() {
	if (buffer_consume == buffer_produce) {
		return 0;
	}
	
	uint8_t data = buffer[buffer_consume];
	buffer_consume = (buffer_consume + 1) & PS2_KEYBOARD_BUFFER_MASK;
	return data;
}
