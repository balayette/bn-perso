#!/usr/bin/python3

from binaryninja import *

def do_missing_bb(bv, _):
    path = interaction.get_open_filename_input("Select instruction trace")
    if path is None:
        return

    with open(path, "r") as f:
        count = 0
        seen = set()

        for l in f.readlines():
            try:
                addr = int(l, 16)
            except:
                continue

            if addr in seen:
                continue

            bs = bv.get_basic_blocks_at(addr)
            if len(bs) > 0:
                continue

            print(f"Added function at {hex(addr)}")
            print(f"{bv.get_disassembly(addr)}")
            bv.add_function(addr)
            count += 1
            seen.add(addr)

        print(f"Added {count} blocks")
