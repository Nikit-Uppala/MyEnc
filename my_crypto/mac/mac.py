import sys
import os
parent = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir))
sys.path.insert(0, parent)
import random
from prf.prf import PRF
from helpers.helper import endPad, getBinary, pad, XOR


class MAC:

    def __init__(self, block_size, oneway, hc):
        self.block_size = block_size
        self.prf = PRF(block_size, oneway, hc)
    
    def gen(self):
        key = random.randint(0, 1<<(self.block_size)-1)
        return pad(self.block_size, getBinary(key))
    
    def mac(self, k, x):
        bin_x = getBinary(x)
        bin_k = getBinary(k)
        length = len(bin_x)
        assert len(bin_k) <= self.block_size, f"Length of key is greater than expected ({self.block_size} bits)."
        assert length <= (1 << self.block_size), f"Message length too long. (Maximum length allowed - {1 << self.block_size})"
        bin_k = pad(self.block_size, bin_k)
        bin_x = endPad(self.block_size, bin_x)
        f = pad(self.block_size, getBinary(length))
        tag = self.prf.F(k, f)
        for i in range(0, length, self.block_size):
            tag = XOR(tag, bin_x[i:i+self.block_size])
            tag = self.prf.F(k, tag)
        return tag

    def verify(self, k, x, t):
        tag =  self.mac(k, x)
        return tag == t


def main():
    from helpers.functions import DLP, DLP_hc, get_g_p
    block_size = 128
    g, p = get_g_p(block_size)
    Mac = MAC(block_size, DLP(g, p), DLP_hc(block_size))
    key = Mac.gen()
    print("Your Key:", key)
    m = "010011010111100100100000011000110110100101110000011010000110010101110010001000000110100101110011001000000110011101101111011001001"
    print("\nMessage:", m)
    tag = Mac.mac(key, m)
    print("\nTag:", tag)

    verification = Mac.verify(key, m, tag)
    print("\nVerification:", verification)

if __name__ == "__main__":
    main()
