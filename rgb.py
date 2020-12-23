from migen import *
from migen.genlib.cdc import MultiReg
from litex.soc.interconnect.csr import *

class RGBLed(Module, AutoCSR):
	def __init__(self, pins, clock_domain="sys"):
		self.r = Signal(8)
		self.g = Signal(8)
		self.b = Signal(8)
		
		counter_r = Signal(8, reset_less=True)
		counter_g = Signal(8, reset_less=True)
		counter_b = Signal(8, reset_less=True)
		
		sync = getattr(self.sync, clock_domain)
		sync += [
			counter_r.eq(counter_r + 1),
			counter_g.eq(counter_g + 1),
			counter_b.eq(counter_b + 1),
			
			# inverted logic on led pins
			If(counter_r < self.r,
				pins.r.eq(0)
			).Else(
				pins.r.eq(1)
			),
			If(counter_g < self.g,
				pins.g.eq(0)
			).Else(
				pins.g.eq(1)
			),
			If(counter_b < self.b,
				pins.b.eq(0)
			).Else(
				pins.b.eq(1)
			),
		]
		
		self.add_csr(clock_domain)
	
	def add_csr(self, clock_domain):
		self._control = CSRStorage(fields=[
			CSRField("r", size=8, offset=0),
			CSRField("g", size=8, offset=8),
			CSRField("b", size=8, offset=16),
		])
		
		n = 0 if clock_domain == "sys" else 2
		self.specials += [
			MultiReg(self._control.fields.r, self.r, n=n),
			MultiReg(self._control.fields.g, self.g, n=n),
			MultiReg(self._control.fields.b, self.b, n=n),
		]
