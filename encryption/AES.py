from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64decode, b64encode

def encryption(message, key):
    cipher = AES.new(key, AES.MODE_CBC)
    data = message.encode('UTF-8')
    msg = cipher.encrypt(pad(data, AES.block_size))
    iv = b64encode(cipher.iv).decode('UTF-8')
    msg = b64encode(msg).decode('UTF-8')
    return msg, iv

def decryption(message, key, iv):
    iv = b64decode(iv)
    message = b64decode(message)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(message), AES.block_size)
    print(plaintext.decode('UTF-8'))
    

#Everything below can be commented out later
"""
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
"""