# Report

洪昊昀    计82    2017010591

## 1. 任务

支持指针，引入左值的概念、修改赋值，支持取地址操作符 `&` 和解引用操作符 `*`，支持类型转换。

## 2. 实验内容

修改或新增的语法规范如下：

```
ty
    : 'int'
    | ty '*'
    ;

asgn
    : cond
    | unary asgnOp asgn
    ;
    
unary
    : ...
    | '(' ty ')' unary
```

step 11 需要修改的很多：

1. 需要增加左值分析，对不合法的如`1+2=3` 或 `&(1+2)`的代码进行处理。
2. 因为禁止隐式类型转化，但允许显式类型转化，要对所有使用类型变量的部分进行类型检查，还要保证 `&` 的操作数是指针类型，`*` 的操作类型是指针类型。
3. 增加指针类型，在其中要确定左右值，要有左右值转化函数、引用和解引用函数，还要考虑到空指针，需要从0显示转换得到，解引用空指针是未定义行为。

## 3. 思考题

### 3.1

为什么类型检查要放到名称解析之后？

因为变量类型和函数返回值类型是在名称解析之后得到的，名称解析之后才能进行类型检查判断判断是否和所需类型一致。

### 3.2

MiniDecaf 中一个值只能有一种类型，但在很多语言中并非如此，请举出一个反例。

C++ 中，char 和 int 可以根据 ASCII 码隐式转换。

### 3.3

在本次实验中我们禁止进行指针的比大小运算。请问如果要实现指针大小比较需要注意什么问题？可以和原来整数比较的方法一样吗？

需要注意指针的类型，因为不同类型指针比大小没有意义。

不能和原来整数比较方法一样。

## 4.

在step10的基础上，我主要借鉴了参考代码中irgen和name的部分，在这次实验中我对如何支持指针、左值的概念、修改赋值、取地址操作符 `&` 和解引用操作符 `*`和类型转换的理解更加深入了，也能够在有bug的参考实现的思路的基础上根据自己的理解实现正确的代码。

