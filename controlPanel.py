import diffieHellman.diffieHellman as diffieHellman
import encryption.AES as AES
import perlinNoise.perlinNoise as perlinNoise

class initializationVector:
    def __init__(self, iv = 0) -> None:
        self._iv = iv
    def get_iv(self):
        return self._iv
    def set_iv(self, x):
        self._iv = x

ivector = initializationVector()
active = True
message, key = None, None
while(active):
    mode = input("Welcome, enter 1 to encrypt and send a new message, enter 2 to receive and decrypt a message, enter 3 to quit\n")
    if mode == "1":
        message = input("Input message to send: ")
        notSent = True
        while(notSent):
            choice = input("Enter 1 to add AES encryption, enter 2 to add Perlin Noise, enter 3 to send the message using steganography, enter 4 to go back\n")
            if choice == "1":
                key = diffieHellman.getSharedKey()
                message, iv = AES.encryption(message, key)
                ivector.set_iv(iv)
            elif choice == "2":
                perlinNoise.encryption(message)
            elif choice == "3":
                notSent = False
            elif choice == "4":
                notSent = False
            else:
                print("Invalid input, try again")
    elif mode == "2":
        AES.decryption(message, key, ivector.get_iv())
    elif mode == "3":
        active = False
    else:
        print("Invalid input, try again.")