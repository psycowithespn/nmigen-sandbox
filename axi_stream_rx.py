from nmigen import *

from axi_stream import AxiStream
from lfsr import Lfsr

def flatten(list):
    return [i for l in list for i in l]

class AxiStreamRx(Elaboratable):
    def __init__(self):
        self.s_axis = AxiStream(prefix = "s", tuser_bits = 100)
        self.lfsr = Lfsr()

    def elaborate(self, platform):
        m = Module()

        m.submodules += self.lfsr

        m.d.comb += self.s_axis.tready.eq(self.lfsr.out[0])

        return m

    def ports(self):
        return flatten([self.s_axis.ports()])
