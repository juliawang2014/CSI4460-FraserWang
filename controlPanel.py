import libraries.diffieHellman as diffieHellman
import libraries.steg as steg
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import secrets

key = ""
steg.doLogOutput = False

def mainLoop():
    """loop to pick between starting a new session or resuming the saved session, or altenratively exiting"""
    mode = input("Welcome!\nEnter 1 to resume an existing session.\nEnter 2 to start a new session.\nEnter 3 to quit.\n")
    if mode == "1":
        #load paramaters from paramaters.config to resume previous session that has already been set up
        global key
        key = diffieHellman.resumeCommunicationSession()
        print(f"Key: {key}")
        recieveSendMessagesLoop()
    elif mode == "2":
        #initialize diffieHellman process
        keyToShare = diffieHellman.startNewCommunication().decode("ascii")
        #construct file name to look like camera picture from smartphone, using current date and time
        now = datetime.now()
        str = now.strftime("./output/IMG_%Y%m%d_%H%M%S.png")
        #encode public key into image
        #TODO: pick random image from ./media/ to encode
        steg.encodeMessageIntoImage(keyToShare, "./media/eyes.png", str)
        print(f"\nKey encoded into inital image stored at {str}\n")
        input("Waiting for shared inital image from the other party to be put into the ./input folder.\nPlease press enter once the image is put there.")
        #decode information from newest image located in ./input
        #code to get newest taken from https://stackoverflow.com/questions/39327032/how-to-get-the-latest-file-in-a-folder
        print("\nGetting newest image in ./input....")
        file = max([os.path.join("./input/", basename) for basename in os.listdir("./input/")], key=os.path.getctime)
        print(f"\nFile found! Filename: {file}")
        #get public key encoded in image and derive session key from the public key
        sharedKey = bytes(steg.decodeMessageFromImage(file), "utf8")
        key = diffieHellman.receiveExternalKey(sharedKey)
        print(f"Key: {key}\nCurrent session has been saved.")
        recieveSendMessagesLoop()
    elif mode == "3":
        print("Goodbye!")
    else:
        print("Invalid input, please try again.")
        mainLoop()
        
def recieveSendMessagesLoop():
    """loop to send/recieve messages once session is set up"""
    mode = input("\nPress 1 to recieve a message, 2 to send a message, or 3 to go back.\n")
    if mode == "1":
        #get newest file in ./input, which should contain the ivector + encrypted message
        input("Waiting for image to be put into ./input, newest file will be seleted\nPlease press enter once the image is put there.\n")
        file = max([os.path.join("./input/", basename) for basename in os.listdir("./input/")], key=os.path.getctime)
        print(f"File found! Filename: {file}")
        #extract ivector and encrypted message
        keyForSteg = key.hex().upper()
        messageEncoded = steg.decodeMessageFromImage(file, inputKey=keyForSteg)
        ivector = messageEncoded[0:16]
        messageEncrypted = messageEncoded[16:]
        #create cipher and decrpt message
        cipher = AES.new(key,AES.MODE_CBC, iv=ivector)
        messageDecrypted = unpad(cipher.decrypt(messageEncrypted), AES.block_size)
        print(f"Message decoded from file:\n{messageDecrypted.decode('ascii')}")
        recieveSendMessagesLoop()
    elif mode == "2":
        #initalize AES encryption with cryptographically secure random ivector
        ivector = secrets.token_bytes(16)
        cipher = AES.new(key,AES.MODE_CBC, iv=ivector)
        messageToEncode = input("Please enter your message now!\n")
        messageEncrypted = cipher.encrypt(pad(bytes(messageToEncode, "ascii"), AES.block_size))
        #construct file name to look like camera picture from smartphone, using current date and time
        now = datetime.now()
        str = now.strftime("./output/IMG_%Y%m%d_%H%M%S.png")
        keyForSteg = key.hex().upper()
        #encode into ./media/eyes.png 
        #TODO: put many pictures into ./media and choose randomly from them
        steg.encodeMessageIntoImage(ivector + messageEncrypted, "./media/eyes.png", str, inputKey=keyForSteg)
        print(f"\nMessage encoded into image stored at {str}")
        recieveSendMessagesLoop()
    elif mode == "3":
        mainLoop()
    else:
        print("Invalid input, please try again.")
        recieveSendMessagesLoop()

if __name__ == "__main__":
    mainLoop()