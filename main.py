#!/usr/bin/python

#first argument is gonna be -m/mode e/encode/d/decode for Encode or Decode for now, then some sort of file input, gonna use a png image in local folder for now.

from PIL import Image
import argparse
import sys

print("arguments:\t", sys.argv[1:], "\n")

def printModeTest(mode):
    if mode == "e" or mode == "encode":
        print("encode")
        openImage()
    elif mode == "d" or mode == "decode":
        print("decode")
        
def openImage():
    with Image.open("./media/eyes.png") as image:
        #output first 10 pixels, don't want to completely clear the console output.
        imageArray = list(image.getdata(band=None))
        print("Total number of pixels: " + str(len(imageArray)))
        size = image.size
        print("Image size: " + str(size))
        print("Inital data: " + str(imageArray[0:10]))
        
        #call our two functions to modify the image data in different ways.
        #the [:] is neccessary to pass the list by value instead of reference, avoiding changing it.
        removeBlue(imageArray[:], size)
        stripBit(imageArray[:], size, 0)
        
def removeBlue(imageArray, size):   #set all blue values in pixels to 0 because I'm evil
    for i in range(len(imageArray)):
        r, g, b = imageArray[i]
        imageArray[i] = (r, g, 0)
       
    #print out new data
    print("\nBlue data: " + str(imageArray[0:10]))
        
    #put imageData back into new image
    image2 = Image.new(mode="RGB", size=size)
    image2.putdata(imageArray)
    #image2.show()

def stripBit(imageArray, size, bit):  #0 for bit is LSB
    for i in range(len(imageArray)):
        r, g, b = imageArray[i]
        imageArray[i] = setBit(r, bit, 0), setBit(g, bit, 0), setBit(b, bit, 0)
        
    print("\nData without LSB: " + str(imageArray[0:10]))
    #put imageData back into new image
    image2 = Image.new(mode="RGB", size=size)
    image2.putdata(imageArray)
    image2.show()
    


    
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
    
    args = parser.parse_args()
    printModeTest(args.mode)
    
    
if __name__ == "__main__":
    main()