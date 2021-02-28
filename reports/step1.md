
# Report

洪昊昀    计82    2017010591

## 1.

### 1.1 任务

#### 1.1.1 在不同输入上，运行 minilexer, miniparser 和 minivisitor

当输入为：（正确的符合条件的代码）

```Python
lexer.setInput("""\
    int main() {
        return 1;
    }
    """)
```

minilexer, miniparser 和 minivisitor 均能正确运行。

当输入为：（带有未知符号的代码）

```python
lexer.setInput("""\
    int main() {   	
        return '1';
    }
    """)
```

minilexer, miniparser 和 minivisitor 均不能正确运行。

当输入为：（括号不匹配的代码）

```python
lexer.setInput("""\
    int main() {   	
        return 1;
    """)
```

minilexer 能正确运行， miniparser 和 minivisitor 均不能正确运行。

当输入为：

```python
lexer.setInput("""\
    int main() {   	
        return 10000000000;
    }
    """)
```

minilexer 和miniparser 能正确运行，minivisitor 均不能正确运行。 

### 1.2 思考题

#### 1.2.1 修改 minilexer 的输入（`lexer.setInput` 的参数），使得 lex 报错，给出一个简短的例子

当输入为：

```python
lexer.setInput("""\
    int main() {
        return '1';
    }
    """)
```

lex报错为：

```
line 45, in lex
    raise Exception(f"lex error at input position {self.pos}")
Exception: lex error at input position 40
```

#### 1.2.2 修改 minilexer 的输入，使得 lex 不报错但 parse 报错，给出一个简短的例子

当输入为：

```
    lexer.setInput("""\
        int main() {
            return 123;
    """)
```

parse报错为：

```
line 39, in parse
    tok = next(self.lex)
StopIteration
```

#### 1.2.3 在 riscv 中，哪个寄存器是用来存储函数返回值的？

在 riscv 中，$a_0$寄存器是用来存储函数返回值的。

## 2.

### 2.1选择使用工具ANTLR，编写 step1 的 MiniDecaf 词法语法，以利用该工具进行解析。然后，从 AST 生成汇编

实际需要被使用的词法规则如下：

```
Int
    : 'int'
    ;

Return
    : 'return'
    ;


Lparen : '(' ;
Rparen : ')' ;
Lbrace : '{' ;
Rbrace : '}' ;
Semicolon : ';' ;

Punctuator
    : Lparen
    | Rparen
    | Lbrace
    | Rbrace
    | Semicolon
    ;

Integer
    : [0-9]+
    ;

Whitespace
    : [ \t\n\r]+ -> skip
    ;
```

实际需要被使用的语法规则如下：

```
prog
    : func EOF
    ;

func
    : ty 'main' '(' ')' '{' stmt '}'
    ;

ty
    : 'int' # intType
    ;

stmt
    : 'return' expr ';' # returnStmt
    ;

expr
    : Integer
    ;
```

若输入的C代码为：

```python
int main(){return 123;}
```

得到AST为：

```
(prog (func (ty int) main ( ) { (stmt return (expr 123) ;) }) <EOF>)
```

## 3.

### 3.1 改进上一步的代码，先生成 IR，再从 IR 生成汇编。

从 AST 到 IR：按如下规则访问 AST 中的节点：

1. 遇到 `Integer(X)`：生成一条 `push X`。
2. 遇到 `Return expr ;`：先生成 `expr` 对应的 IR，然后生成一条 `ret`。

IR 翻译到汇编：

| IR       | 汇编                                        |
| -------- | ------------------------------------------- |
| `push X` | `addi sp, sp, -4 ; li t1, X ; sw t1, 0(sp)` |
| `ret`    | `lw a0, 0(sp) ; addi sp, sp, 4 ; jr ra`     |

对于 `int main(){return 123;}`，生成如下汇编：

```
    .text
    .globl main
main:
    addi sp, sp, -4
    li t1, 233
    sw t1, 123(sp)
    lw a0, 123(sp)
    addi sp, sp, 4
    jr ra
```

## 4.

我主要复用了参考代码中ir和asm的部分，虽然我没有办法完全靠自己写出来，但也通读了参考代码，掌握了它的思路，我借鉴了main函数部分与CommonLex部分，了解了代码中划分功能层次与解耦的思想、异常的处理方法，也学习了写代码的规范。本次实验对我来说挑战很大，而且也踩了不少坑qwq，很抱歉没有按时完成，但是通过自学、询问助教和同学以及看示例代码，我学到了很多，也对编译有了进一步的了解，希望在以后的实验中能够更加顺利一些吧~