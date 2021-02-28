from . import *
from ..ir.instr import *
from .typer import *
from .namer import *
from ..utils import *
from ..generated.MiniDecafParser import MiniDecafParser
from ..generated.MiniDecafVisitor import MiniDecafVisitor


# 删除之前暂时作为符号表的OffsetManager
# class OffsetManager:
#     def __init__(self):
#         self._off = {}
#         self._top = 0
#
#     def __getitem__(self, var):
#         return self._off[var]
#
#     def newSlot(self, var=None):
#         # 这里处理重复声明变量的问题，要及时raise error
#         if var in self._off:
#             raise MiniDecafError("repeated declaration")
#         self._top -= INT_BYTES
#         if var is not None:
#             self._off[var] = self._top
#         return self._top


# 生成跳转标记用的
class LabelManager:
    def __init__(self):
        self.nlabels = {}
        self.loopEntry = []
        self.loopExit = []

    def newLabel(self, scope="_L"):
        # 初始化或增加label
        initOrAdd(self.nlabels, scope)
        return f"{scope}_{self.nlabels[scope]}"

    def enterLoop(self, entry, exit):
        self.loopEntry.append(entry)
        self.loopExit.append(exit)

    def exitLoop(self):
        self.loopEntry.pop()
        self.loopExit.pop()

    # 判断是不是在loop里面，不是的话raise error
    def breakLabel(self):
        if len(self.loopExit) == 0:
            raise MiniDecafLocatedError("not in a loop")
        return self.loopExit[-1]

    def continueLabel(self):
        if len(self.loopExit) == 0:
            raise MiniDecafLocatedError("not in a loop")
        return self.loopEntry[-1]


class StackIRGen(MiniDecafVisitor):
    def __init__(self, emitter: IREmitter, nameInfo, typeInfo):
        self._E = emitter
        self.lbl = LabelManager()
        self.ni = nameInfo
        self.ti = typeInfo
        self.curFunc = None

    def _var(self, term):
        return self.ni[term]

    def emitVar(self, var):
        if var.offset is None:
            self._E([GlobalSymbol(var.ident)])
        else:
            self._E([FrameSlot(var.offset)])

    def visitReturnStmt(self, ctx: MiniDecafParser.ReturnStmtContext):
        self.visitChildren(ctx)
        self._E([Ret()])

    def visitExprStmt(self, ctx: MiniDecafParser.ExprStmtContext):
        self.visitChildren(ctx)
        self._E([Pop()])

    def visitBlock(self, ctx: MiniDecafParser.BlockContext):
        self.visitChildren(ctx)
        self._E([Pop()] * self.ni.funcs[self.curFunc].blockSlots[ctx])

    def visitBlockItemDecl(self, ctx: MiniDecafParser.BlockItemDeclContext):
        self.visitChildren(ctx)

    def visitIfStmt(self, ctx: MiniDecafParser.IfStmtContext):
        ctx.expr().accept(self)
        exitLabel = self.lbl.newLabel("if_end")
        elseLabel = self.lbl.newLabel("if_else")
        if ctx.el is not None:
            self._E([Branch("beqz", elseLabel)])
            ctx.th.accept(self)
            self._E([Branch("br", exitLabel), Label(elseLabel)])
            ctx.el.accept(self)
            self._E([Label(exitLabel)])
        else:
            self._E([Branch("beqz", exitLabel)])
            ctx.th.accept(self)
            self._E([Label(exitLabel)])

    # 循环语句
    def loop(self, name, init, cond, body, post):
        enterLabel = self.lbl.newLabel(f"{name}_entry")
        if post is not None:
            continueLabel = self.lbl.newLabel(f"{name}_continue")
        else:
            continueLabel = enterLabel
        exitLabel = self.lbl.newLabel(f"{name}_exit")
        self.lbl.enterLoop(continueLabel, exitLabel)
        if init is not None:
            init.accept(self)
            if isinstance(init, MiniDecafParser.ExprContext):
                self._E([Pop()])
        self._E([Label(enterLabel)])
        if cond is not None:
            cond.accept(self)
        else:
            self._E([Const(1)])
        self._E([Branch("beqz", exitLabel)])
        body.accept(self)
        if post is not None:
            self._E([Label(continueLabel)])
            post.accept(self)
            if isinstance(post, MiniDecafParser.ExprContext):
                self._E([Pop()])
        self._E([Branch("br", enterLabel), Label(exitLabel)])
        self.lbl.exitLoop()

    def visitForDeclStmt(self, ctx: MiniDecafParser.ForDeclStmtContext):
        self.loop("for", ctx.init, ctx.ctrl, ctx.stmt(), ctx.post)
        self._E([Pop()] * self.ni.funcs[self.curFunc].blockSlots[ctx])

    # 循环语句部分
    def visitForStmt(self, ctx: MiniDecafParser.ForStmtContext):
        self.loop("for", ctx.init, ctx.ctrl, ctx.stmt(), ctx.post)

    def visitWhileStmt(self, ctx: MiniDecafParser.WhileStmtContext):
        self.loop("while", None, ctx.expr(), ctx.stmt(), None)

    def visitDoWhileStmt(self, ctx: MiniDecafParser.DoWhileStmtContext):
        self.loop("dowhile", ctx.stmt(), ctx.expr(), ctx.stmt(), None)

    def visitBreakStmt(self, ctx: MiniDecafParser.BreakStmtContext):
        self._E([Branch("br", self.lbl.breakLabel())])

    def visitContinueStmt(self, ctx: MiniDecafParser.ContinueStmtContext):
        self._E([Branch("br", self.lbl.continueLabel())])

    def visitAtomInteger(self, ctx: MiniDecafParser.AtomIntegerContext):
        self._E([Const(int(toStr(ctx.Integer())))])

    def emitLoc(self, lvalue:MiniDecafParser.ExprContext):
        loc = self.ti.lvalueLoc(lvalue)
        for locStep in loc:
            if isinstance(locStep, IRInstr):
                self._E([locStep])
            else:
                locStep.accept(self)

    def visitCUnary(self, ctx: MiniDecafParser.CUnaryContext):
        op = toStr(ctx.unaryOp())
        if op == '&':
            self.emitLoc(ctx.cast())
        elif op == '*':
            self.visitChildren(ctx)
            self._E([Load()])
        else:
            self.visitChildren(ctx)
            self._E([Unary(op)])

    def _binaryExpr(self, ctx, op):
        self.visitChildren(ctx)
        self._E([Binary(toStr(op))])

    def _addExpr(self, ctx, op, lhs, rhs):
        if type(self.ti[lhs]) is PtrType:
            sz = self.ti[lhs].sizeof()
            if type(self.ti[rhs]) is PtrType: # ptr - ptr
                lhs.accept(self)
                rhs.accept(self)
                self._E([Binary(op)])
                self._E([Const(sz), Binary('/')])
            else: # ptr +- int
                lhs.accept(self)
                rhs.accept(self)
                self._E([Const(sz), Binary('*')])
                self._E([Binary(op)])
        else:
            sz = self.ti[rhs].sizeof()
            if type(self.ti[rhs]) is PtrType:
                lhs.accept(self)
                self._E([Const(sz), Binary('*')])
                rhs.accept(self)
                self._E([Binary(op)])
            else:
                self.visitChildren(ctx)
                self._E([Binary(op)])

    def visitCAdd(self, ctx: MiniDecafParser.CAddContext):
        self._addExpr(ctx, toStr(ctx.addOp()), ctx.add(), ctx.mul())

    def visitCMul(self, ctx: MiniDecafParser.CMulContext):
        self._binaryExpr(ctx, ctx.mulOp())

    def visitCRel(self, ctx: MiniDecafParser.CRelContext):
        self._binaryExpr(ctx, ctx.relOp())

    def visitCEq(self, ctx: MiniDecafParser.CEqContext):
        self._binaryExpr(ctx, ctx.eqOp())

    # 增加短路求值
    def visitCLand(self, ctx: MiniDecafParser.CLandContext):
        # self._binaryExpr(ctx, "&&")
        falseLabel = self.lbl.newLabel("land_false")
        exitLabel = self.lbl.newLabel("land_exit")
        ctx.land().accept(self)
        self._E([Branch("beqz", falseLabel)])
        ctx.eq().accept(self)
        self._E([Branch("beqz", falseLabel), Const(1), Branch("br", exitLabel), Label(falseLabel), Const(0),
                 Label(exitLabel)])

    # 增加短路求值
    def visitCLor(self, ctx: MiniDecafParser.CLorContext):
        # self._binaryExpr(ctx, "||")
        trueLabel = self.lbl.newLabel("lor_true")
        exitLabel = self.lbl.newLabel("lor_exit")
        ctx.lor().accept(self)
        self._E([Branch("bnez", trueLabel)])
        ctx.land().accept(self)
        self._E([Branch("bnez", trueLabel), Const(0), Branch("br", exitLabel), Label(trueLabel), Const(1),
                 Label(exitLabel)])

    def visitDecl(self, ctx: MiniDecafParser.DeclContext):
        variable = self._var(ctx.Ident())
        if ctx.expr() is not None:
            ctx.expr().accept(self)
        else:
            self._E([Const(0)] * (variable.size//INT_BYTES))

    def visitDeclExternalDecl(self, ctx:MiniDecafParser.DeclExternalDeclContext):
        pass

    def visitAtomIdent(self, ctx: MiniDecafParser.AtomIdentContext):
        variable = self._var(ctx.Ident())
        self.emitVar(variable)
        if not isinstance(self.ti[ctx], ArrayType):
            self._E([Load()])

    def _computeAddr(self, lvalue: Unary):
        if isinstance(lvalue, MiniDecafParser.TUnaryContext):
            return self._computeAddr(lvalue.atom())
        if isinstance(lvalue, MiniDecafParser.AtomIdentContext):
            variable = self._var(lvalue.Ident())
            return self._E([FrameSlot(variable.offset)])
        elif isinstance(lvalue, MiniDecafParser.AtomParenContext):
            return self._computeAddr(lvalue.expr())
        raise MiniDecafLocatedError(lvalue, f"{toStr(lvalue)} is not a lvalue")

    def visitCAsgn(self, ctx: MiniDecafParser.CAsgnContext):
        ctx.asgn().accept(self)
        self.emitLoc(ctx.unary())
        self._E([Store()])

    def visitCCond(self, ctx: MiniDecafParser.CCondContext):
        ctx.lor().accept(self)
        exitLabel = self.lbl.newLabel("cond_end")
        elseLabel = self.lbl.newLabel("cond_else")
        self._E([Branch("beqz", elseLabel)])
        ctx.expr().accept(self)
        self._E([Branch("br", exitLabel), Label(elseLabel)])
        ctx.cond().accept(self)
        self._E([Label(exitLabel)])

    def visitFuncDef(self, ctx:MiniDecafParser.FuncDefContext):
        func = toStr(ctx.Ident())
        nParams = len(self.ti.funcs[func].paramTy)
        self.curFunc = func
        self._E.enterFunction(func, nParams)
        ctx.block().accept(self)
        self._E.exitFunction()
        self.curFunc = None

    def visitFuncDecl(self, ctx:MiniDecafParser.FuncDeclContext):
        pass

    def visitPostfixArray(self, ctx:MiniDecafParser.PostfixArrayContext):
        fixupMult = self.ti[ctx.postfix()].base.sizeof()
        ctx.postfix().accept(self)
        ctx.expr().accept(self)
        self._E([Const(fixupMult), Binary('*'), Binary('+')])
        if not isinstance(self.ti[ctx], ArrayType):
            self._E([Load()])

    def visitPostfixCall(self, ctx:MiniDecafParser.PostfixCallContext):
        args = ctx.argList().expr()
        for arg in reversed(args):
            arg.accept(self)
        func = toStr(ctx.Ident())
        self._E([Call(func)])

    def visitProg(self, ctx:MiniDecafParser.ProgContext):
        for globInfo in self.ni.globs.values():
            self._E.emitGlobal(globInfo)
        self.visitChildren(ctx)
