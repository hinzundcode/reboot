from migen import *
from migen.genlib.cdc import MultiReg
from litex.soc.interconnect.csr import *

class PS2(Module, AutoCSR):
	def __init__(self, pins):
		self.value = Signal(8)
		self.count = Signal(3)
		
		self.done = Signal()
		self.error = Signal()
		self.clear = Signal()
		
		self.parity = Signal()
		self.xor_sum = Signal()
		
		self.clock = Signal(reset=1)
		self.data = Signal(reset=1)
		self.falling = Signal()
		
		self.specials += [
			MultiReg(pins.clk, self.clock, reset=1),
			MultiReg(pins.data, self.data, reset=1),
		]
		
		clock_s = Signal(reset=1)
		clock_r = Signal(reset=1)
		self.sync += [
			clock_s.eq(self.clock),
			clock_r.eq(clock_s),
			self.falling.eq(~clock_r & clock_s),
		]
		
		self.submodules.fsm = fsm = FSM(reset_state="IDLE")
		fsm.act("IDLE",
			If(self.falling,
				NextState("SAMPLE-BIT")
			)
		)
		fsm.act("SAMPLE-BIT",
			If(self.falling,
				NextValue(self.value, self.data << 7 | self.value >> 1),
				NextValue(self.xor_sum, self.xor_sum ^ self.data),
				If(self.count == 7,
					NextState("WAIT-PARITY")
				).Else(
					NextValue(self.count, self.count + 1),
					NextState("SAMPLE-BIT")
				)
			)
		)
		fsm.act("WAIT-PARITY",
			If(self.falling,
				NextValue(self.parity, self.data),
				NextState("WAIT-STOP"))
		)
		fsm.act("WAIT-STOP",
			If(self.falling,
				# xor_sum is 0 on even number of ones
				# ps2 parity bit is 1 on even number of ones
				If(self.parity == self.xor_sum,
					NextValue(self.error, 1)
				),
				NextState("DONE")
			)
		)
		fsm.act("DONE",
			self.done.eq(1),
			If(self.clear,
				NextValue(self.value, 0),
				NextValue(self.count, 0),
				NextValue(self.parity, 0),
				NextValue(self.xor_sum, 0),
				NextValue(self.error, 0),
				NextState("IDLE")
			)
		)
		
		self.add_csr()
	
	def add_csr(self):
		self._status = CSRStatus(fields=[
			CSRField("done", size=1, offset=0),
			CSRField("error", size=1, offset=1),
		])
		self._control = CSRStorage(fields=[
			CSRField("clear", size=1, offset=0, pulse=True),
		])
		self._data = CSRStatus(8)
		
		self.comb += [
			self._status.fields.done.eq(self.done),
			self._status.fields.error.eq(self.error),
			self._data.status.eq(self.value),
			self.clear.eq(self._control.fields.clear),
		]

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
