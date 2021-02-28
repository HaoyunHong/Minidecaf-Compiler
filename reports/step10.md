# Report

洪昊昀    计82    2017010591

## 1. 任务

增加对全局变量的支持

## 2. 实验内容

修改或新增的语法规范如下：

```
externalDecl
    : func # funcExternalDecl
    | decl ';' # declExternalDecl
    ;
```

为了处理多函数和函数的声明、定义、调用，我主要在代码中增加了具有如注释所示功能的如下内容：

```python
class IRGlob: # 全局变量IR
    def __init__(self, sym, size, init=None, align=INT_BYTES):
        self.size = size # 字节大小
        self.init = init # 初始值
        
class GlobInfo: # 存储全局变量信息
    def __init__(self, var, size, init=None):
        self.var = var # 值
        self.size = var.size # 字节大小
        self.init = init # 初始值

# 全局变量asm
@Instrs 
def globalSymbol(sym):
    return [f"la t1, {sym}"] + push("t1")
```

## 3. 思考题

### 3.1

请给出将全局变量 `a` 的值读到寄存器 `t0` 所需的 riscv 指令序列。

```assembly
lui t0, %hi(a)
addi t0, t0, %lo(a)
```

## 4.

在step9的基础上，我主要借鉴了参考代码中irgen和name的部分，在这次实验中我对如何处理全局变量的理解更加深入 了，也能够在有bug的参考实现的思路的基础上根据自己的理解实现正确的代码。

