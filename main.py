#!/usr/bin/python

#first argument is gonna be -m/mode e/encode/d/decode for Encode or Decode for now, then some sort of file input, gonna use a png image in local folder for now.
import argparse
import sys

print("arguments:\t", sys.argv[1:], "\n")

#argument = sys.argv[1]
#if argument == "-d":
#    print("decode mode")
#elif argument == "-e":
#    print("encode mode")
    
#print("start new stuff")
    
def printModeTest(mode):
    print(mode)
    if mode == "e" || mode == "encode":
        print("encode")
    elif mode == "d" || mode == "decode":
        print("decode")
    
    


def main():
    parser = argparse.ArgumentParser(description = "Steganography encode/decode")
    parser.add_argument("-m", "--mode", dest = mode, type = str, required = True, help = "Mode of operation, e is encode and d is decode.")
    
    args = parse.parse_args()
    printModeTest(args.mode)
    
    
if __name__ == "__main__":
    main()