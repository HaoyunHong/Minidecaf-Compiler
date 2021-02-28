# Report

洪昊昀    计82    2017010591

## 1. 任务

增加对循环语句，以及 break/continue 的支持。

## 2. 实验内容

修改或新增的语法规范如下：

```
stmt
    : 'return' expr ';' # returnStmt
    | expr ';' # exprStmt
    | ';' # nullStmt
    | 'if' '(' expr ')' th=stmt ('else' el=stmt)? # IfStmt
    | block # blockStmt
    | 'for' '(' init=decl ';' ctrl=expr? ';' post=expr? ')' stmt # forDeclStmt
    | 'for' '(' init=expr? ';' ctrl=expr? ';' post=expr? ')' stmt # forStmt
    | 'while' '(' expr ')' stmt # whileStmt
    | 'do' stmt 'while' '(' expr ')' ';' # doWhileStmt
    | 'break' ';' # breakStmt
    | 'continue' ';' # continueStmt
    ;
```

## 3. 思考题

### 3.1从执行的指令的条数这个角度（`label` 指令不计算在内，假设循环体至少执行了一次），请评价这两种翻译方式哪一种更好？

我认为第一种翻译方式更好，因为它执行的指令条数更少，第二种多了一次得到`cond 的 IR`，也多了一次`bnez BEGINLOOP_LABEL`。

## 4.

在step7的基础上，我主要借鉴了参考代码中irgen和name的部分，在这次实验中我对循环语句和break/continue的理解更加深入 了，也能够在有bug的参考实现的思路的基础上根据自己的理解实现正确的代码。

