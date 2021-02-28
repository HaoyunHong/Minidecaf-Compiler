import sys
import argparse
from antlr4 import *

from .utils import *
from .generated.MiniDecafLexer import MiniDecafLexer
from .generated.MiniDecafParser import MiniDecafParser

from .frontend import irGen, nameGen, typeCheck
from .asm import AsmEmitter
from .asm.riscv import RISCVAsmGen as AsmGen


def parseArgs(argv):
    parser = argparse.ArgumentParser(description="MiniDecaf compiler")
    parser.add_argument("infile", type=str, help="the input C file")
    parser.add_argument("outfile", type=str, nargs="?", help="the output assembly file")
    return parser.parse_args()


def nameInfoGenerator(tree):
    nameInfo = nameGen(tree)
    return nameInfo


def TypeCheck(tree, nameInfo):
    typeInfo = typeCheck(tree, nameInfo)
    return typeInfo


def irGenerator(tree, nameInfo, typeInfo):
    ir = irGen(tree, nameInfo, typeInfo)
    return ir


def asmGen(ir, fout):
    asmEmitter = AsmEmitter(fout)
    AsmGen(asmEmitter).gen(ir)


def asmGenerator(ir, outfile):
    if outfile is not None:
        with open(outfile, 'w') as fout:
            return asmGen(ir, fout)
    else:
        return asmGen(ir, sys.stdout)


def Lexer(inputStream):
    lexer = MiniDecafLexer(inputStream)
    class BailErrorListener:
        def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
            raise MiniDecafError(f"lexer error at {line},{column}")
    lexer.addErrorListener(BailErrorListener())
    return CommonTokenStream(lexer)


def Parser(tokenStream):
    parser = MiniDecafParser(tokenStream)
    parser._errHandler = BailErrorStrategy()
    tree = parser.prog()
    return tree


def main():
    try:
        args = parseArgs(sys.argv)
        inputStream = FileStream(args.infile)
        tokenStream = Lexer(inputStream)
        tree = Parser(tokenStream)
        nameInfo = nameInfoGenerator(tree)
        typeInfo = TypeCheck(tree, nameInfo)
        ir = irGenerator(tree, nameInfo, typeInfo)
        asmGenerator(ir, args.outfile)
    except MiniDecafError as e:
        return 1
