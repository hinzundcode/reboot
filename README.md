## helpful commands

### loading firmware over serial

```
$ lxterm --kernel firmware/firmware.bin /dev/cu.usbserial-A600K743
```

### uart crossover

```
$ litex_server --uart --uart-port /dev/cu.usbserial-142401 --uart-baudrate 3000000
$ lxterm --kernel ../firmware/firmware.bin crossover
```

### litescope

```
$ litex_server --uart --uart-port /dev/cu.usbserial-142401 --uart-baudrate 3000000
$ (cd build; litescope_cli)
$ (cd build; litescope_cli -f ps2_keyboard_clk)
```
