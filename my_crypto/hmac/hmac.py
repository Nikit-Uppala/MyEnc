import sys
import os
parent = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir))
sys.path.insert(0, parent)
import random
from hash.hashing import HashFunction
from helpers.helper import pad, getBinary, XOR


class HMAC:

    def __init__(self, output_length, IV=0, ipad="0x5C", opad="0x36"):
        assert output_length % 8 == 0, "Length multiple of 8 expected"
        self.output_length = output_length
        self.hash = HashFunction(output_length, IV=IV)
        self.hash.gen()
        self.ipad = pad(8, getBinary(int(ipad, 16)))
        self.opad = pad(8, getBinary(int(opad, 16)))
        self.IV = pad(output_length, getBinary(IV))
    
    def gen(self):
        key = random.randint(0, (1<<self.output_length)-1)
        return pad(self.output_length, getBinary(key))
    
    def mac(self, k, input):
        k = getBinary(k)
        assert len(k) <= self.output_length, f"Length of key larger than expected. ({self.output_length})"
        input = getBinary(input)
        assert len(input) <= 1<<self.output_length, "Message length too long."
        k = pad(self.output_length, k)
        multiple = self.output_length//len(self.ipad)
        temp = XOR(k, self.ipad*multiple)
        inner_hash = self.hash.hash("".join([temp, input]))
        temp = XOR(k, self.opad*multiple)
        tag = self.hash.hash("".join([temp, inner_hash]))
        return tag

    def verify(self, k, input, tag):
        check = self.mac(k, input)
        return check == tag


def main():
    output_length = 64
    IV = 1209378
    Mac = HMAC(output_length, IV)
    
    key = Mac.gen()
    print("Your Key:", key)
    m = "01001101011110010010000001100011011010010111000001101000011001010111001000100000011010010111001100100000011001110110111101100100"
    print("\nMessage:", m)
    tag = Mac.mac(key, m)
    print("\nTag:", tag)

    verification = Mac.verify(key, m, tag)
    print("\nVerification:", verification)


if __name__ == "__main__":
    main()
