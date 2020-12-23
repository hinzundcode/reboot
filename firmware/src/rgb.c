#include <rgb.h>
#include <generated/csr.h>

void rgb_set(uint8_t led, uint8_t r, uint8_t g, uint8_t b) {
	switch (led) {
		case RGB_LED0:
			rgb0_control_write(b << CSR_RGB0_CONTROL_B_OFFSET | g << CSR_RGB0_CONTROL_G_OFFSET | r << CSR_RGB0_CONTROL_R_OFFSET);
			break;
		case RGB_LED1:
			rgb1_control_write(b << CSR_RGB1_CONTROL_B_OFFSET | g << CSR_RGB1_CONTROL_G_OFFSET | r << CSR_RGB1_CONTROL_R_OFFSET);
			break;
		case RGB_LED2:
			rgb2_control_write(b << CSR_RGB2_CONTROL_B_OFFSET | g << CSR_RGB2_CONTROL_G_OFFSET | r << CSR_RGB2_CONTROL_R_OFFSET);
			break;
		case RGB_LED3:
			rgb3_control_write(b << CSR_RGB3_CONTROL_B_OFFSET | g << CSR_RGB3_CONTROL_G_OFFSET | r << CSR_RGB3_CONTROL_R_OFFSET);
			break;
	}
}
