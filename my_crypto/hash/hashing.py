import sys
import os
parent = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir))
sys.path.insert(0, parent)
from helpers.helper import endPad, pad, getBinary
from fixed_hash.fixed_hash import FixedLengthHash


class HashFunction:

    def __init__(self, output_length, fixedHash=None, IV=0):
        self.output_length = output_length
        self.fixedHash = fixedHash
        self.IV = IV
    
    def gen(self):
        if self.fixedHash is None:
            self.fixedHash = FixedLengthHash(self.output_length)
        if self.fixedHash.cyclic is None:
            self.fixedHash.gen()
    
    def hash(self, input):
        input = getBinary(input)
        length = len(input)
        input = endPad(self.output_length, input)
        l = pad(self.output_length, getBinary(length))
        input = "".join([input, l])
        out = pad(self.output_length, getBinary(self.IV))
        for i in range(0, len(input), self.output_length):
            block = input[i: i+self.output_length]
            out = self.fixedHash.hash("".join([out, block]))
        return out


def main():
    output_length = 64
    hash = HashFunction(output_length)

    hash.gen()
    print(f"q:{hash.fixedHash.cyclic.q}")
    print(f"g:{hash.fixedHash.cyclic.g}")
    print(f"h:{hash.fixedHash.h}")

    m = "010100110101111001001000000110001101101001011100000110100001100101011100100010000001101001011100110010000001100111011011110110010010"

    print("\nString:", m)
    print("Length of string:", len(m))
    h = hash.hash(m)
    print("\nHash output:", h)
    print("Length of the output:", len(h))

if __name__ == "__main__":
    main()
