def getBinary(n):
    if type(n) == type(str()):
        return n
    return bin(n)[2:]


def pad(n, x):
    extra = ""
    if len(x) != n:
        extra = "0"*(n-len(x))
    return "".join([extra, x])


def endPad(block_size, x):
    numZeros = block_size-len(x) % block_size
    if numZeros == block_size:
        return x
    return "".join([x, "0"*numZeros])


def XOR(s1, s2):
    assert(len(s1) == len(s2))
    result = []
    for i in range(len(s1)):
        result.append(f"{int(s1[i] != s2[i])}")
    return "".join(result)
