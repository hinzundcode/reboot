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
		
		clk_d = Signal()
		clk_fall = Signal()
		self.sync += clk_d.eq(pins.clk)
		self.comb += clk_fall.eq(~pins.clk & clk_d)
		
		self.submodules.fsm = fsm = FSM(reset_state="IDLE")
		fsm.act("IDLE",
			idle.eq(1),
			If(clk_fall,
				NextValue(byte, 0),
				NextValue(count, 0),
				NextValue(parity, 0),
				NextValue(xor_sum, 0),
				NextState("SAMPLE-BIT")
			)
		)
		fsm.act("SAMPLE-BIT",
			If(clk_fall,
				NextValue(byte, pins.data << 7 | byte >> 1),
				NextValue(xor_sum, xor_sum ^ pins.data),
				NextValue(count, count + 1),
				If(count == 7,
					NextState("WAIT-PARITY")
				).Else(
					NextState("SAMPLE-BIT")
				)
			)
		)
		fsm.act("WAIT-PARITY",
			If(clk_fall,
				NextValue(parity, pins.data),
				NextState("WAIT-STOP"))
		)
		fsm.act("WAIT-STOP",
			If(clk_fall,
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

def testbench(pins):
	def send_bit(bit):
		yield pins.data.eq(bit)
		yield
		yield pins.clk.eq(0)
		yield
		yield pins.clk.eq(1)
		yield
	
	yield
	
	for bit in [0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1]:
		yield from send_bit(bit)
	
	yield
	yield
	
	yield pins.clk.eq(1)
	yield pins.data.eq(1)
	yield
	

if __name__ == "__main__":
	pins = Record([
		("clk", 1),
		("data", 1),
	], reset=1)
	ps2 = PS2(pins)
	run_simulation(ps2, testbench(pins), vcd_name="ps2.vcd")
