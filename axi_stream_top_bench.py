from nmigen.back import verilog
from nmigen.sim import Simulator

from axi_stream_top import AxiStreamTop

dut = AxiStreamTop()

def bench():
    for _ in range(1000):
        yield

sim = Simulator(dut)
sim.add_clock(1e-6)
sim.add_sync_process(bench)
with sim.write_vcd("axi_stream_top.vcd"):
    sim.run()

with open("axi_stream_top.v", "w") as f:
    f.write(verilog.convert(dut))
