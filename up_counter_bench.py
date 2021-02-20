from nmigen.back import verilog
from nmigen.sim import Simulator

from up_counter import UpCounter

dut = UpCounter(25)


def bench():
    yield dut.en.eq(0)
    for _ in range(30):
        yield
        assert not (yield dut.ovf)

    yield dut.en.eq(1)
    for _ in range(25):
        yield
        assert not (yield dut.ovf)
    yield
    assert (yield dut.ovf)

    yield
    assert not (yield dut.ovf)


sim = Simulator(dut)
sim.add_clock(1e-6)
sim.add_sync_process(bench)
with sim.write_vcd("up_counter.vcd"):
    sim.run()

with open("up_counter.v", "w") as f:
    f.write(verilog.convert(dut, ports=[dut.en, dut.ovf]))
