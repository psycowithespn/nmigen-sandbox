from nmigen import *

from axi_stream import AxiStream

def flatten(list):
    return [i for l in list for i in l]

class AxiStreamTx(Elaboratable):
    def __init__(self):
        self.m_axis = AxiStream(prefix = "m")

        self.counter = Signal(8)

    def elaborate(self, platform):
        m = Module()

        m.d.comb += self.m_axis.tvalid.eq(1)
        m.d.comb += self.m_axis.tlast.eq(self.m_axis.tdata == 255)
        m.d.comb += self.m_axis.tdata.eq(self.counter)

        with m.If(self.m_axis.tx_done()):
            m.d.sync += self.counter.eq(self.counter + 1)

        return m

    def ports(self):
        return flatten([self.m_axis.ports()])
