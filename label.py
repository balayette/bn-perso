from binaryninja.log import *
from binaryninja import *

def do_label_all_calls(bv, function):
    for xref in bv.get_code_refs(function.symbol.address):
        do_label_one_call(bv, xref.address)


def do_label_one_call(bv, addr):
    function = bv.get_functions_containing(addr)
    if len(function) != 1:
        log_warn("Multiple/no functions")
        return
    function = function[0]

    call_llil = function.get_llil_at(addr)
    if not call_llil:
        log_warn("Couldn't get LLIL")
        return

    if not call_llil.operation == LowLevelILOperation.LLIL_CALL:
        log_warn(f"{hex(addr)} not a call")
        return

    if not call_llil.dest.operation == LowLevelILOperation.LLIL_CONST_PTR:
        log_warn("Call though reg")
        return

    dest_function = bv.get_function_at(call_llil.dest.constant)

    call_mlil = call_llil.mlil
    function_mlil = function.mlil
    if not call_mlil or not function_mlil:
        log_warn("Couldn't get mlil")
        return

    call_mlil = call_mlil.ssa_form

    params = []
    for (param, arg) in zip(call_mlil.params, dest_function.parameter_vars):
        if hasattr(param, 'constant'):
            function.set_comment(param.address, f"`{arg.name}`")
        elif param.operation == MediumLevelILOperation.MLIL_VAR_SSA:
            addr_set = function_mlil.get_ssa_var_definition(param.src).address
            function.set_comment(addr_set, f"`{arg.name}`")
        else:
            log_warn(f"Unhandled param type `{type(param)}`")
