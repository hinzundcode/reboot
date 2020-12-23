import os
import argparse
import sys

from migen import *
from migen.genlib.resetsync import AsyncResetSynchronizer

from litex_boards.platforms import ecpix5

from litex.build.lattice.trellis import trellis_args, trellis_argdict

from litex.soc.cores.clock import *
from litex.soc.integration.soc_core import *
from litex.soc.integration.builder import *

from litedram.modules import MT41K256M16
from litedram.phy import ECP5DDRPHY

from liteeth.phy.ecp5rgmii import LiteEthPHYRGMII

from litex_boards.targets.ecpix5 import _CRG

from litex.build.openfpgaloader import OpenFPGALoader

from platform import ECPIX545Platform

class SoC(SoCCore):
	def __init__(self, platform, sys_clk_freq=int(75e6), **kwargs):
		SoCCore.__init__(self, platform, sys_clk_freq, **kwargs)
		
		self.submodules.crg = _CRG(platform, sys_clk_freq)
		
		self.submodules.ddrphy = ECP5DDRPHY(
			platform.request("ddram"),
			sys_clk_freq=sys_clk_freq)
		self.add_csr("ddrphy")
		self.comb += self.crg.stop.eq(self.ddrphy.init.stop)
		self.comb += self.crg.reset.eq(self.ddrphy.init.reset)
		self.add_sdram("sdram",
				phy                     = self.ddrphy,
				module                  = MT41K256M16(sys_clk_freq, "1:2"),
				origin                  = self.mem_map["main_ram"],
				size                    = kwargs.get("max_sdram_size", 0x40000000),
				l2_cache_size           = kwargs.get("l2_size", 8192),
				l2_cache_min_data_width = kwargs.get("min_l2_data_width", 128),
				l2_cache_reverse        = True
		)
		

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("--build", action="store_true")
	parser.add_argument("--load", action="store_true")
	parser.add_argument("--flash", action="store_true")
	
	builder_args(parser)
	soc_core_args(parser)
	trellis_args(parser)
	
	parser.set_defaults(
		output_dir="build",
		csr_csv="build/csr.csv"
	)
	
	args = parser.parse_args()
	
	platform = ECPIX545Platform(toolchain="trellis")
	soc = SoC(platform, **soc_core_argdict(args))
	
	builder = Builder(soc,
		**builder_argdict(args))
	
	if args.build:
		builder.build(**trellis_argdict(args))
	
	if args.load or args.flash:
		prog = soc.platform.create_programmer()
		prog.load_bitstream(os.path.join(builder.gateware_dir, soc.platform.name + ".bit"), args.flash)

if __name__ == "__main__":
	main()
