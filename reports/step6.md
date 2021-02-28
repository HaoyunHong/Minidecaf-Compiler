# Report

洪昊昀    计82    2017010591

## 1. 任务

要使编译器支持 if 语句和条件表达式。

## 2. 实验内容

修改或新增的语法规范如下：

```
func
    : ty 'main' '(' ')' block
    ;
stmt
    : 'return' expr ';' # returnStmt
    | expr ';' # exprStmt
    | ';' # nullStmt
    | 'if' '(' expr ')' th=stmt ('else' el=stmt)? # IfStmt
    | block # blockStmt
    ;

blockItem
    : stmt # blockItemStmt
    | decl ';' # blockItemDecl
    ;

block
    : '{' blockItem* '}'
    ;
```

## 3. 思考题

### 3.1 Rust 和 Go 语言中的 if-else 语法与 C 语言中略有不同，它们都要求两个分支必须用大括号包裹起来，而且条件表达式不需要用括号包裹起来。请问相比 C 的语法，这两种语言的语法有什么优点？

这两种语言的语法不会有悬吊 else 问题，因为有大括号，可以通过解析大括号的匹配得到 if-else 的匹配关系。

## 4.

在step4的基础上，我主要借鉴了参考代码中ir和asm的部分，在这次实验中我对实验和 antlr4 工具的理解更加深入了，能够在有bug的参考实现的思路的基础上根据自己的理解实现正确的代码。

