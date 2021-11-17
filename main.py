#!/usr/bin/python

#first argument is gonna be -m/mode e/encode/d/decode for Encode or Decode for now, then some sort of file input, gonna use a png image in local folder for now.

from PIL import Image
import argparse
import sys

print("arguments:\t", sys.argv[1:], "\n")

def printModeTest(mode, text):
    if mode == "e" or mode == "encode":
        print("encode", "e")
        openImage(text)
    elif mode == "d" or mode == "decode":
        print("decode")
        with Image.open("./media/encoded.png") as image:
            decodeMessage(list(image.getdata(band=None)), image.size)  
        
def openImage(text):
    with Image.open("./media/eyes.png") as image:
        #output first 10 pixels, don't want to completely clear the console output.
        imageArray = list(image.getdata(band=None))
        print("Total number of pixels: " + str(len(imageArray)))
        size = image.size
        print("Image size: " + str(size))
        print("Inital data: " + str(imageArray[0:10]))
        print("Message to encode: " + text)
        
        binaryString = convertASCIItoBinaryString(text)
        
        #call our three functions to modify the image data in different ways.
        #the [:] is neccessary to pass the list by value instead of reference, avoiding changing it.
        
        #removeBlue(imageArray[:], size)
        #stripBit(imageArray[:], size, 0)
        encodeMessage(imageArray[:], size, binaryString)
    
def encodeMessage(imageArray, size, message): 
    #encodes a message into lsb of red pixels of a given image, message should be a string consisting of 0s and 1s.
    #message must be shorter than imageArray, no checking so be careful!
    #now with message length at the beginning of everything!
    setMessageLength(imageArray, len(message))
    for i in range(len(message)):
        r, g, b = imageArray[i+8]
        imageArray[i+8] = setBit(r, 0, int(message[i])), g, b
        
    print("\nData with encoded binary message: " + str(imageArray[0:10]))
    saveImageArrayAsImage(imageArray, size)
    
def decodeMessage(imageArray, size):
    #get length of message and then extract
    message = ""
    length = getMessageLength(imageArray)
    for i in range(length):
        r = imageArray[i+8][0]
        message = message + str(r % 2)
        
    message = convertBinaryStringToASCII(message)
    print("\nDecoded message:\n" + message)
    
def setMessageLength(imageArray, length):
    #storing the message length into the LSB of the first 8 pixels of the image, using all 3 colors. This accepts message of length up to 16,777,215 bits, pretty good!
    strBinLength = bin(length)[2:].zfill(24) #pad beginning with 0s to take up the full 24 bits, also remove the 0x that python puts in there
    for i in range(8):
        #looks messy but its just taking the length and encoding it into the first 8 pixels of the image 1 pixel at a time
        tuple = setBit(imageArray[i][0], 0, int(strBinLength[3*i])), setBit(imageArray[i][1], 0, int(strBinLength[3*i+1])), setBit(imageArray[i][2], 0, int(strBinLength[3*i+2]))
        imageArray[i] = tuple
    getMessageLength(imageArray)
    
def getMessageLength(imageArray):
    length = ""
    for i in range(8):
        for j in range(3):
            length += str(imageArray[i][j] % 2)
    print("Binary length:  " + str(length))
    print("Decimal length: " + str(int(length, base=2)))
    return int(length, base=2)
    
def saveImageArrayAsImage(imageArray, size):
    #put imageData back into new image
    image = Image.new(mode="RGB", size=size)
    image.putdata(imageArray)
    #image2.show()
    image.save("./media/encoded.png")
    
def convertASCIItoBinaryString(input):
    #take each character and pad to be 8 bits, add to output string and return entire string.
    output = ""
    input = input.encode("ascii")
    for char in input:
        output += bin(char)[2:].zfill(8)
    return output
    
def convertBinaryStringToASCII(input):
    output = ""
    for i in range(0, int(len(input)), 8):
        #yeah I know the following line is a bit of a mess but hey it works
        output  += int(input[i:i+8], base=2).to_bytes(1, byteorder='big').decode("ascii")
    return output 

#following 2 functions derived from https://wiki.python.org/moin/BitManipulation
def setBit(int_type, offset, value):
    if value == 1:
        mask = 1 << offset
        return(int_type | mask)
    if value == 0:
        mask = ~(1 << offset)
        return(int_type & mask)
        
def toggleBit(int_type, offset):
    mask = 1 << offset
    return(int_type ^ mask)

def main():
    parser = argparse.ArgumentParser(description = "Steganography encode/decode")
    parser.add_argument("-m", "--mode", dest = 'mode', type = str, required = True, help = "Mode of operation, e is encode and d is decode.")
    parser.add_argument("-t", "--text", dest = 'text', type = str, required = False, help = "Message to encode, binary string")
    
    args = parser.parse_args()
    printModeTest(args.mode, args.text)
    #printModeTest(args.mode, "1010101010101010101010101010")

def removeBlue(imageArray, size):   
    #set all blue values in pixels to 0 because I'm evil
    for i in range(len(imageArray)):
        r, g, b = imageArray[i]
        imageArray[i] = (r, g, 0)
       
    #print out new data
    print("\nBlue data: " + str(imageArray[0:10]))
        
    #put imageData back into new image
    image2 = Image.new(mode="RGB", size=size)
    image2.putdata(imageArray)
    #saveImageArrayAsImage(imageArray, size)

def stripBit(imageArray, size, bit):  
    #0 for bit is LSB
    for i in range(len(imageArray)):
        r, g, b = imageArray[i]
        imageArray[i] = setBit(r, bit, 0), setBit(g, bit, 0), setBit(b, bit, 0)
        
    print("\nData without LSB: " + str(imageArray[0:10]))
    #put imageData back into new image
    image2 = Image.new(mode="RGB", size=size)
    image2.putdata(imageArray)
    #saveImageArrayAsImage(imageArray, size)
    
if __name__ == "__main__":
    main()