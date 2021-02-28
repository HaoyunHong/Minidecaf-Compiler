# Report

洪昊昀    计82    2017010591

## 1. 任务

增加对多函数和声明、定义、调用函数的支持。

## 2. 实验内容

修改或新增的语法规范如下：

```g4
prog
    : externalDecl + EOF
    ;

externalDecl
    : func # funcExternalDecl
    ;

func
    : ty Ident '(' paramList ')' block # funcDef
    | ty Ident '(' paramList ')' ';' # funcDecl
    ;

paramList
    : (decl (',' decl)*)?
    ;

expr
    : asgn
    ;

asgn
    : cond # tAsgn
    | unary asgnOp asgn # cAsgn
    ;

postfix
    : atom # tPostfix
    | postfix '[' expr ']' # postfixArray
    | Ident '(' argList ')' # postfixCall
    ;

argList
    : (expr (',' expr)*)?
    ;
```

为了处理多函数和函数的声明、定义、调用，我主要在代码中增加了具有如注释所示功能的内容：

```python
class IRFunc: # 存储一个函数信息
    def __init__(self, name, nParams, instrs):
        self.name = name # 函数名
        self.nParams = nParams # 函数参数个数
        self.instrs = instrs # 指令序列
    
class IRProg: # 存储所有函数信息
    def __init__(self, funcs:[IRFunc]):
        self.funcs = funcs
        
class Call(IRInstr): # 调用函数
    def __init__(self, func):
        self.func = func

    def __str__(self):
        return f"call {self.func}"

    def accept(self, visitor):
        visitor.visitCall(self)

# 下面两个函数分别处理函数声明和定义，IR 生成的 Visitor 遍历 AST 时的情况
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

# 存储函数名信息
class FuncNameInfo:
    def __init__(self, hasDef=True):
        self._v = {}
        self._pos = {}
        self.blockSlots = {}
        self.hasDef = hasDef
        
# 生成函数asm
def genFunc(self, func):
    self.curFunc = func.name
    self.genPrologue(func)
    for instr in func.instrs:
        self._E([
            AsmComment(instr)])
        instr.accept(self)
        self.genEpilogue(func)
```



## 3. 思考题

### 3.1

MiniDecaf 的函数调用时参数求值的顺序是未定义行为。试写出一段 MiniDecaf 代码，使得不同的参数求值顺序会导致不同的返回结果。

```c++
int fun(int a, int b) {
    int s = 10 * a + 9 * b;
    return s;
}

int main() {
    int x = 10;
    int ans = fun(x++, x);
    return ans;
}
```

## 4.

在step8的基础上，我主要借鉴了参考代码中irgen和name的部分，在这次实验中我对多函数和函数调用的处理的理解更加深入 了，也能够在有bug的参考实现的思路的基础上根据自己的理解实现正确的代码。

