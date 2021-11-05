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
        print("Inital data:   " + str(imageArray[0:10]))
        
        #section to set all blue values in pixels to 0 because I'm evil
        for i in range(len(imageArray)):
            r, g, b = imageArray[i]
            imageArray[i] = (r, g, 0)
            
        #print out new data
        print("\nModified data: " + str(imageArray[0:10]))
        
        #put imageData back into new image
        image2 = Image.new(mode="RGB", size=size)
        image2.putdata(imageArray)
        image2.show()
            
        

def main():
    parser = argparse.ArgumentParser(description = "Steganography encode/decode")
    parser.add_argument("-m", "--mode", dest = 'mode', type = str, required = True, help = "Mode of operation, e is encode and d is decode.")
    
    args = parser.parse_args()
    printModeTest(args.mode)
    
    
if __name__ == "__main__":
    main()