from my_crypto.helpers.functions import DLP, DLP_hc, get_g_p, modExpo
from my_crypto.helpers.helper import pad
from my_crypto.cca.cca import CCA
import random
import os

def strToBin(s):
    result = []
    for c in s:
        bits = pad(8, bin(ord(c))[2:])
        result.append(bits)
    return "".join(result)


def binToStr(b):
    assert(len(b)%8 == 0)
    result = []
    for i in range(0, len(b), 8):
        result.append(chr(int(b[i:i+8], 2)))
    return "".join(result)


def binToHex(b):
    numBits = 4
    assert(len(b)%numBits == 0)
    result = []
    for i in range(0, len(b), numBits):
        block = b[i:i+numBits]
        block = int(block, 2)
        if block < 10:
            result.append(str(block))
        else:
            result.append(chr(ord('a')+block-10))
    return "".join(result)


def hexToBin(h):
    result = []
    for c in h:
        if 'z' >= c >= 'a':
            result.append(pad(4, bin(10+ord(c)-ord('a'))[2:]))
        else:
            result.append(pad(4, bin(int(c))[2:]))
    return "".join(result)


def main():
    # print(len("My cipher is god"), strToBin("My cipher is god"), sep="\n")
    block_size = 64
    keys_dir = "keys"
    if not os.path.isdir(keys_dir):
        os.mkdir(keys_dir)
    g_p_file = f"g_p_{block_size}.txt"
    if not os.path.isfile(f"{keys_dir}/{g_p_file}"):
        print("searching prime")
        g, p = get_g_p(block_size)
        print("prime found")
        print("p =", p)
        print("g =", g)
        with open(f"{keys_dir}/{g_p_file}", "w") as file:
            file.write(f"{g} {p}\n")
    else:
        with open(f"{keys_dir}/{g_p_file}", "r") as file:
            g, p = (int(x) for x in file.readline().strip().split())
    
    oneway = DLP(g, p)
    hc = DLP_hc(block_size)
    cipher = CCA(block_size, oneway, hc, True)
    
    key_file = f"key_{block_size}.txt"
    if not os.path.isfile(f"{keys_dir}/{key_file}"):
        key1, key2 = cipher.gen()
        print("Key for message confidentiality:", binToHex(key1))
        print("Key for message integrity:", binToHex(key2))
        with open(f"{keys_dir}/{key_file}", "w") as file:
            file.write(binToHex(key1) + "\n")
            file.write(binToHex(key2) + "\n")
    else:
        with open(f"{keys_dir}/{key_file}", "r") as file:
            key1 = hexToBin(file.readline().strip())
            key2 = hexToBin(file.readline().strip())
    
    print("\t\t====MY CIPHER====")
    while True:
        print("'E' for encryption\n'D' for decryption\n")
        choice = input("Enter your choice:")

        if choice == "E" or choice == "e":
            message = input("Enter a message:")
            message = strToBin(message)
            ciphertext = cipher.encrypt(key1, key2, message, "RC")
            print("Cipher text:", binToHex(ciphertext))
        
        elif choice == "D" or choice == "d":
            ciphertext = input("Enter a valid cipher text:")
            ciphertext = hexToBin(ciphertext)
            message = cipher.decrypt(key1, key2, ciphertext, "RC")
            if len(message) % 8 != 0:
                print("Message not authenticated")
            else:
                print("Message:", binToStr(message))
        print()


if __name__ == "__main__":
    main()