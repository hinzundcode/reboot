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

from litex_boards.targets.ecpix5 import _CRG, BaseSoC

from litex.build.openfpgaloader import OpenFPGALoader

class SoC(BaseSoC):
	def __init__(self, sys_clk_freq=int(75e6), **kwargs):
		BaseSoC.__init__(self, sys_clk_freq, **kwargs)

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
	
	soc = SoC(**soc_core_argdict(args))
	
	builder = Builder(soc,
		**builder_argdict(args))
	
	#print(trellis_argdict(args))
	#exit()
	
	if args.build:
		builder.build(**trellis_argdict(args), run=args.build)
	
	if args.load or args.flash:
		prog = OpenFPGALoader("ecpix5")
		prog.load_bitstream(os.path.join(builder.gateware_dir, soc.platform.name + ".bit"), args.flash)

if __name__ == "__main__":
	main()
