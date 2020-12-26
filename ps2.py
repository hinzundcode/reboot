from migen import *

class PS2(Module):
	def __init__(self, pins):
		byte = Signal(8)
		count = Signal(3)
		parity = Signal()
		xor_sum = Signal()
		
		idle = Signal()
		done = Signal()
		error = Signal()
		
		self.submodules.fsm = fsm = FSM(reset_state="IDLE")
		fsm.act("IDLE",
			idle.eq(1),
			If(~pins.clk,
				NextValue(byte, 0),
				NextValue(count, 0),
				NextValue(parity, 0),
				NextValue(xor_sum, 0),
				NextState("WAIT-START-UP")
			)
		)
		fsm.act("WAIT-START-UP",
			If(pins.clk,
				NextState("SAMPLE-BIT"))
		)
		fsm.act("SAMPLE-BIT",
			If(~pins.clk,
				NextValue(byte, pins.data << 7 | byte >> 1),
				NextValue(xor_sum, xor_sum ^ pins.data),
				NextValue(count, count + 1),
				NextState("WAIT-BIT-UP")
			)
		)
		fsm.act("WAIT-BIT-UP",
			If(pins.clk,
				If(count == 0,
					NextState("WAIT-PARITY")
				).Else(
					NextState("SAMPLE-BIT")
				)
			)
		)
		fsm.act("WAIT-PARITY",
			If(~pins.clk,
				NextValue(parity, pins.data),
				NextState("WAIT-PARITY-UP"))
		)
		fsm.act("WAIT-PARITY-UP",
			If(pins.clk,
				NextState("WAIT-STOP"))
		)
		fsm.act("WAIT-STOP",
			If(~pins.clk,
				NextState("WAIT-STOP-UP"))
		)
		fsm.act("WAIT-STOP-UP",
			If(pins.clk,
				# xor_sum is 0 on even number of ones
				# ps2 parity bit is 1 on even number of ones
				If(parity == xor_sum,
					NextState("ERROR")
				).Else(
					NextState("DONE")
				)
			)
		)
		fsm.act("DONE",
			done.eq(1)
		)
		fsm.act("ERROR",
			error.eq(1)
		)

def testbench(clk, data):
	def send_bit(bit):
		yield data.eq(bit)
		yield
		yield clk.eq(0)
		yield
		yield clk.eq(1)
		yield
	
	yield
	
	for bit in [0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1]:
		yield from send_bit(bit)
	
	yield
	yield
	
	yield clk.eq(1)
	yield data.eq(1)
	yield
	

if __name__ == "__main__":
	clk = Signal(reset=1)
	data = Signal(reset=1)
	class Pins():
		def __init__(self, clk, data):
			self.clk = clk
			self.data = data
	ps2 = PS2(Pins(clk, data))
	
	run_simulation(ps2, testbench(clk, data), vcd_name="ps2.vcd")
