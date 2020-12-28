from binaryninja import *
from binaryninja.log import *

class BNILVisitor(object):
    """
    MIT License

    Copyright (c) 2019 Josh Watson

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    """
    def __init__(self, **kw):
        super(BNILVisitor, self).__init__()

    def visit(self, expression, idx=0):
        method_name = 'visit_{}'.format(expression.operation.name)
        if hasattr(self, method_name):
            value = getattr(self, method_name)(expression, idx)
        else:
            for i, x in enumerate(expression.operands):
                if isinstance(x, lowlevelil.LowLevelILInstruction):
                    self.visit(x, i)
            value = None
        return value


class Visitor(BNILVisitor):
    def __init__(self, bv, function):
        super(Visitor, self).__init__()
        self.function = function
        self.bv = bv

    def visit_LLIL_CONST(self, exp, idx=0):
        log_info(
            f"Found const @ {hex(exp.address)} = {hex(exp.value.value)} opidx: {idx}"
        )
        addr = exp.value.value
        if self.bv.get_symbol_at(addr) or self.bv.get_segment_at(addr):
            self.function.set_int_display_type(
                exp.address,
                addr,
                idx,
                enums.IntegerDisplayType.PointerDisplayType,
            )

def do_pointers_display(bv, func):
    v = Visitor(bv, func)
    for bb in func.llil:
        for inst in bb:
            v.visit(inst)
