from nmigen import *

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

    def link_slave(self, m, slave):
        m.d.comb += self.tready.eq(slave.tready)
        m.d.comb += slave.tvalid.eq(self.tvalid)
        m.d.comb += slave.tdata.eq(self.tdata)
        m.d.comb += slave.tlast.eq(self.tlast)

        if (self.tuser is not None and slave.tuser is not None):
            m.d.comb += slave.tuser.eq(self.tuser)
