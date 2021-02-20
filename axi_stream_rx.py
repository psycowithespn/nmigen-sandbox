from nmigen import *

from axi_stream import AxiStream
from lfsr import Lfsr

def flatten(list):
    return [i for l in list for i in l]

class AxiStreamRx(Elaboratable):
    def __init__(self):
        self.s_axis = AxiStream(prefix = "s", tuser_bits = 100)
        self.lfsr = Lfsr()
        self.rx_byte_count = Signal(32)

    def elaborate(self, platform):
        m = Module()

        m.submodules += self.lfsr

        m.d.comb += self.lfsr.en.eq(1)
        m.d.comb += self.s_axis.tready.eq(self.lfsr.out[0])

        with m.If(self.s_axis.tx_done()):
            m.d.sync += self.rx_byte_count.eq(self.rx_byte_count + 1)

        return m

    def ports(self):
        return flatten([self.s_axis.ports()])
