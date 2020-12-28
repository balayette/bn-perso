#!/usr/bin/python3

from binaryninja import *

from .hl import do_hl, do_hc
from .bb import do_missing_bb
from .exec_cfg import do_exec_cfg
from .fptr import do_exec_fptr
from .pointers_display import do_pointers_display

PluginCommand.register_for_address("Perso\\Highlight addresses", "Highlights instructions from a list of addresses", do_hl)
PluginCommand.register_for_address("Perso\\Highlight + hitcount", "Highlights instructions and prints hitcount", do_hc)
PluginCommand.register_for_address("Perso\\Create missing basic blocks", "Create missing basic blocks from trace", do_missing_bb)
PluginCommand.register_for_address("Perso\\Create CFG out of execution trace", "Create CFG out of execution traces", do_exec_cfg)
PluginCommand.register_for_address("Perso\\Create functions from function pointer array", "Create missing functions from a function pointer array.", do_exec_fptr)
PluginCommand.register_for_function("Perso\\Fix pointer display types", "Set the display type to pointers where it might make sense", do_pointers_display)
