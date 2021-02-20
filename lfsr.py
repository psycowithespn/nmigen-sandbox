from nmigen import *

class Lfsr(Elaboratable):
    def __init__(self, out_bit_len = 16, init_state = 0xACE1, tap_mask = 0x002D):
        self.en = Signal()
        self.out = Signal(out_bit_len, reset = init_state)
        self.tap_mask = Const(tap_mask)

    def elaborate(self, platform):
        m = Module()

        with m.If(self.en):
            m.d.sync += self.out.eq(Cat(self.out.shift_right(1), (self.out & self.tap_mask).xor()))

        return m
