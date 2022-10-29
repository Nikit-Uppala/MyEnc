import sys
import os
parent = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir))
sys.path.insert(0, parent)
from helpers.helper import getBinary, pad
from prg.prg import PRG 


class PRF:

    def __init__(self, n, oneway, hc):
        self.n = n
        self.prg = PRG(n, 2*n, oneway, hc)
    
    def F(self, k, x):
        bin_f = pad(self.n, getBinary(k))
        bin_x = pad(self.n, getBinary(x))
        for i in range(self.n-1, -1, -1):
            bin_f = self.prg.gen(int(bin_f, 2))
            if bin_x[i] == "0": # take first half
                bin_f = bin_f[:self.n]
            else: # take second half
                bin_f = bin_f[self.n:]
        return bin_f


def main():
    from helpers.functions import DLP, DLP_hc, get_g_p
    import time, random
    n = int(input("Enter the size of input(n):"))
    g, p = get_g_p(n)
    print(f"p={p}\ng={g}")
    dlp = DLP(g, p)
    hc = DLP_hc(n)
    psuedofuncs = PRF(n, dlp, hc)
    while True:
        k = random.randint(0, (1<<n)-1)
        x = random.randint(0, (1<<n)-1)
        output = psuedofuncs.F(k, x)
        print("\nk:", pad(n, getBinary(k)))
        print("x:", pad(n, getBinary(x)))
        print("Output:", output)
        time.sleep(1)


if __name__ == "__main__":
    main()
