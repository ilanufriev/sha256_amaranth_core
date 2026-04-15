# SPDX-License-Identifier: BSD-3-Clause
# SPDX-FileCopyrightText: 2026 Ilia Anufriev

import amaranth as am

from amaranth.back import verilog

import amaranth.lib.wiring as wiring
from amaranth.lib.wiring import (
        In,
        Out,
        Signal,
        )


H_CONST = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
]


K_CONST = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
    0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
    0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
    0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
    0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
    0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
    0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
    0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
    0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
    0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
    0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
    0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
    0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
    0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
    0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
]


# Verilog-style async ROM because amaranth's Arrays
# aggravate me
class K_storage(wiring.Component):
    round_i: In(6)
    k_o: Out(32, init=0x428a2f98)

    def __init__(self):
        super().__init__()

    def elaborate(self, platform):
        m = am.Module()

        with m.Switch(self.round_i):
            for i in range(64):
                with m.Case(i):
                    m.d.comb += self.k_o.eq(K_CONST[i])
            with m.Case():
                m.d.comb += self.k_o.eq(K_CONST[0]);

        return m


def _s0(a):
    return a.rotate_right(2) ^ a.rotate_right(13) ^ a.rotate_right(22)


def _s1(e):
    return e.rotate_right(6) ^ e.rotate_right(11) ^ e.rotate_right(25)


def _ch(e, f, g):
    return (e & f) ^ ((~e) & g)


def _maj(a, b, c):
    return (a & (b ^ c)) ^ (b & c)


class Sha256(wiring.Component):
    """SHA-256 hash function implementation.
    Inputs:
        - block_i - block of data. Note, that this module
          does not perform padding, this has to be done by
          the user beforehand. Last byte in the sequence that
          needs to be hashed must be placed into LSB of the block.
        - valid_i - shows that the input data is valid.
          Module starts working as soon as valid_i is driven
          to VCC.
        - hash_o - digest of the current block of data. Note
          that the internal state of the module does not get
          reset between block digestion runs. So if one wants
          to hash a new set of blocks, they must first reset the
          module with rst signal driven to VCC.
        - ready_o - shows that the module is ready to receive new
          data. It is driven to GND when module is digesting the
          block.
    """

    block_i:  In(512)
    valid_i:  In(1)
    first_i:  In(1)

    hash_o:   Out(256)
    ready_o:  Out(1, init=1)

    def __init__(self):
        super().__init__()
        self.k_storage = K_storage()

    def get_byte(self, signal: Signal, index: int):
        return signal.bit_select(index * 8, 8)

    def elaborate(self, platform):
        m = am.Module()
        m.submodules += [self.k_storage]

        w = am.Array(Signal(32, init=0, name=f"w_{igen}") for igen in range(16))
        w_i = Signal(32, init=0)
        k_i = Signal(32, init=0)

        i      = Signal(32, init=1)
        cstep  = Signal(4, init=0)
        temp1  = Signal(32, init=0)
        temp2  = Signal(32, init=0)

        h_ = [Signal(32, init=H_CONST[igen], name=f"h_{igen}") for igen in range(8)]

        a = Signal(32, init=0)
        b = Signal(32, init=0)
        c = Signal(32, init=0)
        d = Signal(32, init=0)
        e = Signal(32, init=0)
        f = Signal(32, init=0)
        g = Signal(32, init=0)
        h = Signal(32, init=0)

        # Connect submodule's ports to this module's wires
        m.d.comb += [
            self.k_storage.round_i.eq(i),
            k_i.eq(self.k_storage.k_o),
            ]

        # Intermediate variables
        m.d.comb += [
            temp1.eq(h + _s1(e) + _ch(e, f, g) + k_i + w_i),
            temp2.eq(_s0(a) + _maj(a, b, c)),
            ]

        t1 = Signal(32, init=0)
        t2 = Signal(32, init=0)

        # Schedule array expansion
        with m.If(i > 15):
            m.d.comb += [
                t1.eq((w[1].rotate_right(7)) ^ (w[1].rotate_right(18)) ^ (w[1] >> 3)),
                t2.eq((w[14].rotate_right(17)) ^ (w[14].rotate_right(19)) ^ (w[14] >> 10)),
                w_i.eq(w[0] + t1 + w[9] + t2),
                ]
        with m.Else():
            m.d.comb += [
                t1.eq(0),
                t2.eq(0),
                w_i.eq(w[0]),
                ]

        with m.Switch(cstep):

            # ====== init stage ======
            with m.Case(0):
                with m.If(self.valid_i):
                    for igen in range(16):
                        m.d.sync += [
                            w[15 - igen].eq(self.block_i.bit_select(igen * 32, 32)),
                            ]

                    with m.If(self.first_i):
                        for igen in range(8):
                            m.d.sync += h_[igen].eq(h_[igen].init)

                        m.d.sync += [
                            a.eq(h_[0].init),
                            b.eq(h_[1].init),
                            c.eq(h_[2].init),
                            d.eq(h_[3].init),
                            e.eq(h_[4].init),
                            f.eq(h_[5].init),
                            g.eq(h_[6].init),
                            h.eq(h_[7].init),
                            ]

                    with m.Else():
                        m.d.sync += [
                            a.eq(h_[0]),
                            b.eq(h_[1]),
                            c.eq(h_[2]),
                            d.eq(h_[3]),
                            e.eq(h_[4]),
                            f.eq(h_[5]),
                            g.eq(h_[6]),
                            h.eq(h_[7]),
                            ]

                    m.d.sync += [
                        i.eq(0),
                        self.ready_o.eq(0),
                        cstep.eq(cstep + 1),
                        ]

            # ====== for i from 0 to 64 loop start ======
            with m.Case(1):
                with m.If(i < 64):
                    m.d.sync += [
                        h.eq(g),
                        g.eq(f),
                        f.eq(e),
                        e.eq(d + temp1),
                        d.eq(c),
                        c.eq(b),
                        b.eq(a),
                        a.eq(temp1 + temp2),
                        ]

                    for igen in range(15):
                        m.d.sync += w[igen].eq(w[igen + 1])

                    m.d.sync += w[15].eq(w_i)

                    m.d.sync += [
                        i.eq(i + 1),
                        ]

                with m.Else():
                    m.d.sync += [
                        i.eq(0),
                        cstep.eq(cstep + 1),  # go out of the loop
                        ]

            # ====== Finalize results ======
            with m.Case(2):
                m.d.sync += [
                    h_[0].eq(h_[0] + a),
                    h_[1].eq(h_[1] + b),
                    h_[2].eq(h_[2] + c),
                    h_[3].eq(h_[3] + d),
                    h_[4].eq(h_[4] + e),
                    h_[5].eq(h_[5] + f),
                    h_[6].eq(h_[6] + g),
                    h_[7].eq(h_[7] + h),

                    cstep.eq(cstep + 1),
                    ]

            with m.Case(3):
                global_b_idx = 0
                for h_idx in range(7, -1, -1):
                    for b_idx in range(4):
                        m.d.sync += [
                            self.get_byte(self.hash_o, global_b_idx).eq(
                                    self.get_byte(h_[h_idx], b_idx)
                                    )
                            ]
                        global_b_idx += 1
                m.d.sync += [
                    self.ready_o.eq(1),
                    cstep.eq(0),
                    ]

        return m

if __name__ == "__main__":
    sha256 = Sha256()
    with open("sha256.v", "w") as f:
        f.write(verilog.convert(sha256, name="sha256"))
