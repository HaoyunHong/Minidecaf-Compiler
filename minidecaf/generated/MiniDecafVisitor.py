# Generated from MiniDecaf.g4 by ANTLR 4.8
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .MiniDecafParser import MiniDecafParser
else:
    from MiniDecafParser import MiniDecafParser

# This class defines a complete generic visitor for a parse tree produced by MiniDecafParser.

class MiniDecafVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by MiniDecafParser#prog.
    def visitProg(self, ctx:MiniDecafParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#funcExternalDecl.
    def visitFuncExternalDecl(self, ctx:MiniDecafParser.FuncExternalDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#declExternalDecl.
    def visitDeclExternalDecl(self, ctx:MiniDecafParser.DeclExternalDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#funcDef.
    def visitFuncDef(self, ctx:MiniDecafParser.FuncDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#funcDecl.
    def visitFuncDecl(self, ctx:MiniDecafParser.FuncDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#paramList.
    def visitParamList(self, ctx:MiniDecafParser.ParamListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#ptrType.
    def visitPtrType(self, ctx:MiniDecafParser.PtrTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#intType.
    def visitIntType(self, ctx:MiniDecafParser.IntTypeContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#returnStmt.
    def visitReturnStmt(self, ctx:MiniDecafParser.ReturnStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#exprStmt.
    def visitExprStmt(self, ctx:MiniDecafParser.ExprStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#nullStmt.
    def visitNullStmt(self, ctx:MiniDecafParser.NullStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#IfStmt.
    def visitIfStmt(self, ctx:MiniDecafParser.IfStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#blockStmt.
    def visitBlockStmt(self, ctx:MiniDecafParser.BlockStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#forDeclStmt.
    def visitForDeclStmt(self, ctx:MiniDecafParser.ForDeclStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#forStmt.
    def visitForStmt(self, ctx:MiniDecafParser.ForStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#whileStmt.
    def visitWhileStmt(self, ctx:MiniDecafParser.WhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#doWhileStmt.
    def visitDoWhileStmt(self, ctx:MiniDecafParser.DoWhileStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#breakStmt.
    def visitBreakStmt(self, ctx:MiniDecafParser.BreakStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#continueStmt.
    def visitContinueStmt(self, ctx:MiniDecafParser.ContinueStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#decl.
    def visitDecl(self, ctx:MiniDecafParser.DeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#blockItemStmt.
    def visitBlockItemStmt(self, ctx:MiniDecafParser.BlockItemStmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#blockItemDecl.
    def visitBlockItemDecl(self, ctx:MiniDecafParser.BlockItemDeclContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#block.
    def visitBlock(self, ctx:MiniDecafParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#expr.
    def visitExpr(self, ctx:MiniDecafParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#tAsgn.
    def visitTAsgn(self, ctx:MiniDecafParser.TAsgnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#cAsgn.
    def visitCAsgn(self, ctx:MiniDecafParser.CAsgnContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#tCond.
    def visitTCond(self, ctx:MiniDecafParser.TCondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#cCond.
    def visitCCond(self, ctx:MiniDecafParser.CCondContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#cLor.
    def visitCLor(self, ctx:MiniDecafParser.CLorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#tLor.
    def visitTLor(self, ctx:MiniDecafParser.TLorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#tLand.
    def visitTLand(self, ctx:MiniDecafParser.TLandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#cLand.
    def visitCLand(self, ctx:MiniDecafParser.CLandContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#tEq.
    def visitTEq(self, ctx:MiniDecafParser.TEqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#cEq.
    def visitCEq(self, ctx:MiniDecafParser.CEqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#tRel.
    def visitTRel(self, ctx:MiniDecafParser.TRelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#cRel.
    def visitCRel(self, ctx:MiniDecafParser.CRelContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#cAdd.
    def visitCAdd(self, ctx:MiniDecafParser.CAddContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#tAdd.
    def visitTAdd(self, ctx:MiniDecafParser.TAddContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#tMul.
    def visitTMul(self, ctx:MiniDecafParser.TMulContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#cMul.
    def visitCMul(self, ctx:MiniDecafParser.CMulContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#tUnary.
    def visitTUnary(self, ctx:MiniDecafParser.TUnaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#cUnary.
    def visitCUnary(self, ctx:MiniDecafParser.CUnaryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#tCast.
    def visitTCast(self, ctx:MiniDecafParser.TCastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#cCast.
    def visitCCast(self, ctx:MiniDecafParser.CCastContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#postfixArray.
    def visitPostfixArray(self, ctx:MiniDecafParser.PostfixArrayContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#postfixCall.
    def visitPostfixCall(self, ctx:MiniDecafParser.PostfixCallContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#tPostfix.
    def visitTPostfix(self, ctx:MiniDecafParser.TPostfixContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#argList.
    def visitArgList(self, ctx:MiniDecafParser.ArgListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#atomInteger.
    def visitAtomInteger(self, ctx:MiniDecafParser.AtomIntegerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#atomParen.
    def visitAtomParen(self, ctx:MiniDecafParser.AtomParenContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#atomIdent.
    def visitAtomIdent(self, ctx:MiniDecafParser.AtomIdentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#unaryOp.
    def visitUnaryOp(self, ctx:MiniDecafParser.UnaryOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#addOp.
    def visitAddOp(self, ctx:MiniDecafParser.AddOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#mulOp.
    def visitMulOp(self, ctx:MiniDecafParser.MulOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#relOp.
    def visitRelOp(self, ctx:MiniDecafParser.RelOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#eqOp.
    def visitEqOp(self, ctx:MiniDecafParser.EqOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by MiniDecafParser#asgnOp.
    def visitAsgnOp(self, ctx:MiniDecafParser.AsgnOpContext):
        return self.visitChildren(ctx)



del MiniDecafParser