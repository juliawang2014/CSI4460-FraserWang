#!/usr/bin/python

from PIL import Image
import argparse
import sys
import libraries.perlinNoise as pn

key = "0123456789ABCDEF0123456789ABCDEF" #testing key, 256 bits long but we will take 4 bits at a time out of it and use each 4 bit chunk for helping to encode 1 bit into the image
outputLocation = "./media/encoded.png"
doLogOutput = False
doRawEncoding = True

def encodeMessageIntoImage(message, inputImagePath, outputImagePath, inputKey="0123456789ABCDEF0123456789ABCDEF"):
    """method to encode message into image with specified message, path to image intput/output, and key"""
    global key
    key = inputKey
    global outputLocation
    outputLocation = outputImagePath
    with Image.open(inputImagePath) as image:
        imageArray = list(image.getdata(band=None))
        binaryString = convertMessagetoBinaryString(message)
        if doLogOutput:
            print(f"Total number of pixels: {str(len(imageArray))}")
            print(f"Image size: {str(image.size)}")
            print(f"Inital data: {str(imageArray[0:10])}")
            print(f"Message to encode:\n{message}")
        
        encodeMessage(imageArray, image.size, binaryString)

def decodeMessageFromImage(imagePath, inputKey="0123456789ABCDEF0123456789ABCDEF"):
    """method to get message out of image from path, key is optional"""
    global key
    key = inputKey
    with Image.open(imagePath) as image:
        return decodeMessage(list(image.getdata(band=None)), image.size) 

def printModeTest(mode, text):
    """code to switch behaviors based on mode, not used unless python program is called by itself"""
    if mode == "e" or mode == "encode":
        print("encode")
        openImage(text)
    elif mode == "d" or mode == "decode":
        print("decode")
        with Image.open("./media/encoded.png") as image:
            decodeMessage(list(image.getdata(band=None)), image.size)  
            
def openImage(text):
    """open our image into memory so we can encode
    not used unless file is called by itself"""
    with Image.open("./media/eyes.png") as image:
        #output first 10 pixels, don't want to completely clear the console output.
        imageArray = list(image.getdata(band=None))
        size = image.size
        if doLogOutput:
            print(f"Total number of pixels: {str(len(imageArray))}")
            print(f"Image size: {str(size)}")
            print(f"Inital data: {str(imageArray[0:10])}")
            print(f"Message to encode:\n{text}")
        
        binaryString = convertMessagetoBinaryString(text)
        
        #call our three functions to modify the image data in different ways.
        #the [:] is neccessary to pass the list by value instead of reference, avoiding changing it.
        
        #removeBlue(imageArray[:], size)
        #stripBit(imageArray[:], size, 0)
        encodeMessage(imageArray[:], size, binaryString)
        
def encodeMessage(imageArray, size, message): 
    """encodes a message into lsb of red pixels of a given image, message should be a string consisting of 0s and 1s.
    now with message length at the beginning of everything!
    also with improved scrambling, can't quite read data without key so that's nice""" 
    
    #check max length string can be, either due to our size encoding limits or the number of pixels in the image
    maxLength = len(imageArray) // 2 - 8 #divide by 2 because each bit of message is going to be stored between 2 pixels
    if len(message) > 16777215:
        maxLength = 16777215  
    if (len(message) > maxLength):
        print(f"Message is too long!\nMessage length (in characters): {len(message)//8}\nMax length (in characters): {maxLength//8}")
        return
    setMessageLength(imageArray, len(message))
    
    #pad out key with copies of itself to be the same length as the message we want to encode
    keyPadded = repeatStringToMatchLength(key, len(message))
    
    #main loop, replace each 2 pixel section with encoded data from encodeIntoChunk
    for i in range(0, len(message)*2, 2):
        working = list(imageArray[i+8]) + list(imageArray[i+9])
        imageArray[i+8:i+10] = encodeIntoChunk(working, int(message[i//2]), keyPadded[i//2])

    if doLogOutput:   
        print(f"\nData with encoded binary message: {str(imageArray[0:10])}")

    saveImageArrayAsImage(imageArray, size)
    
    
def encodeIntoChunk(chunk, value, key):
    """chunk represents 2 pixels of imageData unrolled into an array of size 6, depending on the key value pick which parts to encode to then encode parity, change other values to random, then return list of tuples like imageArray"""
    #cases for the possible values of key
    if key == "F":
        #special case for F key value, take parity of whole chunk after some scrambling
        for i in range(3):
            flipIndex = pn.PerlinNoiseFactoryWrapper(5)
            if pn.PerlinNoiseFactoryWrapper(1):
                chunk[flipIndex] = toggleBit(chunk[flipIndex], 0)
        if value != getLSBParity(chunk):
            randomIndex = pn.PerlinNoiseFactoryWrapper(5)
            chunk[randomIndex] = toggleBit(chunk[randomIndex], 0)
    else:
        #common logic for the other key values, encode random value into random parity pairs after inital encoding
        firstBit, secondBit = getArrayIndicesForParityEncoding(key)
        if value != getLSBParity([chunk[firstBit], chunk[secondBit]]):
            if pn.PerlinNoiseFactoryWrapper(1):
                chunk[firstBit] = toggleBit(chunk[firstBit], 0)
            else:
                chunk[secondBit] = toggleBit(chunk[secondBit], 0)

        #do our scrambling now    
        indexList = [0, 1, 2, 3, 4, 5]
        #remove the ones we already the actual data into
        indexList.remove(firstBit)
        indexList.remove(secondBit)

        #get 2 random indexes to encode random parity into
        firstBit = indexList[pn.PerlinNoiseFactoryWrapper(len(indexList) - 1)]
        indexList.remove(firstBit)
        secondBit = indexList[pn.PerlinNoiseFactoryWrapper(len(indexList) - 1)]
        indexList.remove(secondBit)
        parity = pn.PerlinNoiseFactoryWrapper(1)
        if parity != getLSBParity([chunk[firstBit], chunk[secondBit]]):
            if pn.PerlinNoiseFactoryWrapper(1):
                chunk[firstBit] = toggleBit(chunk[firstBit], 0)
            else:
                chunk[secondBit] = toggleBit(chunk[secondBit], 0)

        #2 items left in indexList, encode random parity into them
        parity = pn.PerlinNoiseFactoryWrapper(1)
        if parity != getLSBParity([chunk[indexList[0]], chunk[indexList[1]]]):
            if pn.PerlinNoiseFactoryWrapper(1):
                chunk[indexList[0]] = toggleBit(chunk[indexList[0]], 0)
            else:
                chunk[indexList[1]] = toggleBit(chunk[indexList[1]], 0)       
        
        
    return [tuple(chunk[0:3]), tuple(chunk[3:6])]
    
def decodeMessage(imageArray, size):
    """get raw binary message out of image"""
    #get length of message and then extract
    message = ""
    length = getMessageLength(imageArray)
    keyPadded = repeatStringToMatchLength(key, length)
    
    #extract, 2 pixels at a time
    for i in range(length):
        message = message + str(decodeChunk(list(imageArray[2*i+8]) + list(imageArray[2*i+9]), keyPadded[i]))

    message = convertBinaryStringToBytes(message)
    if message.isascii():
        message = message.decode("ascii")
    if doLogOutput:
        print(f"\nDecoded message:\n{message}")
    return message

def decodeChunk(chunk, key):
    """get parity of subset of chunk based on key value"""
    if key == "F":
        return getLSBParity(chunk)
    else:
        firstBit, secondBit = getArrayIndicesForParityEncoding(key)
        return getLSBParity([chunk[firstBit], chunk[secondBit]])
    
def getArrayIndicesForParityEncoding(key):
    """return a tuple with 2 items, corresponding to the indices to encode parity in/ the indices parity is encoded in"""
    firstBit = 0
    secondBit = 0
    #cases for the possible values of key
    if key == "0":
        firstBit = 0
        secondBit = 1
    elif key == "1":
        firstBit = 0
        secondBit = 2
    elif key == "2":
        firstBit = 0
        secondBit = 3
    elif key == "3":
        firstBit = 0
        secondBit = 4
    elif key == "4":
        firstBit = 0
        secondBit = 5
    elif key == "5":
        firstBit = 1
        secondBit = 2
    elif key == "6":
        firstBit = 1
        secondBit = 3
    elif key == "7":
        firstBit = 1
        secondBit = 4
    elif key == "8":
        firstBit = 1
        secondBit = 5
    elif key == "9":
        firstBit = 2
        secondBit = 3
    elif key == "A":
        firstBit = 2
        secondBit = 4
    elif key == "B":
        firstBit = 2
        secondBit = 5
    elif key == "C":
        firstBit = 3
        secondBit = 4
    elif key == "D":
        firstBit = 3
        secondBit = 5
    elif key == "E":
        firstBit = 4
        secondBit = 5
    else:
        print("KEY ERROR")
        quit()
    return(firstBit, secondBit)
    
def getLSBParity(list):
    """given a list as input, return the parity of the LSBs in said list"""
    parity = 0
    for item in list:
        parity = parity ^ (item % 2)
    return parity

def setMessageLength(imageArray, length):
    """stores message length into the image in the first 8 pixels"""
    #storing the message length into the LSB of the first 8 pixels of the image, using all 3 colors. This accepts message of length up to 16,777,215 bits, pretty good!
    strBinLength = bin(length)[2:].zfill(24) #pad beginning with 0s to take up the full 24 bits, also remove the 0x that python puts in there
    for i in range(8):
        #looks messy but its just taking the length and encoding it into the first 8 pixels of the image 1 pixel at a time
        tuple = setBit(imageArray[i][0], 0, int(strBinLength[3*i])), setBit(imageArray[i][1], 0, int(strBinLength[3*i+1])), setBit(imageArray[i][2], 0, int(strBinLength[3*i+2]))
        imageArray[i] = tuple
    getMessageLength(imageArray)
    
def getMessageLength(imageArray):
    """gets the message length out of the first 8 pixels"""
    length = ""
    for i in range(8):
        for j in range(3):
            length += str(imageArray[i][j] % 2)
    if doLogOutput:
        print(f"Binary length:  {str(length)}")
        print(f"Decimal length: {str(int(length, base=2))}")
    return int(length, base=2)
    
def saveImageArrayAsImage(imageArray, size):
    """saves image array from memory to disk"""
    #put imageData back into new image
    image = Image.new(mode="RGB", size=size)
    image.putdata(imageArray)
    #image2.show()
    image.save(outputLocation)
    
def convertMessagetoBinaryString(input):
    """convert ascii string or raw bytes (depending on if it is an ascii string) to string containing binary representation"""
    #take each character and pad to be 8 bits, add to output string and return entire string.
    output = ""
    if input.isascii():
        input = input.encode("ascii")
    for char in input:
        output += bin(char)[2:].zfill(8)
    return output

def convertBinaryStringToBytes(input):
    """covert binary string into ASCII equivalent"""
    output = ""
    for i in range(0, int(len(input)), 8):
        #yeah I know the following line is a bit of a mess but hey it works
        output += int(input[i:i+8], base=2).to_bytes(1, byteorder='big').hex()
    return bytes.fromhex(output) 

def setBit(int_type, offset, value):
    """following 2 functions derived from https://wiki.python.org/moin/BitManipulation, this one sets a specific bit"""
    if value == 1:
        mask = 1 << offset
        return(int_type | mask)
    if value == 0:
        mask = ~(1 << offset)
        return(int_type & mask)

def toggleBit(int_type, offset):
    """toggles a given bit inside an integer"""
    mask = 1 << offset
    return(int_type ^ mask)
    
def repeatStringToMatchLength(subject, targetLen):
    """repeats subject string enough times to be larger than target string then cuts off any extra
    code taken from https://stackoverflow.com/questions/3391076/repeat-string-to-certain-length"""
    return (subject * (targetLen // len(subject) + 1))[:targetLen]

def main():
    """not used unless file is called by itself"""
    parser = argparse.ArgumentParser(description = "Steganography encode/decode")
    parser.add_argument("-m", "--mode", dest = 'mode', type = str, required = True, help = "Mode of operation, e is encode and d is decode.")
    parser.add_argument("-t", "--text", dest = 'text', type = str, required = False, help = "Message to encode, binary string")

    args = parser.parse_args()
    printModeTest(args.mode, args.text)

def removeBlue(imageArray, size):   
    """set all blue values in pixels to 0 because I'm evil"""
    for i in range(len(imageArray)):
        r, g, b = imageArray[i]
        imageArray[i] = (r, g, 0)
       
    #print out new data
    print(f"\nBlue data: {str(imageArray[0:10])}")
        
    #put imageData back into new image
    image2 = Image.new(mode="RGB", size=size)
    image2.putdata(imageArray)
    #saveImageArrayAsImage(imageArray, size)


def stripBit(imageArray, size, bit): 
    """strip out specified bit from all color information in image"""
    #0 for bit is LSB
    for i in range(len(imageArray)):
        r, g, b = imageArray[i]
        imageArray[i] = setBit(r, bit, 0), setBit(g, bit, 0), setBit(b, bit, 0)
        
    print(f"\nData without LSB: {str(imageArray[0:10])}")
    #put imageData back into new image
    image2 = Image.new(mode="RGB", size=size)
    image2.putdata(imageArray)
    #saveImageArrayAsImage(imageArray, size)
    
if __name__ == "__main__":
    main()
