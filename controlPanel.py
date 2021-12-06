import libraries.diffieHellman as diffieHellman
import libraries.steg as steg
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

ivector = b'\xd4\xef[y2\x91\x0c\x14\ry\x88\x13\xc4$\xfd&'
msg = ""
key = ""
steg.doLogOutput = False

def mainLoop():
    mode = input("Welcome!\nEnter 1 to resume an existing session.\nEnter 2 to start a new session.\nEnter 3 to quit.\n")
    if mode == "1":
        global key
        key = diffieHellman.resumeCommunicationSession()
        print(f"Key: {key}")
        recieveSendMessagesLoop()
    elif mode == "2":
        keyToShare = diffieHellman.startNewCommunication().decode("ascii")
        #construct file name to look like camera picture from smartphone, using current date and time
        now = datetime.now()
        str = now.strftime("./output/IMG_%Y%m%d_%H%M%S.png")
        steg.encodeMessageIntoImage(keyToShare, "./media/eyes.png", str)
        print(f"\nKey encoded into inital image stored at {str}\n")
        input("Waiting for shared inital image from the other party to be put into the ./input folder.\nPlease press enter once the image is put there.")

        #decode information from newest image located in ./input
        #code to get newest taken from https://stackoverflow.com/questions/39327032/how-to-get-the-latest-file-in-a-folder
        print("\nGetting newest image in ./input....")
        file = max([os.path.join("./input/", basename) for basename in os.listdir("./input/")], key=os.path.getctime)
        print(f"\nFile found! Filename: {file}")
        sharedKey = bytes(steg.decodeMessageFromImage(file), "utf8")
        key = diffieHellman.receiveExternalKey(sharedKey)
        print(f"Key: {key}")
        recieveSendMessagesLoop()
    elif mode == "3":
        print("Goodbye!")
    else:
        print("Invalid input, please try again.")
        mainLoop()
        
        
def recieveSendMessagesLoop():
    mode = input("\nPress 1 to recieve a message, 2 to send a message, or 3 to go back.\n")
    if mode == "1":
        cipher = AES.new(key,AES.MODE_CBC, iv=ivector)
        input("Waiting for image to be put into ./input, newest file will be seleted\nPlease press enter once the image is put there.\n")
        file = max([os.path.join("./input/", basename) for basename in os.listdir("./input/")], key=os.path.getctime)
        print(f"File found! Filename: {file}")
        keyForSteg = key.hex().upper()
        messageEncrypted = steg.decodeMessageFromImage(file, inputKey=keyForSteg)
        messageDecrypted = unpad(cipher.decrypt(messageEncrypted), AES.block_size)
        print(f"Message decoded from file:\n{messageDecrypted.decode('ascii')}")
        recieveSendMessagesLoop()
    elif mode == "2":
        cipher = AES.new(key,AES.MODE_CBC, iv=ivector)
        messageToEncode = input("Please enter your message now!\n")
        messageEncrypted = cipher.encrypt(pad(bytes(messageToEncode, "ascii"), AES.block_size))
        #construct file name to look like camera picture from smartphone, using current date and time
        now = datetime.now()
        str = now.strftime("./output/IMG_%Y%m%d_%H%M%S.png")
        keyForSteg = key.hex().upper()
        steg.encodeMessageIntoImage(messageEncrypted, "./media/eyes.png", str, inputKey=keyForSteg)
        print(f"\nMessage encoded into image stored at {str}")
        recieveSendMessagesLoop()
    elif mode == "3":
        mainLoop()
    else:
        print("Invalid input, please try again.")
        recieveSendMessagesLoop()

if __name__ == "__main__":
    mainLoop()


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
