#!/usr/bin/python

import sys

print("arguuments:\t", sys.argv[1:], "\n")

argument = sys.argv[1]
if argument == "d":
    print("decode mode")
elif argument == "e":
    print("encode mode")