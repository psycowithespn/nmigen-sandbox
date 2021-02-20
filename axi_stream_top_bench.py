from nmigen.back import verilog
from nmigen.sim import Simulator

from axi_stream_top import AxiStreamTop

dut = AxiStreamTop()


def bench():
    tvalid_last = 0
    tvalid_can_fall = 0
    for i in range(2000):
        yield
        # Check that TVALID never goes low until the transmission completes.
        tvalid = (yield dut.tx.m_axis.tvalid)
        tx_done = (yield dut.tx.m_axis.tx_done())
        # Don't care about no change in tvalid.
        # Don't care if tvalid is high.
        # Only allow tvalid to fall the cycle after a tx_done.
        assert((tvalid == tvalid_last) or (tvalid) or (tvalid_can_fall))
        tvalid_can_fall = tx_done
        tvalid_last = tvalid


sim = Simulator(dut)
sim.add_clock(1e-6)
sim.add_sync_process(bench)
with sim.write_vcd("axi_stream_top.vcd"):
    sim.run()

with open("axi_stream_top.v", "w") as f:
    f.write(verilog.convert(dut))
