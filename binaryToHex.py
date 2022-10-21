#!/usr/bin/python3

import argparse
import mmap
import os

for file in os.listdir("./"):
    if file.startswith("CPU"):
        with open(file, "r+b") as f:
            m = mmap.mmap(f.fileno(), 0)
            while True:
                b = m.read(8)
                if b == b'':
                    break
                print('0x{:016x}'.format(int.from_bytes(b, "big", signed=False)))
            m.close()
