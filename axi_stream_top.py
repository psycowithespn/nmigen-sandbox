from nmigen import *

from axi_stream_rx import AxiStreamRx
from axi_stream_tx import AxiStreamTx

class AxiStreamTop(Elaboratable):
    def __init__(self):
        self.rx = AxiStreamRx()
        self.tx = AxiStreamTx()

    def elaborate(self, platform):
        m = Module()

        m.submodules += [self.rx, self.tx]
        self.tx.m_axis.link_slave(m, self.rx.s_axis)

        return m
