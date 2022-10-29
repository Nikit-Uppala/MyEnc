import sys
import os
parent = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir))
sys.path.insert(0, parent)
import random
from helpers.helper import pad, getBinary
from helpers.functions import get_g_p, modExpo


class CyclicGroup:

    def __init__(self, q, g=None):
        self.q = q
        self.G = range(0, q)
        self.g = g
    
    def getGen(self):
        self.g = None
        while self.g is None:
            temp = random.randint(2, self.q-1)
            if modExpo(temp, (self.q-1)//2, self.q) == 1:
                self.g = temp
    
    def operation(self, a, b):
        return (a%self.q*b%self.q)%self.q
    
    def repeatedOperation(self, a, x):
        return modExpo(a, x, self.q)


class FixedLengthHash:

    def __init__(self, output_length, cyclic=None, h=None):
        self.input_length = 2 * output_length
        self.output_length = output_length
        self.cyclic = cyclic
        self.h = None
        if cyclic is not None:
            self.h = h
    
    def gen(self):
        # to be implemented
        if self.cyclic is None:
            g, p = get_g_p(self.output_length)
            self.cyclic = CyclicGroup(p, g)
        if self.cyclic.g is None:
            self.cyclic.getGen()
        self.h = random.randint(1, p-1)
    
    def hash(self, input):
        assert self.h is not None, "Please run the gen function first"
        input = getBinary(input)
        assert len(input) <= self.input_length, f"Length of the input is bigger than {self.input_length}"
        input = pad(self.input_length, input)
        first_half = input[:self.output_length]
        second_half = input[self.output_length:]
        output = self.cyclic.repeatedOperation(self.cyclic.g, int(first_half, 2))
        output = self.cyclic.operation(
            output,
            self.cyclic.repeatedOperation(self.h, int(second_half, 2))
        )
        return pad(self.output_length, getBinary(output))


def main():
    output_length = 64
    hash = FixedLengthHash(output_length)
    hash.gen()
    print(f"q:{hash.cyclic.q}")
    print(f"g:{hash.cyclic.g}")
    print(f"h:{hash.h}")

    m = "01001101011110010010000001100011011010010111000001101000011001010111001000100000011010010111001100100000011001110110111101100100"
    print("\nString:", m)
    print("Length of string:", len(m))
    h = hash.hash(m)
    print("\nHash output:", h)
    print("Length of output:", len(h))

if __name__ == "__main__":
    main()
