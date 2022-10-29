import random


def modExpo(g, x, p):
    result = 1
    while x > 0:
        if x%2 == 1:
            result = int((result * g)%p)
        g = int((g*g)%p)
        x = x//2
    return result


def MSB(n, x):
    bin_x = x
    if type(x) == type(int()):
        bin_x = bin(x)[2:]
    if len(bin_x) == n:
        return bin_x[0]
    return "0"


def LSB(x):
    bin_x = x
    if type(x) == type(int()):
        bin_x = bin(x)[2:]
    return bin_x[-1]


def GCD(a, b):
    while b != 0:
        temp = a%b
        a = b
        b = temp
    return a


def millerRabin(n, iters=10):
    odd = n-1
    pow_2 = 0
    while (odd&1) == 0:
        odd >>= 1
        pow_2 += 1
    for i in range(iters):
        a = random.randint(2, n-2)
        check1 = modExpo(a, odd, n)
        if check1 != 1:
            check2 = False
            for j in range(pow_2):
                check = modExpo(a, odd<<j, n)
                if check == n-1:
                    check2 = True
                    break
            if check2 == False:
                return False
    return True


def isPrime(n):
    # low-level primality testing using first N(168) primes
    if n in primes:
        return True
    for p in primes:
        if p >= n:
            break
        if n%p == 0:
            return False
    # is low-level primality passes then high-level primality test using Miller Rabin test
    return millerRabin(n)



def getPrime(n): # this function returns random n-bit prime number p such that (p-1)/2 is also prime
    p = None
    while p is None:
        temp = random.randrange((1<<(n-1))+1, (1<<(n)), 2)
        if isPrime(temp):
            p = temp
    return p


def get_g_p(n):
    p = None
    while p is None:
        temp = getPrime(n-1)
        if isPrime(2*temp+1):
            p = 2*temp+1
    g = None
    while g is None:
        temp = random.randint(2, p-1)
        if modExpo(temp, (p-1)//2, p) != 1:
            g = temp
    return g, p



primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997)
DLP = lambda g, p: lambda x: modExpo(g, x, p)
DLP_hc = lambda n: lambda x: MSB(n, x)
