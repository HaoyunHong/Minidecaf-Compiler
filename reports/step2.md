
# Report

洪昊昀    计82    2017010591

## 1. 任务

给整数常量增加一元运算：取负 `-`、按位取反 `~` 以及逻辑非 `!`。

## 2. 实验内容

我在step1的基础上新增了3个一元操作符token，然后把三条指令整合成一条`unary(op)`，遍历 AST，在遇到一元表达式时，先生成子表达式的 IR，再根据操作符类型生成 `neg` 或 `not` 或 `lnot`，最后由 IR 生成对应的汇编。

## 3. 思考题

我们在语义规范中规定整数运算越界是未定义行为，运算越界可以简单理解成理论上的运算结果没有办法保存在32位整数的空间中，必须截断高于32位的内容。请设计一个表达式，只使用`-~!`这三个单目运算符和 $[0, 2^{31} - 1]$ 范围内的非负整数，使得运算过程中发生越界。

答：对于$[0,2^{31}-1）$范围内的任意一个数a，令表达式为$-!\sim a=-0=0xFFFFFFFF+1=0x100000000$，发生越界。

## 4.

在step1的基础上，我主要借鉴了参考代码中ir和asm的部分，虽然我没有办法完全靠自己写出来，但已经理解了它的思路。相比做 step1 时的手足无措，在这次实验中我对实验的理解更加深入了。