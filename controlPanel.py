import libraries.diffieHellman as diffieHellman
import libraries.AES as AES

ivector = ""
msg = ""
key = ""

active = True
while(active):
    mode = input("Welcome!\nEnter 1 to resume an existing session.\nEnter 2 to start a new session.\nEnter 3 to quit.\n")
    if mode == "1":
        key = diffieHellman.resumeCommunicationSession()
        print(key)
    if mode == "2":
        keyToShare = diffieHellman.startNewCommunication()
        print(keyToShare)
        
        


"""
while(active):
    mode = input("Welcome, enter 1 to encrypt and send a new message, enter 2 to receive and decrypt a message, enter 3 to quit\n")
    if mode == "1":
        message = input("Input message to send: ")
        notSent = True
        while(notSent):
            choice = input("Enter 1 to add AES encryption, enter 2 to send the message using steganography, enter 3 to go back\n")
            if choice == "1":
                key = diffieHellman.getSharedKey()
                m, iv = AES.encryption(message, key)
                ivector = iv
                msg = message
                print("Cipher text: {}".format(msg))
            elif choice == "2":
                notSent = False
            elif choice == "3":
                notSent = False
            else:
                print("Invalid input, try again")
    elif mode == "2":
        msg = AES.decryption(msg, key, ivector)
        print("Decrypted message: {}".format(msg))
    elif mode == "3":
        active = False
    else:
        print("Invalid input, try again.")"""
