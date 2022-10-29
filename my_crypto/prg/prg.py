import sys
import os
parent = os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir))
sys.path.insert(0, parent)
from helpers.helper import getBinary, pad


class PRG:

    def __init__(self, n, l, oneway, hc):
        self.n = n
        self.l = l
        self.oneway = oneway
        self.hc = hc

    def gen(self, seed):
        bin_seed = getBinary(seed)
        
        assert len(bin_seed) <= self.n, f"length of seed is larger than expected ({self.n})."

        bin_seed = pad(self.n, bin_seed)
        if self.l == self.n + 1:
            hc = self.hc(bin_seed)
            f = self.oneway(int(bin_seed, 2))
            return pad(self.n, getBinary(f)) + hc

        psuedorandom = []
        for i in range(self.l):
            hc = self.hc(bin_seed)
            f = self.oneway(int(bin_seed, 2))
            bin_seed = pad(self.n, getBinary(f))
            psuedorandom.append(hc)
        return "".join(psuedorandom)


def main():
    from helpers.functions import DLP, DLP_hc, get_g_p
    import time, random
    n = int(input("Enter the size of seed(n):"))
    l = int(input("Enter the size of pseudorandom output(l(n)):"))
    g, p = get_g_p(n)
    print(f"p={p}\ng={g}")
    dlp = DLP(g, p)
    hc = DLP_hc(n)
    generator = PRG(n, l, dlp, hc)
    while True:
        seed = random.randint(0, (1<<n)-1)
        ps_out = generator.gen(seed)
        print("\nSeed:", pad(n, getBinary(seed)))
        print("Pseudorandom Output:", ps_out)
        time.sleep(1)


if __name__ == "__main__":
    main()