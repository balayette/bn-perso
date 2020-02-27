#!/usr/bin/python3

from binaryninja import *

from .hl import do_hl, do_hc

PluginCommand.register_for_address("Perso\\Highlight addresses", "Highlights instructions from a list of addresses", do_hl)
PluginCommand.register_for_address("Perso\\Highlight + hitcount", "Highlights instructions and prints hitcount", do_hc)
