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
            with m.Case(0):
                m.d.comb += self.k_o.eq(0x428a2f98)
            with m.Case(1):
                m.d.comb += self.k_o.eq(0x71374491)
            with m.Case(2):
                m.d.comb += self.k_o.eq(0xb5c0fbcf)
            with m.Case(3):
                m.d.comb += self.k_o.eq(0xe9b5dba5)
            with m.Case(4):
                m.d.comb += self.k_o.eq(0x3956c25b)
            with m.Case(5):
                m.d.comb += self.k_o.eq(0x59f111f1)
            with m.Case(6):
                m.d.comb += self.k_o.eq(0x923f82a4)
            with m.Case(7):
                m.d.comb += self.k_o.eq(0xab1c5ed5)
            with m.Case(8):
                m.d.comb += self.k_o.eq(0xd807aa98)
            with m.Case(9):
                m.d.comb += self.k_o.eq(0x12835b01)
            with m.Case(10):
                m.d.comb += self.k_o.eq(0x243185be)
            with m.Case(11):
                m.d.comb += self.k_o.eq(0x550c7dc3)
            with m.Case(12):
                m.d.comb += self.k_o.eq(0x72be5d74)
            with m.Case(13):
                m.d.comb += self.k_o.eq(0x80deb1fe)
            with m.Case(14):
                m.d.comb += self.k_o.eq(0x9bdc06a7)
            with m.Case(15):
                m.d.comb += self.k_o.eq(0xc19bf174)
            with m.Case(16):
                m.d.comb += self.k_o.eq(0xe49b69c1)
            with m.Case(17):
                m.d.comb += self.k_o.eq(0xefbe4786)
            with m.Case(18):
                m.d.comb += self.k_o.eq(0x0fc19dc6)
            with m.Case(19):
                m.d.comb += self.k_o.eq(0x240ca1cc)
            with m.Case(20):
                m.d.comb += self.k_o.eq(0x2de92c6f)
            with m.Case(21):
                m.d.comb += self.k_o.eq(0x4a7484aa)
            with m.Case(22):
                m.d.comb += self.k_o.eq(0x5cb0a9dc)
            with m.Case(23):
                m.d.comb += self.k_o.eq(0x76f988da)
            with m.Case(24):
                m.d.comb += self.k_o.eq(0x983e5152)
            with m.Case(25):
                m.d.comb += self.k_o.eq(0xa831c66d)
            with m.Case(26):
                m.d.comb += self.k_o.eq(0xb00327c8)
            with m.Case(27):
                m.d.comb += self.k_o.eq(0xbf597fc7)
            with m.Case(28):
                m.d.comb += self.k_o.eq(0xc6e00bf3)
            with m.Case(29):
                m.d.comb += self.k_o.eq(0xd5a79147)
            with m.Case(30):
                m.d.comb += self.k_o.eq(0x06ca6351)
            with m.Case(31):
                m.d.comb += self.k_o.eq(0x14292967)
            with m.Case(32):
                m.d.comb += self.k_o.eq(0x27b70a85)
            with m.Case(33):
                m.d.comb += self.k_o.eq(0x2e1b2138)
            with m.Case(34):
                m.d.comb += self.k_o.eq(0x4d2c6dfc)
            with m.Case(35):
                m.d.comb += self.k_o.eq(0x53380d13)
            with m.Case(36):
                m.d.comb += self.k_o.eq(0x650a7354)
            with m.Case(37):
                m.d.comb += self.k_o.eq(0x766a0abb)
            with m.Case(38):
                m.d.comb += self.k_o.eq(0x81c2c92e)
            with m.Case(39):
                m.d.comb += self.k_o.eq(0x92722c85)
            with m.Case(40):
                m.d.comb += self.k_o.eq(0xa2bfe8a1)
            with m.Case(41):
                m.d.comb += self.k_o.eq(0xa81a664b)
            with m.Case(42):
                m.d.comb += self.k_o.eq(0xc24b8b70)
            with m.Case(43):
                m.d.comb += self.k_o.eq(0xc76c51a3)
            with m.Case(44):
                m.d.comb += self.k_o.eq(0xd192e819)
            with m.Case(45):
                m.d.comb += self.k_o.eq(0xd6990624)
            with m.Case(46):
                m.d.comb += self.k_o.eq(0xf40e3585)
            with m.Case(47):
                m.d.comb += self.k_o.eq(0x106aa070)
            with m.Case(48):
                m.d.comb += self.k_o.eq(0x19a4c116)
            with m.Case(49):
                m.d.comb += self.k_o.eq(0x1e376c08)
            with m.Case(50):
                m.d.comb += self.k_o.eq(0x2748774c)
            with m.Case(51):
                m.d.comb += self.k_o.eq(0x34b0bcb5)
            with m.Case(52):
                m.d.comb += self.k_o.eq(0x391c0cb3)
            with m.Case(53):
                m.d.comb += self.k_o.eq(0x4ed8aa4a)
            with m.Case(54):
                m.d.comb += self.k_o.eq(0x5b9cca4f)
            with m.Case(55):
                m.d.comb += self.k_o.eq(0x682e6ff3)
            with m.Case(56):
                m.d.comb += self.k_o.eq(0x748f82ee)
            with m.Case(57):
                m.d.comb += self.k_o.eq(0x78a5636f)
            with m.Case(58):
                m.d.comb += self.k_o.eq(0x84c87814)
            with m.Case(59):
                m.d.comb += self.k_o.eq(0x8cc70208)
            with m.Case(60):
                m.d.comb += self.k_o.eq(0x90befffa)
            with m.Case(61):
                m.d.comb += self.k_o.eq(0xa4506ceb)
            with m.Case(62):
                m.d.comb += self.k_o.eq(0xbef9a3f7)
            with m.Case(63):
                m.d.comb += self.k_o.eq(0xc67178f2)
            with m.Case():
                m.d.comb += self.k_o.eq(0x428a2f98)

        return m


class Sha256(wiring.Component):
    """SHA-256 hash function implementation.
    Inputs:
        - block_i - block of data. Note, that this module
          does not perform padding, this has to be done by
          the user beforehand. Bytes in block_i are placed
          in natural order. If we take an array of bytes, then
          the first element of said array is going to be placed
          into LSB of block_i.
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

    hash_o:   Out(256)
    ready_o:  Out(1, init=1)

    def __init__(self):
        super().__init__()
        self.k_storage = K_storage()

    def get_byte(self, signal: Signal, index: int):
        return signal.bit_select(index * 8, 8)

    def get_word(self, signal: Signal, index: int):
        return signal.bit_select(index * 32, 32)

    def elaborate(self, platform):
        m = am.Module()
        m.submodules += [self.k_storage]

        w = am.Array([Signal(32, init=0, name=f"w_{i}") for i in range(16)])
        w_i = Signal(32, init=0)
        k_i = Signal(32, init=0)

        i      = Signal(32, init=1)
        cstep  = Signal(4, init=0)
        s0     = Signal(32)
        s1     = Signal(32)
        ch     = Signal(32)
        maj    = Signal(32)

        h0 = Signal(32, init=0x6a09e667)
        h1 = Signal(32, init=0xbb67ae85)
        h2 = Signal(32, init=0x3c6ef372)
        h3 = Signal(32, init=0xa54ff53a)
        h4 = Signal(32, init=0x510e527f)
        h5 = Signal(32, init=0x9b05688c)
        h6 = Signal(32, init=0x1f83d9ab)
        h7 = Signal(32, init=0x5be0cd19)

        a = Signal(32, init=0)
        b = Signal(32, init=0)
        c = Signal(32, init=0)
        d = Signal(32, init=0)
        e = Signal(32, init=0)
        f = Signal(32, init=0)
        g = Signal(32, init=0)
        h = Signal(32, init=0)

        # Connect submodule's ports to this module's wires
        m.d.comb += self.k_storage.round_i.eq(i)
        m.d.comb += k_i.eq(self.k_storage.k_o)

        # Intermediate variables
        m.d.comb += s1.eq(e.rotate_right(6) ^ e.rotate_right(11) ^ e.rotate_right(25))
        m.d.comb += ch.eq((e & f) ^ ((~e) & g))
        m.d.comb += s0.eq(a.rotate_right(2) ^ a.rotate_right(13) ^ a.rotate_right(22))
        m.d.comb += maj.eq((a & b) ^ (a & c) ^ (b & c))

        t1 = Signal(32, init=0)
        t2 = Signal(32, init=0)

        # Schedule array expansion
        with m.If(i > 15):
            m.d.comb += t1.eq(
                (w[1].rotate_right(7)) ^ (w[1].rotate_right(18)) ^ (w[1] >> 3)
            )
            m.d.comb += t2.eq(
                (w[14].rotate_right(17)) ^ (w[14].rotate_right(19)) ^ (w[14] >> 10)
            )
            m.d.comb += w_i.eq(w[0] + t1 + w[9] + t2)
        with m.Else():
            m.d.comb += t1.eq(0)
            m.d.comb += t2.eq(0)
            m.d.comb += w_i.eq(w[0])

        with m.Switch(cstep):

            # ====== init stage ======
            with m.Case(0):
                with m.If(self.valid_i):
                    for igen in range(16):
                        m.d.sync += [
                            self.get_byte(w[igen], 0).eq(self.get_byte(self.block_i, igen * 4 + 3)),
                            self.get_byte(w[igen], 1).eq(self.get_byte(self.block_i, igen * 4 + 2)),
                            self.get_byte(w[igen], 2).eq(self.get_byte(self.block_i, igen * 4 + 1)),
                            self.get_byte(w[igen], 3).eq(self.get_byte(self.block_i, igen * 4 + 0)),
                            ]

                    m.d.sync += [
                        i.eq(0),
                        self.ready_o.eq(0),

                        a.eq(h0),
                        b.eq(h1),
                        c.eq(h2),
                        d.eq(h3),
                        e.eq(h4),
                        f.eq(h5),
                        g.eq(h6),
                        h.eq(h7),

                        cstep.eq(cstep + 1),
                        ]

            # ====== for i from 0 to 64 loop start ======
            with m.Case(1):
                with m.If(i < 64):
                    m.d.sync += [
                        h.eq(g),
                        g.eq(f),
                        f.eq(e),
                        e.eq(d + h + s1 + ch + k_i + w_i),
                        d.eq(c),
                        c.eq(b),
                        b.eq(a),
                        a.eq(h + s1 + ch + k_i + w_i + s0 + maj),
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
                    h0.eq(h0 + a),
                    h1.eq(h1 + b),
                    h2.eq(h2 + c),
                    h3.eq(h3 + d),
                    h4.eq(h4 + e),
                    h5.eq(h5 + f),
                    h6.eq(h6 + g),
                    h7.eq(h7 + h),

                    cstep.eq(cstep + 1),
                    ]

            with m.Case(3):
                m.d.sync += [
                    self.get_byte(self.hash_o,  0).eq(self.get_byte(h7, 0)),
                    self.get_byte(self.hash_o,  1).eq(self.get_byte(h7, 1)),
                    self.get_byte(self.hash_o,  2).eq(self.get_byte(h7, 2)),
                    self.get_byte(self.hash_o,  3).eq(self.get_byte(h7, 3)),

                    self.get_byte(self.hash_o,  4).eq(self.get_byte(h6, 0)),
                    self.get_byte(self.hash_o,  5).eq(self.get_byte(h6, 1)),
                    self.get_byte(self.hash_o,  6).eq(self.get_byte(h6, 2)),
                    self.get_byte(self.hash_o,  7).eq(self.get_byte(h6, 3)),

                    self.get_byte(self.hash_o,  8).eq(self.get_byte(h5, 0)),
                    self.get_byte(self.hash_o,  9).eq(self.get_byte(h5, 1)),
                    self.get_byte(self.hash_o, 10).eq(self.get_byte(h5, 2)),
                    self.get_byte(self.hash_o, 11).eq(self.get_byte(h5, 3)),

                    self.get_byte(self.hash_o, 12).eq(self.get_byte(h4, 0)),
                    self.get_byte(self.hash_o, 13).eq(self.get_byte(h4, 1)),
                    self.get_byte(self.hash_o, 14).eq(self.get_byte(h4, 2)),
                    self.get_byte(self.hash_o, 15).eq(self.get_byte(h4, 3)),

                    self.get_byte(self.hash_o, 16).eq(self.get_byte(h3, 0)),
                    self.get_byte(self.hash_o, 17).eq(self.get_byte(h3, 1)),
                    self.get_byte(self.hash_o, 18).eq(self.get_byte(h3, 2)),
                    self.get_byte(self.hash_o, 19).eq(self.get_byte(h3, 3)),

                    self.get_byte(self.hash_o, 20).eq(self.get_byte(h2, 0)),
                    self.get_byte(self.hash_o, 21).eq(self.get_byte(h2, 1)),
                    self.get_byte(self.hash_o, 22).eq(self.get_byte(h2, 2)),
                    self.get_byte(self.hash_o, 23).eq(self.get_byte(h2, 3)),

                    self.get_byte(self.hash_o, 24).eq(self.get_byte(h1, 0)),
                    self.get_byte(self.hash_o, 25).eq(self.get_byte(h1, 1)),
                    self.get_byte(self.hash_o, 26).eq(self.get_byte(h1, 2)),
                    self.get_byte(self.hash_o, 27).eq(self.get_byte(h1, 3)),

                    self.get_byte(self.hash_o, 28).eq(self.get_byte(h0, 0)),
                    self.get_byte(self.hash_o, 29).eq(self.get_byte(h0, 1)),
                    self.get_byte(self.hash_o, 30).eq(self.get_byte(h0, 2)),
                    self.get_byte(self.hash_o, 31).eq(self.get_byte(h0, 3)),

                    self.ready_o.eq(1),
                    cstep.eq(0),
                    ]

        return m

if __name__ == "__main__":
    sha256 = Sha256()
    with open("sha256.v", "w") as f:
        f.write(verilog.convert(sha256, name="sha256"))
