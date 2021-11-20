import diffieHellman.diffieHellman as diffieHellman
import encryption.AES as AES
import perlinNoise.perlinNoise as perlinNoise

#a, b = diffieHellman.dhSend()
#print(a)
#print(b)
#print(diffieHellman.dhReceive(a, b))


active = True
mode = input("Welcome, enter 1 to encrypt and send a message, enter 2 to receive and decrypt a message, enter 3 to quit")
a, b = None, None
while(active):
    if mode == 1:
        message = input("Input message to send: ")
        notSent = True
        while(notSent):
            choice = input("Enter 1 to add AES encryption, enter 2 to add Perlin Noise, enter 3 to send the message using steganography, enter 4 to go back")
            if choice == 1:
                pass
            elif choice == 2:
                pass
            elif choice == 3:
                notSent = False
            elif choice == 4:
                notSent = False
            else:
                print("Invalid input, try again")
    elif mode == 2:
        pass
    elif mode == 3:
        active = False
    else:
        print("Invalid input, try again.")