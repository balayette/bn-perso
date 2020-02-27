#!/usr/bin/python3

from binaryninja import *

col = HighlightStandardColor.OrangeHighlightColor

def do(bv, hc):
    path = interaction.get_open_filename_input("Select address list")
    if path is None:
        return

    with open(path, "r") as f:
        seen = {}

        for l in f.readlines():
            try:
                addr = int(l, 16)
            except:
                continue

            if addr in seen:
                seen[addr] += 1
            else:
                seen[addr] = 1

        for addr in seen.keys():
            bs = bv.get_basic_blocks_at(addr)
            if len(bs) == 0:
                print(f"No basic block at {hex(addr)}")
                continue

            for b in bs:
                fun = b.function
                if not fun:
                    continue

                fun.set_user_instr_highlight(addr, col)

                if hc:
                    curr = fun.get_comment_at(addr)
                    fun.set_comment_at(addr, f"{curr} [hitcount: {seen[addr]}]")

def do_hl(bv, _):
    do(bv, False)

def do_hc(bv, _):
    do(bv, True)
