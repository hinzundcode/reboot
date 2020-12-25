# copied and adapted from litex_boards/platforms/ecpix5.py

from litex.build.generic_platform import *
from litex.build.lattice import LatticePlatform
from litex.build.openfpgaloader import OpenFPGALoader

_io = [
	# Clk / Rst
	("clk100", 0, Pins("K23"), IOStandard("LVCMOS33")),
	("rst_n",  0, Pins("N5"),  IOStandard("LVCMOS33")),

	# Leds
	("rgb_led", 0,
		Subsignal("r", Pins("T23")),
		Subsignal("g", Pins("R21")),
		Subsignal("b", Pins("T22")),
		IOStandard("LVCMOS33"),
	),
	("rgb_led", 1,
		Subsignal("r", Pins("U21")),
		Subsignal("g", Pins("W21")),
		Subsignal("b", Pins("T24")),
		IOStandard("LVCMOS33"),
	),
	("rgb_led", 2,
		Subsignal("r", Pins("K21")),
		Subsignal("g", Pins("K24")),
		Subsignal("b", Pins("M21")),
		IOStandard("LVCMOS33"),
	),
	("rgb_led", 3,
		Subsignal("r", Pins("P21")),
		Subsignal("g", Pins("R23")),
		Subsignal("b", Pins("P22")),
		IOStandard("LVCMOS33"),
	),

	# Serial
	("serial", 0,
		Subsignal("rx", Pins("R26"), IOStandard("LVCMOS33")),
		Subsignal("tx", Pins("R24"), IOStandard("LVCMOS33")),
	),

	# DDR3 SDRAM
	("ddram", 0,
		Subsignal("a", Pins(
			"T5 M3 L3 V6 K2 W6 K3 L1",
			"H2 L2 N1 J1 M1 K1"),
			IOStandard("SSTL15_I")),
		Subsignal("ba",    Pins("U6 N3 N4"), IOStandard("SSTL15_I")),
		Subsignal("ras_n", Pins("T3"), IOStandard("SSTL15_I")),
		Subsignal("cas_n", Pins("P2"), IOStandard("SSTL15_I")),
		Subsignal("we_n",  Pins("R3"), IOStandard("SSTL15_I")),
		Subsignal("dm", Pins("U4 U1"), IOStandard("SSTL15_I")),
		Subsignal("dq", Pins(
			"T4 W4 R4 W5 R6 P6 P5 P4",
			"R1 W3 T2 V3 U3 W1 T1 W2",),
			IOStandard("SSTL15_I"),
			Misc("TERMINATION=75")),
		Subsignal("dqs_p", Pins("V4 V1"), IOStandard("SSTL15D_I"),
			Misc("TERMINATION=OFF"),
			Misc("DIFFRESISTOR=100")),
		Subsignal("clk_p", Pins("H3"), IOStandard("SSTL15D_I")),
		Subsignal("cke",   Pins("P1"), IOStandard("SSTL15_I")),
		Subsignal("odt",   Pins("P3"), IOStandard("SSTL15_I")),
		Misc("SLEWRATE=FAST"),
	),
]

_connectors = [
	("pmod0", "T25 U25 U24 V24 T26 U26 V26 W26"),
	("pmod1", "U23 V23 U22 V21 W25 W24 W23 W22"),
	("pmod2", "J24 H22 E21 D18 K22 J21 H21 D22"),
	("pmod3", "E4 F4 E6 H4 F3 D4 D5 F5"),
	("pmod4", "E26 D25 F26 F25 C26 C25 A25 A24"),
	("pmod5", "D19 C21 B21 C22 D21 A21 A22 A23"),
	("pmod6", "C16 B17 C18 B19 A17 A18 A19 C19"),
	("pmod7", "D14 B14 E14 B16 C14 A14 A15 A16"),
]

class BasePlatform(LatticePlatform):
	default_clk_name   = "clk100"
	default_clk_period = 1e9/100e6
	
	def create_programmer(self):
		return OpenFPGALoader("ecpix5")
	
	def do_finalize(self, fragment):
		LatticePlatform.do_finalize(self, fragment)
		self.add_period_constraint(self.lookup_request("clk100", loose=True), 1e9/100e6)
		self.add_period_constraint(self.lookup_request("eth_clocks:rx", 0, loose=True), 1e9/125e6)

class ECPIX545Platform(BasePlatform):
	def __init__(self, toolchain="trellis", **kwargs):
		LatticePlatform.__init__(self, "LFE5UM5G-45F-8BG554C", _io, _connectors, toolchain=toolchain, **kwargs)

class ECPIX585Platform(BasePlatform):
	def __init__(self, toolchain="trellis", **kwargs):
		LatticePlatform.__init__(self, "LFE5UM5G-85F-8BG554I", _io, _connectors, toolchain=toolchain, **kwargs)
