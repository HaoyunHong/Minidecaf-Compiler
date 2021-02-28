from ..utils import *
from ..generated.MiniDecafParser import MiniDecafParser
from ..generated.MiniDecafVisitor import MiniDecafVisitor


class Variable:
    _varcnt = {}

    def __init__(self, ident, offset, size):
        initOrAdd(Variable._varcnt, ident)
        self.id = Variable._varcnt[ident]
        self.ident = ident
        self.offset = offset
        self.size = size

    def __eq__(self, other):
        return self.id == other.id and self.ident == other.ident and self.offset == other.offset and self.size == other.size

    def __str__(self):
        return f"{self.ident}({self.id})"

    def __repr__(self):
        return self.__str__()

    def __hash__(self):
        return hash((self.ident, self.id, self.offset, self.size))

# 存储函数名信息
class FuncNameInfo:
    def __init__(self, hasDef=True):
        self._v = {}
        self._pos = {}
        self.blockSlots = {}
        self.hasDef = hasDef

    def __str__(self):
        res = "name resolution:\n"

        def f(pv):
            pos, var = pv
            if var.offset is not None:
                loc = f"at frameslot {var.offset}"
            else:
                loc = f"global symbol"
            return f"{str(pos):>16} : {str(var):<10} {loc}"

        res += "\n".join(map(f,
                             [(self._pos[term], self._v[term]) for term in self._v]))

        res += "\nnumber of slots in each block:\n"

        def f(bs):
            ctx, slots = bs
            startPos = (ctx.start.line, ctx.start.column)
            stopPos = (ctx.stop.line, ctx.stop.column)
            region = f"{startPos} ~ {stopPos}"
            return f"{region:>32} : {slots}"

        res += "\n".join(map(f,
                             [(ctx, self.blockSlots[ctx]) for ctx in self.blockSlots]))

        return res

    def bind(self, term, var, pos):
        self._v[term] = var
        self._pos[term] = pos

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, term):
        return self._v[term]


class GlobInfo:
    def __init__(self, var, size, init=None):
        self.var = var
        self.size = var.size
        self.init = init

    def __str__(self):
        return f"{self.var}, size={self.size}, {self.initStr()}"

    def initStr(self):
        if self.init is None:
            return "uninitialized"
        else:
            return f"initializer={self.init}"


class NameInfo:
    def __init__(self):
        self._v = {}
        self.funcs = {}
        self.globs = {}

    def freezeFuncInfo(self):
        for funcNameInfo in self.funcs.values():
            self._v.update(funcNameInfo._v)

    def __str__(self):
        def f(fn):
            func, funcNameInfo = fn
            indentedFuncNameInfo = "\t" + str(funcNameInfo).replace("\n", "\n\t")
            return f"NameInfo for {func}:\n{indentedFuncNameInfo}"

        res = "\n--------\n\n".join(map(f, self.funcs.items()))
        res += "\n--------\n\nGlobInfos:\n\t"
        res += "\n\t".join(map(str, self.globs.values()))
        return res

    def __repr__(self):
        return self.__str__()

    def __getitem__(self, term):
        return self._v[term]


class Namer(MiniDecafVisitor):

    def __init__(self):
        self._v = myStack()  # str -> Variable
        self._nSlots = []  # 名称解析栈
        self.curNSlots = 0  # 目前的slot数目
        self.nameInfo = NameInfo()
        self._curFuncNameInfo = None

    # 压入栈
    def defVar(self, ctx, term, numInts=1):
        self.curNSlots += numInts
        var = self._v[toStr(term)] = Variable(toStr(term), -INT_BYTES * self.curNSlots, INT_BYTES * numInts)
        pos = (ctx.start.line, ctx.start.column)
        self._curFuncNameInfo.bind(term, var, pos)

    def useVar(self, ctx, term):
        var = self._v[toStr(term)]
        pos = (ctx.start.line, ctx.start.column)
        self._curFuncNameInfo.bind(term, var, pos)

    def declNElems(self, ctx):
        res = prod([int(toStr(x)) for x in ctx.Integer()])
        if res <= 0:
            raise MiniDecafLocatedError(ctx, "array size <= 0")
        if res >= MAX_INT:
            raise MiniDecafLocatedError(ctx, "array size too large")
        return res

    def enterScope(self, ctx):
        self._v.push()
        self._nSlots.append(self.curNSlots)

    def exitScope(self, ctx):
        self._curFuncNameInfo.blockSlots[ctx] = self.curNSlots - self._nSlots[-1]
        self.curNSlots = self._nSlots[-1]
        self._v.pop()
        self._nSlots.pop()

    def visitBlock(self, ctx: MiniDecafParser.BlockContext):
        self.enterScope(ctx)
        self.visitChildren(ctx)
        self.exitScope(ctx)

    def visitDecl(self, ctx: MiniDecafParser.DeclContext):
        if ctx.expr() is not None:
            ctx.expr().accept(self)
        var = toStr(ctx.Ident())
        if var in self._v.top_n():
            raise MiniDecafLocatedError(ctx, f"redefinition of {var}")
        self.defVar(ctx, ctx.Ident(), self.declNElems(ctx))

    def visitForDeclStmt(self, ctx: MiniDecafParser.ForDeclStmtContext):
        self.enterScope(ctx)
        self.visitChildren(ctx)
        self.exitScope(ctx)

    def visitAtomIdent(self, ctx: MiniDecafParser.AtomIdentContext):
        var = toStr(ctx.Ident())
        if var not in self._v:
            raise MiniDecafLocatedError(ctx, f"{var} undeclared")
        self.useVar(ctx, ctx.Ident())

    def visitFuncDef(self, ctx: MiniDecafParser.FuncDefContext):
        func = toStr(ctx.Ident())
        if func in self.nameInfo.funcs and \
                self.nameInfo.funcs[func].hasDef:
            raise MiniDecafLocatedError(f"redefinition of function {func}")
        funcNameInfo = FuncNameInfo(hasDef=True)
        self._curFuncNameInfo = self.nameInfo.funcs[func] = funcNameInfo
        self.enterScope(ctx.block())
        ctx.paramList().accept(self)
        # skip the enter/exitScope of the block because we've already done it.
        self.visitChildren(ctx.block())
        self.exitScope(ctx.block())
        self._curFuncNameInfo = None

    def visitFuncDecl(self, ctx: MiniDecafParser.FuncDeclContext):
        func = toStr(ctx.Ident())
        if func in self.nameInfo.globs:
            raise MiniDecafLocatedError(ctx, f"global variable {func} redeclared as function")
        funcNameInfo = FuncNameInfo(hasDef=False)
        if func not in self.nameInfo.funcs:
            self.nameInfo.funcs[func] = funcNameInfo

    def globalInitializer(self, ctx: MiniDecafParser.ExprContext):
        if ctx is None:
            return None
        try:
            initializer = safeEval(toStr(ctx))
            return initializer
        except:
            raise MiniDecafLocatedError(ctx, "global initializers must be constants")

    def visitDeclExternalDecl(self, ctx: MiniDecafParser.DeclExternalDeclContext):
        ctx = ctx.decl()
        init = self.globalInitializer(ctx.expr())
        varStr = toStr(ctx.Ident())
        if varStr in self.nameInfo.funcs:
            raise MiniDecafLocatedError(ctx, f"function {varStr} redeclared as global variable")
        var = Variable(varStr, None, INT_BYTES * self.declNElems(ctx))
        globInfo = GlobInfo(var, INT_BYTES, init)
        if varStr in self._v.top_n():
            prevGlobInfo = self.nameInfo.globs[varStr]
            if prevGlobInfo.init is not None and globInfo.init is not None:
                raise MiniDecafLocatedError(ctx, f"redefinition of variable {varStr}")
            if globInfo.init is not None:
                self.nameInfo.globs[varStr].init = init
        else:
            self._v[varStr] = var
            self.nameInfo.globs[varStr] = globInfo

    def visitProg(self, ctx: MiniDecafParser.ProgContext):
        self.visitChildren(ctx)
        self.nameInfo.freezeFuncInfo()
