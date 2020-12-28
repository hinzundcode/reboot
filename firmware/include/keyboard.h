#ifndef __KEYBOARD_H
#define __KEYBOARD_H

#define KEY_0 0x45
#define KEY_1 0x16
#define KEY_2 0x1E
#define KEY_3 0x26
#define KEY_4 0x25
#define KEY_5 0x2E
#define KEY_6 0x36
#define KEY_7 0x3D
#define KEY_8 0x3E
#define KEY_9 0x46
#define KEY_A 0x1C
#define KEY_AE 0x52
#define KEY_ALT 0x11
#define KEY_B 0x32
#define KEY_BACKSPACE 0x66
#define KEY_BACKTICK 0x55
#define KEY_C 0x21
#define KEY_CAPSLOCK 0x58
#define KEY_CARET 0xE
#define KEY_COMMA 0x41
#define KEY_D 0x23
#define KEY_E 0x24
#define KEY_ENTER 0x5A
#define KEY_ESC 0x76
#define KEY_F 0x2B
#define KEY_F1 0x5
#define KEY_F10 0x9
#define KEY_F11 0x78
#define KEY_F12 0x7
#define KEY_F2 0x6
#define KEY_F3 0x4
#define KEY_F4 0xC
#define KEY_F5 0x3
#define KEY_F6 0xB
#define KEY_F7 0x83
#define KEY_F8 0xA
#define KEY_F9 0x1
#define KEY_G 0x34
#define KEY_H 0x33
#define KEY_HASH 0x5D
#define KEY_I 0x43
#define KEY_J 0x3B
#define KEY_K 0x42
#define KEY_L 0x4B
#define KEY_LEFT_CTRL 0x14
#define KEY_LEFT_SHIFT 0x12
#define KEY_LESS 0x61
#define KEY_M 0x3A
#define KEY_MINUS 0x4A
#define KEY_N 0x31
#define KEY_NUMLOCK 0x77
#define KEY_NUMPAD_0 0x70
#define KEY_NUMPAD_1 0x69
#define KEY_NUMPAD_2 0x72
#define KEY_NUMPAD_3 0x7A
#define KEY_NUMPAD_4 0x6B
#define KEY_NUMPAD_5 0x73
#define KEY_NUMPAD_6 0x74
#define KEY_NUMPAD_7 0x6C
#define KEY_NUMPAD_8 0x75
#define KEY_NUMPAD_9 0x7D
#define KEY_NUMPAD_ASTERISK 0x7C
#define KEY_NUMPAD_COMMA 0x71
#define KEY_NUMPAD_MINUS 0x7B
#define KEY_NUMPAD_PLUS 0x79
#define KEY_O 0x44
#define KEY_OE 0x4C
#define KEY_P 0x4D
#define KEY_PERIOD 0x49
#define KEY_PLUS 0x5B
#define KEY_Q 0x15
#define KEY_R 0x2D
#define KEY_RIGHT_SHIFT 0x59
#define KEY_S 0x1B
#define KEY_SPACE 0x29
#define KEY_SS 0x4E
#define KEY_T 0x2C
#define KEY_TAB 0xD
#define KEY_U 0x3C
#define KEY_UE 0x54
#define KEY_V 0x2A
#define KEY_W 0x1D
#define KEY_X 0x22
#define KEY_Y 0x1A
#define KEY_Z 0x35

#define KEY_ALT_GR 0x111
#define KEY_RIGHT_CTRL 0x114
#define KEY_LEFT_META 0x11F
#define KEY_RIGHT_META 0x127
#define KEY_NUMPAD_DIVIDE 0x14A
#define KEY_NUMPAD_ENTER 0x15A
#define KEY_LEFT 0x165
#define KEY_END 0x169
#define KEY_HOME 0x16C
#define KEY_INSERT 0x170
#define KEY_DELETE 0x171
#define KEY_DOWN 0x172
#define KEY_RIGHT 0x174
#define KEY_UP 0x175
#define KEY_PAGE_DOWN 0x17A
#define KEY_PAGE_UP 0x17D
#define KEY_SCROLL_LOCK 0x17E

void keyboard_service();

#endif
