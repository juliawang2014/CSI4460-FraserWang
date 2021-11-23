import libraries.diffieHellman as diffieHellman
import libraries.AES as AES

class initializationVector:
    def __init__(self, iv = 0) -> None:
        self._iv = iv
    def get_iv(self):
        return self._iv
    def set_iv(self, x):
        self._iv = x

class messageMaker:
    def __init__(self, message = "") -> None:
        self._message = message
    def get_message(self):
        return self._message
    def set_message(self, x):
        self._message = x

class keyMaker:
    def __init__(self, key = None) -> None:
        self._key = key
    def get_key(self):
        return self._key
    def set_key(self, x):
        self._key = x

ivector = initializationVector()
msg = messageMaker()
key = keyMaker()
active = True
while(active):
    mode = input("Welcome, enter 1 to encrypt and send a new message, enter 2 to receive and decrypt a message, enter 3 to quit\n")
    if mode == "1":
        message = input("Input message to send: ")
        notSent = True
        while(notSent):
            choice = input("Enter 1 to add AES encryption, enter 2 to send the message using steganography, enter 3 to go back\n")
            if choice == "1":
                key.set_key(diffieHellman.getSharedKey())
                m, iv = AES.encryption(message, key.get_key())
                ivector.set_iv(iv)
                msg.set_message(m)
                print("Cipher text: {}".format(msg.get_message()))
            elif choice == "2":
                notSent = False
            elif choice == "3":
                notSent = False
            else:
                print("Invalid input, try again")
    elif mode == "2":
        msg.set_message(AES.decryption(msg.get_message(), key.get_key(), ivector.get_iv()))
        print("Decrypted message: {}".format(msg.get_message()))
    elif mode == "3":
        active = False
    else:
        print("Invalid input, try again.")