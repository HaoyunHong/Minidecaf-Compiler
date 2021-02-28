# Report

洪昊昀    计82    2017010591

## 1. 任务

在编译器中增加变量，包括变量的声明，变量的使用（读取/赋值），使得main 函数可以包含多条语句和声明，要引入栈帧确定变量存放在哪里、如何访问。

## 2. 实验内容

修改或新增部分的语法规范如下：

```
func
    : ty 'main' '(' ')' '{' stmt* '}'
    ;

stmt
    : 'return' expr ';' # returnStmt
    | decl ';' # declStmt
    | expr ';' # exprStmt
    | ';' # nullStmt
    | 'if' '(' expr ')' th=stmt ('else' el=stmt)? # IfStmt
    | block # blockStmt
    ;
	
decl
	: ty Ident ('=' expr)?
	;
```

对于符号表，我复用了参考实现中的如下类，用来存储变量名与栈帧地址的键值对。

```python
# 此处相当于符号表
class OffsetManager:
    def __init__(self):
        self._off = {}
        self._top = 0

    def __getitem__(self, var):
        return self._off[var]

    def newSlot(self, var=None):
        # 如果重复声明变量就报错
        if var in self._off:
            raise MiniDecafError("repeated declaration")
        self._top -= INT_BYTES
        if var is not None:
            self._off[var] = self._top
        return self._top
```

## 3. 思考题

### 3.1 描述程序运行过程中函数栈帧的构成，分成哪几个部分？每个部分所用空间最少是多少？

运行过程中函数栈帧分成3部分，最高位存放的是是函数的返回地址和上一个栈帧基址，共 8 字节，所用空间最少是8字节；然后是当前可用的所有局部变量，大小为 `4 * 局部变量个数`，所用空间最少是0字节；然后是运算栈，位于栈顶，大小随计算过程变化，当不在计算某表达式的过程中时为空，所用空间最少是0字节。

### 3.2如果 MiniDecaf 也允许多次定义同名变量，并规定新的定义会覆盖之前的同名定义，请问在你的实现中，需要对定义变量和查找变量的逻辑做怎样的修改？

处理定义变量的声明语句时，不需要在已有同名变量时进行报错，并且需要先计算等号右侧表达式的值，再存储局部变量，然后将该变量信息加入符号表（当没有该变量时）或者更改已加入的同名变量信息。

## 4.

在step4的基础上，我主要借鉴了参考代码中ir和asm的部分，在这次实验中我对实验和 antlr4 工具的理解更加深入了，能够在有bug的参考实现的思路的基础上根据自己的理解实现正确的代码。

