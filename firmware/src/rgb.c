#include <rgb.h>
#include <generated/csr.h>

void rgb_init() {
	rgb_out_write(0b111111111111);
}

void rgb_set(uint8_t led, uint8_t r, uint8_t g, uint8_t b) {
	uint32_t reg = rgb_out_read();
	
	uint8_t offset = led * 3;
	reg |= 0b111 << offset;
	
	if (r > 0) {
		reg &= ~(1 << offset << 0);
	}
	
	if (g > 0) {
		reg &= ~(1 << offset << 1);
	}
	
	if (b > 0) {
		reg &= ~(1 << offset << 2);
	}
	
	rgb_out_write(reg);
}
