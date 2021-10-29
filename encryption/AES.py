from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import argparse

def encryption(message):
    key = get_random_bytes(16)
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = None
    with open(message, "rb") as f:
        data = f.read()
    msg = cipher.encrypt(pad(data, 16))
    print(msg)

def decryption(message):
    pass

def driver(message, mode):
    if mode == 'd':
        decryption(message)
    else:
        encryption(message)

def main():
    parser = argparse.ArgumentParser(description = "AES Encryption")
    parser.add_argument('-m', '--message', dest = 'message', type = str, required = True, help = "The txt file to encode/decode")
    parser.add_argument('-t', '--type', dest = 'type', type = str, required = True, help = 'd for decode mode, e for encode mode. Default is encode mode')

    args = parser.parse_args()
    driver(args.message, args.type)

if __name__ == "__main__":
    main()