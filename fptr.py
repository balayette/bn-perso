from binaryninja.log import *
from binaryninja import *

def do_exec_fptr(bv, addr):
    v = bv.get_data_var_at(addr)
    if not v:
        log_alert(f"No variable at address {hex(addr)}")

    r = BinaryReader(bv)
    for addr in range(v.address, v.address + v.type.width, v.type.width // v.type.count):
        r.seek(addr)
        f = r.read64()
        if not bv.get_function_at(f):
            bv.add_function(f)
            log_info(f"[{hex(addr)}]: {hex(f)}")


