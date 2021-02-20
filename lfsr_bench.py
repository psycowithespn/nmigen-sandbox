from nmigen.back import verilog
from nmigen.sim import Simulator

from lfsr import Lfsr

dut = Lfsr()


def bench():
    yield dut.en.eq(1)
    for _ in range(100):
        yield


sim = Simulator(dut)
sim.add_clock(1e-6)
sim.add_sync_process(bench)
with sim.write_vcd("lfsr.vcd"):
    sim.run()

with open("lfsr.v", "w") as f:
    f.write(verilog.convert(dut, ports=[dut.out]))
