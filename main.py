#!/usr/bin/python

#first argument is gonna be e or d for Encode or Decode for now, then some sort of file input, gonna use a png image in local folder for now.

import sys

print("arguuments:\t", sys.argv[1:], "\n")

argument = sys.argv[1]
if argument == "d":
    print("decode mode")
elif argument == "e":
    print("encode mode")