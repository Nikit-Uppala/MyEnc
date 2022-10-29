import sys
import os
parent = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir))
sys.path.insert(0, parent)
from prf.prf import PRF
from helpers.helper import XOR, endPad, getBinary, pad
import random


class CPA:

    def __init__(self, block_size, oneway, hc):
        self.block_size = block_size
        self.prf = PRF(block_size, oneway, hc)
    
    def gen(self):
        key = random.randint(0, (1<<self.block_size)-1)
        return pad(self.block_size, getBinary(key))
    
    def _OFBEncrypt(self, k, m):
        f = []
        for i in range(self.block_size):
            f.append("1" if random.random() >= 0.5 else "0")
        f = "".join(f)
        blocks = [f]
        for i in range(0, len(m), self.block_size):
            f = self.prf.F(k, f)
            blocks.append(XOR(f, m[i:i+self.block_size]))
        return "".join(blocks)
    
    def _OFBDecrypt(self, k, c):
        f = c[:self.block_size]
        blocks = []
        for i in range(self.block_size, len(c), self.block_size):
            f = self.prf.F(k, f)
            blocks.append(XOR(c[i:i+self.block_size], f))
        return "".join(blocks)
    
    def _RCEncrypt(self, k, m):
        ctr = random.randint(0, (1<<self.block_size) - 1)
        blocks = [pad(self.block_size, getBinary(ctr))]
        block_num = 1
        for i in range(0, len(m), self.block_size):
            r = getBinary((ctr+block_num)%(1<<self.block_size))
            r = self.prf.F(k, pad(self.block_size, r))
            blocks.append(XOR(r, m[i:i+self.block_size]))
            block_num += 1
        return "".join(blocks)

    def _RCDecrypt(self, k, c):
        ctr = int(c[:self.block_size], 2)
        blocks = []
        block_num = 1
        for i in range(self.block_size, len(c), self.block_size):
            r = getBinary((ctr+block_num)%(1<<self.block_size))
            r = self.prf.F(k, pad(self.block_size, r))
            blocks.append(XOR(r, c[i:i+self.block_size]))
            block_num += 1
        return "".join(blocks)

    def encrypt(self, k, m, mode="OFB"):
        bin_k = pad(self.block_size, getBinary(k))
        bin_m = getBinary(m)
        bin_m = endPad(self.block_size, m)
        if mode == "OFB":
            return self._OFBEncrypt(bin_k, bin_m)
        elif mode == "RC":
            return self._RCEncrypt(bin_k, bin_m)

    def decrypt(self, k, c, mode="OFB"):
        bin_k = pad(self.block_size, getBinary(k))
        if mode == "OFB":
            return self._OFBDecrypt(bin_k, c)
        elif mode == "RC":
            return self._RCDecrypt(bin_k, c)


def main():
    from helpers.functions import DLP, DLP_hc, get_g_p
    block_size = 128
    g, p = get_g_p(block_size)
    cipher = CPA(block_size, DLP(g, p), DLP_hc(block_size))
    key = cipher.gen()
    print("Your Key:", key)
    m = "01001101011110010010000001100011011010010111000001101000011001010111001000100000011010010111001100100000011001110110111101100100"
    print("\nMessage:", m)
    c1 = cipher.encrypt(key, m, "OFB")
    c2 = cipher.encrypt(key, m, "OFB")
    print("\nCiphertext 1:", c1)
    print("Ciphertext 2:", c2)

    m1 = cipher.decrypt(key, c1, "OFB")
    m2 = cipher.decrypt(key, c2, "OFB")

    print("\nDecryption of ciphertext 1:", m1)
    print("Decryption of ciphertext 2:", m2)


if __name__ == "__main__":
    main()
