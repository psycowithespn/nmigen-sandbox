from nmigen import *

class UpCounter(Elaboratable):
    def __init__(self, limit):
        self.limit = limit
        self.en = Signal()
        self.ovf = Signal()

        self.count = Signal(limit.bit_length())

    def elaborate(self, platform):
        m = Module()

        m.d.comb += self.ovf.eq(self.count == self.limit)

        with m.If(self.en):
            with m.If(self.ovf):
                m.d.sync += self.count.eq(0)
            with m.Else():
                m.d.sync += self.count.eq(self.count + 1)

        return m
