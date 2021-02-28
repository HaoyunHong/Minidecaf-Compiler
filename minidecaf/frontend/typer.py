from ..utils import *
from ..generated.MiniDecafParser import MiniDecafParser
from ..generated.MiniDecafVisitor import MiniDecafVisitor
from ..ir.instr import *
from .namer import *
from .types import *


class TypeInfo:
    def __init__(self):
        self.loc = {}
        self.funcs = {}
        self._t = {}

    def lvalueLoc(self, ctx):
        return self.loc[ctx]

    def setLvalueLoc(self, ctx, loc):
        self.loc[ctx] = loc

    def __str__(self):
        res = "Lvalue analysis result: (location of expr at lhs == value of rhs):\n\t"

        def p(c):
            return f"{c.start.line},{c.start.column}~{c.stop.line},{c.stop.column}"

        def g(locStep):
            if isinstance(locStep, IRInstr):
                return f"{locStep}"
            else:
                return f"[{p(locStep)}]"

        def f(cl):
            ctx, loc = cl
            ctxStr = f"{p(ctx)}"
            locStr = " :: ".join(map(g, loc))
            return f"{ctxStr:>32} : {locStr}"

        res += "\n\t".join(map(f, self.loc.items()))
        res += "\n\nType info for funcs:\n\t"

        def f(nf):
            name, funcInfo = nf
            return f"{name:>32} : ({funcInfo.paramTy}) -> {funcInfo.retTy}"

        res += "\n\t".join(map(f, self.funcs.items()))
        return res

    def __getitem__(self, ctx):
        return self._t[ctx]


class FuncTypeInfo:
    def __init__(self, retTy, paramTy):
        self.retTy = retTy
        self.paramTy = paramTy

    def compatible(self, other):
        return self.retTy == other.retTy and self.paramTy == other.paramTy

    def call(self):
        @TypeRule
        def callRule(ctx, argTy):
            if self.paramTy == argTy:
                return self.retTy
            return f"bad argument types"

        return callRule


def SaveType(f):
    def g(self, ctx):
        ty = f(self, ctx)
        self.typeInfo._t[ctx] = ty
        return ty

    return g


class Typer(MiniDecafVisitor):

    def __init__(self, nameInfo):
        self.vartyp = {}  # Variable -> Type
        self.nameInfo = nameInfo
        self.curFunc = None
        self.typeInfo = TypeInfo()
        self.locator = Locator(self.nameInfo, self.typeInfo)

    def visitChildren(self, ctx):
        ty = MiniDecafVisitor.visitChildren(self, ctx)
        self.typeInfo._t[ctx] = ty
        return ty

    def _var(self, term):
        return self.nameInfo[term]

    def _declTyp(self, ctx: MiniDecafParser.DeclContext):
        base = ctx.ty().accept(self)
        dims = [int(toStr(x)) for x in reversed(ctx.Integer())]
        if len(dims) == 0:
            return base
        else:
            return ArrayType.make(base, dims)

    def _funcTypeInfo(self, ctx):
        retTy = ctx.ty().accept(self)
        paramTy = self.paramTy(ctx.paramList())
        return FuncTypeInfo(retTy, paramTy)

    def _argTy(self, ctx):
        return list(map(lambda x: x.accept(self), ctx.expr()))

    def visitPtrType(self, ctx):
        return PtrType(ctx.ty().accept(self))

    def visitIntType(self, ctx):
        return IntType()

    def locate(self, ctx):
        loc = self.locator.locate(self.curFunc, ctx)
        if loc is None:
            raise MiniDecafLocatedError(ctx, "lvalue expected")
        self.typeInfo.setLvalueLoc(ctx, loc)

    def checkUnary(self, ctx, op, ty):
        rule = expandIterableKey([
            (['-', '!', '~'], intUnaopRule),
            (['&'], addrofRule),
            (['*'], derefRule),
        ])[op]
        return rule(ctx, ty)

    def checkBinary(self, ctx, op, lhs, rhs):
        rule = expandIterableKey([
            (['*', '/', '%'] + logicOps, intBinopRule),
            (eqOps, eqRule),
            (relOps, relRule),
            (['='], asgnRule),
            (['+'], tryEach('+', intBinopRule, ptrArithRule)),
            (['-'], tryEach('-', intBinopRule, ptrArithRule, ptrDiffRule)),
        ])[op]
        return rule(ctx, lhs, rhs)

    @SaveType
    def visitCCast(self, ctx):
        ctx.cast().accept(self)
        return ctx.ty().accept(self)

    @SaveType
    def visitCUnary(self, ctx):
        res = self.checkUnary(ctx.unaryOp(), toStr(ctx.unaryOp()),
                              ctx.cast().accept(self))
        if toStr(ctx.unaryOp()) == '&':
            self.locate(ctx.cast())
        return res

    @SaveType
    def visitAtomParen(self, ctx):
        return ctx.expr().accept(self)

    @SaveType
    def visitCAdd(self, ctx):
        return self.checkBinary(ctx.addOp(), toStr(ctx.addOp()),
                                ctx.add().accept(self), ctx.mul().accept(self))

    @SaveType
    def visitCMul(self, ctx):
        return self.checkBinary(ctx.mulOp(), toStr(ctx.mulOp()),
                                ctx.mul().accept(self), ctx.cast().accept(self))

    @SaveType
    def visitCRel(self, ctx):
        return self.checkBinary(ctx.relOp(), toStr(ctx.relOp()),
                                ctx.rel().accept(self), ctx.add().accept(self))

    @SaveType
    def visitCEq(self, ctx):
        return self.checkBinary(ctx.eqOp(), toStr(ctx.eqOp()),
                                ctx.eq().accept(self), ctx.rel().accept(self))

    @SaveType
    def visitCLand(self, ctx):
        return self.checkBinary(ctx, "&&",
                                ctx.land().accept(self), ctx.eq().accept(self))

    @SaveType
    def visitCLor(self, ctx):
        return self.checkBinary(ctx, "||",
                                ctx.lor().accept(self), ctx.land().accept(self))

    @SaveType
    def visitCCond(self, ctx):
        return condRule(ctx, ctx.lor().accept(self),
                        ctx.expr().accept(self), ctx.cond().accept(self))

    @SaveType
    def visitCAsgn(self, ctx):
        res = self.checkBinary(ctx.asgnOp(), toStr(ctx.asgnOp()),
                               ctx.unary().accept(self), ctx.asgn().accept(self))
        self.locate(ctx.unary())
        return res

    @SaveType
    def visitPostfixCall(self, ctx):
        argTy = self._argTy(ctx.argList())
        func = toStr(ctx.Ident())
        rule = self.typeInfo.funcs[func].call()
        return rule(ctx, argTy)

    @SaveType
    def visitPostfixArray(self, ctx):
        return arrayRule(ctx,
                         ctx.postfix().accept(self), ctx.expr().accept(self))

    @SaveType
    def visitAtomInteger(self, ctx):
        if safeEval(toStr(ctx)) == 0:
            return ZeroType()
        else:
            return IntType()

    @SaveType
    def visitAtomIdent(self, ctx):
        var = self._var(ctx.Ident())
        return self.vartyp[var]

    def visitDecl(self, ctx):
        var = self._var(ctx.Ident())
        ty = self._declTyp(ctx)
        self.vartyp[var] = ty
        if ctx.expr() is not None:
            initTyp = ctx.expr().accept(self)
            asgnRule(ctx, ty, initTyp)

    def checkFunc(self, ctx):
        funcTypeInfo = self._funcTypeInfo(ctx)
        func = toStr(ctx.Ident())
        if func in self.typeInfo.funcs:
            prevFuncTypeInfo = self.typeInfo.funcs[func]
            if not funcTypeInfo.compatible(prevFuncTypeInfo):
                raise MiniDecafLocatedError(ctx, f"conflicting types for {func}")
        else:
            self.typeInfo.funcs[func] = funcTypeInfo

    def visitFuncDef(self, ctx):
        func = toStr(ctx.Ident())
        self.curFunc = func
        self.checkFunc(ctx)
        self.visitChildren(ctx)
        self.curFunc = None

    def visitFuncDecl(self, ctx):
        func = toStr(ctx.Ident())
        self.curFunc = func
        self.checkFunc(ctx)
        self.curFunc = None

    def paramTy(self, ctx):
        res = []
        for decl in ctx.decl():
            if decl.expr() is not None:
                raise MiniDecafLocatedError(decl, "parameter cannot have initializers")
            paramTy = self._declTyp(decl)
            if isinstance(paramTy, ArrayType):
                raise MiniDecafLocatedError(decl, "parameter cannot have array types")
            res += [paramTy]
        return res

    def visitDeclExternalDecl(self, ctx):
        ctx = ctx.decl()
        var = self.nameInfo.globs[toStr(ctx.Ident())].var
        ty = self._declTyp(ctx)
        if var in self.vartyp:
            prevTy = self.vartyp[var]
            if prevTy != ty:
                raise MiniDecafLocatedError(ctx, f"conflicting types for {var.ident}")
        else:
            self.vartyp[var] = ty
        if ctx.expr() is not None:
            initTyp = ctx.expr().accept(self)
            asgnRule(ctx, ty, initTyp)

    def visitReturnStmt(self, ctx):
        funcRetTy = self.typeInfo.funcs[self.curFunc].retTy
        ty = ctx.expr().accept(self)
        retRule(ctx, funcRetTy, ty)

    def visitIfStmt(self, ctx):
        self.visitChildren(ctx)
        stmtCondRule(ctx, ctx.expr().accept(self))  # idempotent

    def visitForDeclStmt(self, ctx):
        self.visitChildren(ctx)
        if ctx.ctrl is not None: stmtCondRule(ctx, ctx.ctrl.accept(self))

    def visitForStmt(self, ctx):
        self.visitChildren(ctx)
        if ctx.ctrl is not None: stmtCondRule(ctx, ctx.ctrl.accept(self))

    def visitWhileStmt(self, ctx):
        self.visitChildren(ctx)
        stmtCondRule(ctx, ctx.expr().accept(self))

    def visitDoWhileStmt(self, ctx):
        self.visitChildren(ctx)
        stmtCondRule(ctx, ctx.expr().accept(self))


class Locator(MiniDecafVisitor):
    def __init__(self, nameInfo, typeInfo):
        self.nameInfo = nameInfo
        self.typeInfo = typeInfo

    def locate(self, func, ctx):
        self.func = func
        res = ctx.accept(self)
        self.func = None
        return res

    def visitAtomIdent(self, ctx):
        var = self.nameInfo[ctx.Ident()]
        if var.offset is None:
            return [GlobalSymbol(var.ident)]
        else:
            return [FrameSlot(var.offset)]

    def visitCUnary(self, ctx):
        op = toStr(ctx.unaryOp())
        if op == '*':
            return [ctx.cast()]

    def visitPostfixArray(self, ctx):
        fixupMult = self.typeInfo[ctx.postfix()].base.sizeof()
        return [ctx.postfix(), ctx.expr(), Const(fixupMult), Binary('*'), Binary('+')]

    def visitAtomParen(self, ctx):
        return ctx.expr().accept(self)
