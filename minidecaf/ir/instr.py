from ..utils import *


class IRInstr:
    def __init__(self):
        pass

    def __repr__(self):
        return self.__str__()


class Comment(IRInstr):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return f"# {self.msg}"

    def accept(self, visitor):
        visitor.visitComment(self)


class Const(IRInstr):
    def __init__(self, v):
        assert MIN_INT < v < MAX_INT
        self.v = v

    def __str__(self):
        return f"const {self.v}"

    def accept(self, visitor):
        visitor.visitConst(self)


class Ret(IRInstr):
    def __str__(self):
        return "ret"

    def accept(self, visitor):
        visitor.visitRet(self)


class Unary(IRInstr):
    def __init__(self, op):
        assert op in unaryOps
        self.op = op

    def __str__(self):
        return strOfUnaryOp[self.op]

    def accept(self, visitor):
        visitor.visitUnary(self)


class Binary(IRInstr):
    def __init__(self, op):
        assert op in binaryOps
        self.op = op

    def __str__(self):
        return strOfBinaryOp[self.op]

    def accept(self, visitor):
        visitor.visitBinary(self)


class Pop(IRInstr):
    def __str__(self):
        return f"pop"

    def accept(self, visitor):
        visitor.visitPop(self)


class Load(IRInstr):
    def __str__(self):
        return "load"

    def accept(self, visitor):
        visitor.visitLoad(self)


class Store(IRInstr):
    def __str__(self):
        return "store"

    def accept(self, visitor):
        visitor.visitStore(self)


class Label(IRInstr):
    def __init__(self, label):
        self.label = label

    def __str__(self):
        return f"{self.label}:"

    def accept(self, visitor):
        visitor.visitLabel(self)


class Branch(IRInstr):
    def __init__(self, op, label):
        assert op in branchOps
        self.op = op
        self.label = label

    def __str__(self):
        return f"{self.op} {self.label}"

    def accept(self, visitor):
        visitor.visitBranch(self)


class FrameSlot(IRInstr):
    def __init__(self, fpOffset):
        assert fpOffset < 0
        self.offset = fpOffset

    def __str__(self):
        return f"frameslot {self.offset}"

    def accept(self, visitor):
        visitor.visitFrameSlot(self)


class GlobalSymbol(IRInstr):
    def __init__(self, sym: str):
        self.sym = sym

    def __str__(self):
        return f"globalsymbol {self.sym}"

    def accept(self, visitor):
        visitor.visitGlobalSymbol(self)


class Call(IRInstr):
    def __init__(self, func):
        self.func = func

    def __str__(self):
        return f"call {self.func}"

    def accept(self, visitor):
        visitor.visitCall(self)
