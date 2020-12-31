# copied from litex/soc/software/demo/ and adapted

BUILD_DIR?=../build/

include $(BUILD_DIR)/software/include/generated/variables.mak
include $(SOC_DIRECTORY)/software/common.mak

OBJ_DIR=.obj
SRC_DIR=src

CSOURCES = $(wildcard $(SRC_DIR)/*.c)
COBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(CSOURCES:.c=.o)))
ASMSOURCES = $(wildcard $(SRC_DIR)/*.S)
ASMOBJS = $(addprefix $(OBJ_DIR)/, $(notdir $(ASMSOURCES:.S=.o)))
OBJECTS = $(COBJS) $(ASMOBJS)

CFLAGS = $(COMMONFLAGS) -Iinclude

all: firmware.bin

# pull in dependency info for *existing* .o files
-include $(OBJECTS:.o=.d)

%.bin: %.elf
	$(OBJCOPY) -O binary $< $@
	chmod -x $@

firmware.elf: $(OBJECTS)
	$(LD) $(LDFLAGS) \
		-T linker.ld \
		-N -o $@ \
		 $(BUILD_DIR)/software/libbase/crt0.o \
		$(OBJECTS) \
		-L$(BUILD_DIR)/software/libbase \
		-L$(BUILD_DIR)/software/libcompiler_rt \
		-lbase-nofloat -lcompiler_rt
	chmod -x $@

$(OBJECTS): | $(OBJ_DIR)

$(OBJ_DIR):
	mkdir $(OBJ_DIR)

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.c
	$(compile)

$(OBJ_DIR)/%.o: $(SRC_DIR)/%.S
	$(assemble)

clean:
	$(RM) $(OBJECTS) $(OBJECTS:.o=.d) firmware.elf firmware.bin

.PHONY: all main.o clean load
