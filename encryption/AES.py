from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import argparse

def encryption(message, key):
    #key = get_random_bytes(16)
    key = key.encode('UTF-8')
    iv = b'1111111111111111'
    cipher = AES.new(key, AES.MODE_CBC, iv)
    data = message.encode('UTF-8')
    msg = cipher.encrypt(pad(data, 16))
    print(msg)
    with open("..\messages\message.txt", "wb") as file:
        file.write(msg)

def decryption(message, key):
    key = key.encode('UTF-8')
    iv = b'1111111111111111'
    with open(message, "rb") as f:
        data = f.read()
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = cipher.decrypt(data)
    print(plaintext)


def driver(message, mode, key):
    if mode == 'd':
        decryption(message, key)
    else:
        encryption(message, key)

def main():
    parser = argparse.ArgumentParser(description = "AES Encryption")
    parser.add_argument('-m', '--message', dest = 'message', type = str, required = True, help = "The txt file to encode/decode")
    parser.add_argument('-t', '--type', dest = 'type', type = str, required = True, help = 'd for decode mode, e for encode mode. Default is encode mode')
    parser.add_argument('-k', '--key', dest = 'key', type = str, required = True, help = 'Key')

    args = parser.parse_args()
    driver(args.message, args.type, args.key)

if __name__ == "__main__":
    main()
