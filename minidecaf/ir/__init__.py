from ..utils import *
from .instr import IRInstr
from .visitor import IRVisitor


class IRFunc:
    def __init__(self, name, nParams, instrs):
        self.name = name
        self.nParams = nParams
        self.instrs = instrs


class IRGlob:
    def __init__(self, sym, size, init=None, align=INT_BYTES):
        self.sym = sym
        self.size = size
        self.init = init
        self.align = align


class IRProg:
    def __init__(self, funcs, globs):
        self.funcs = funcs
        self.globs = globs


class IREmitter:
    def __init__(self):
        self.instrs = []

    def emit(self, ir_list: [IRInstr]):
        self.instrs += ir_list

    def getIR(self):
        return IRProg(self.instrs)

    def __call__(self, ir_list):
        self.emit(ir_list)
