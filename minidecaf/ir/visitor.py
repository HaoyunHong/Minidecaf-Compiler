from .instr import *


class IRVisitor:

    def __init__(self):
        pass

    def visitConst(self, instr):
        pass

    def visitRet(self, instr):
        pass

    def visitUnary(self, instr):
        pass

    def visitBinary(self, instr):
        pass

    def visitComment(self, instr):
        pass

    def visitPop(self, instr):
        pass

    def visitLoad(self, instr):
        pass

    def visitStore(self, instr):
        pass

    def visitLabel(self, instr):
        pass

    def visitBranch(self, instr):
        pass

    def visitFrameSlot(self, instr):
        pass

    def visitGlobalSymbol(self, instr):
        pass

    def visitCall(self, instr):
        pass

