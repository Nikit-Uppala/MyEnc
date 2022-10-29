import sys
import os
parent = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir))
sys.path.insert(0, parent)
from cpa.cpa import CPA
from mac.mac import MAC
from hmac.hmac import HMAC
import random


class CCA:

    def __init__(self, block_size, oneway, hc, hashMac=True):

        self.block_size = block_size
        self.cpa = CPA(block_size, oneway, hc)
        if hashMac:
            self.mac = HMAC(block_size, IV=random.randint(0, 1<<block_size))
        else:
            self.mac = MAC(block_size, oneway, hc)
    
    def gen(self):
        k1 = self.cpa.gen()
        k2 = self.mac.gen()
        return k1, k2
    
    def encrypt(self, k1, k2, m, mode="OFB"):
        c = self.cpa.encrypt(k1, m, mode)
        t = self.mac.mac(k2, c)
        return "".join([c, t])

    def decrypt(self, k1, k2, c, mode="OFB"):
        tag = c[-self.block_size:]
        c = c[:-self.block_size]
        if not self.mac.verify(k2, c, tag):
            return "_|_"
        return self.cpa.decrypt(k1, c, mode)


def main():
    from helpers.functions import DLP, DLP_hc, get_g_p
    block_size = 128
    g, p = get_g_p(block_size)
    cipher = CCA(block_size, DLP(g, p), DLP_hc(block_size))
    k1, k2 = cipher.gen()
    print("Key 1:", k1)
    print("Key 2:", k2)
    m = "01001101011110010010000001100011011010010111000001101000011001010111001000100000011010010111001100100000011001110110111101100100"
    print("\nMessage:", m)
    c1 = cipher.encrypt(k1, k2, m, "OFB")
    c2 = cipher.encrypt(k1, k2, m, "OFB")
    print("\nCiphertext 1:", c1)
    print("Ciphertext 2:", c2)

    m1 = cipher.decrypt(k1, k2, c1, "OFB")
    m2 = cipher.decrypt(k1, k2, c2, "OFB")

    c1 = c1.replace("0", "1")
    new_m1 = cipher.decrypt(k1, k2, c1, "OFB")

    print("\nDecryption of ciphertext 1:", m1)
    print("Decryption of ciphertext 2:", m2)
    print("\nDecryption if atleast one bit of ciphertext 1 is changed:", new_m1)


if __name__ == "__main__":
    main()
