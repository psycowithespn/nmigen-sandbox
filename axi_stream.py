from nmigen import *

"""
From the AMBA 4 AXI4-Stream Protocol Specification:


Handshake process

The TVALID and TREADY handshake determines when information is passed across the interface.
A two-way flow control mechanism enables both the master and slave to control the rate at which
the data and control information is transmitted across the interface. For a transfer to occur
both the TVALID and TREADY signals must be asserted. Either TVALID or TREADY can be asserted
first or both can be asserted in the same ACLK cycle.

A master is not permitted to wait until TREADY is asserted before asserting TVALID. Once TVALID
is asserted it must remain asserted until the handshake occurs.

A slave is permitted to wait for TVALID to be asserted before asserting the corresponding TREADY.

If a slave asserts TREADY, it is permitted to deassert TREADY before TVALID is asserted.
"""

class AxiStream():
    def __init__(self, prefix = "s", tdata_bits = 8, tuser_bits = 0):
        prefix = prefix + "_axis_"
        self.tvalid = Signal(name = prefix + "tvalid")
        self.tready = Signal(name = prefix + "tready")
        self.tdata = Signal(tdata_bits, name = prefix + "tdata")
        self.tlast = Signal(name = prefix + "tlast")
        if (tuser_bits > 0):
            self.tuser = Signal(tuser_bits, name = prefix + "tuser")
        else:
            self.tuser = None

    def ports(self):
        ret = [self.tvalid, self.tready, self.tdata, self.tlast]

        if (self.tuser is not None):
            ret.append(self.tuser)

        return ret

    def tx_done(self):
        return self.tvalid & self.tready

    def link_slave(self, slave):
        ret = [
            self.tready.eq(slave.tready),
            slave.tvalid.eq(self.tvalid),
            slave.tdata.eq(self.tdata),
            slave.tlast.eq(self.tlast),
        ]

        if (self.tuser is not None and slave.tuser is not None):
            ret.append(slave.tuser.eq(self.tuser))

        return ret
