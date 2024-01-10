# CS2205-PLDI
大作业选题：带数组与字符串类型的程序语言的词法分析与语法分析 

选题要求： 这个任务中，你需要在 While 语言中加入数组与字符串。
- 要求 1：在 While 语言中加入数组相关的变量声明与表达式，并完成词法分析、语法分析与语法树输出。
- 要求 2：支持变量声明的同时初始化，包括对于数组的初始化。
- 要求 3：支持字符串常量，以及一句语句同时声明多个变量。

## 编译相关
要编辑此项目，使用```make```编译后，用```./main sample_src00.jtl```运行示例程序

## 语法设计

while语言语法为:

```
E :: = N | V | -E | E+E | E-E | E*E | E/E | E%E |
E<E | E<=E | E==E | E!=E | E>=E | E>E |
E&&E | E||E | !E

C :: = var V |
V = E |
C; C |
if (E) then { C } else { C } |
while (E) do { C }
```

要求1：在 While 语言中加入数组相关的变量声明与表达式
```
E :: = N | V | V[E] | -E | E+E | E-E | E*E | E/E | E%E |
E<E | E<=E | E==E | E!=E | E>=E | E>E |
E&&E | E||E | !E

C :: = var V | array V[N]
V = E | V[E] = E
C; C |
if (E) then { C } else { C } |
while (E) do { C } |
```

要求2：支持变量声明的同时初始化，包括对于数组的初始化
```
E :: = N | V | V[E] | -E | E+E | E-E | E*E | E/E | E%E |
E<E | E<=E | E==E | E!=E | E>=E | E>E |
E&&E | E||E | !E

L::= E,E,……,E

C :: = var V | array V[N] | var V = E | array V[N]={L}
V = E | V[E] = E
C; C |
if (E) then { C } else { C } |
while (E) do { C } |
```

要求3：支持字符串常量，以及一句语句同时声明多个变量
```
E :: = N | V | S | CH | V[E] | -E | E+E | E-E | E*E | E/E | E%E |
E<E | E<=E | E==E | E!=E | E>=E | E>E |
E&&E | E||E | !E

ES :: = E,E,……,E

D1 :: = V | V = E 
D2 :: = V[N] | V[N] = {ES} | V = S
DS :: = var D1,D1,……,D1 | array D2,D2,……,D2

C :: = DS |
V = E | V[E] = E
C; C |
if (E) then { C } else { C } |
while (E) do { C } |
```

## 语言特性
- 不检查输入的合法性,默认输入语法正确
- 数组类型变量和字符串常量的声明和定义用array声明,数组类型支持同时声明变量和初始化或仅声明,字符串常量以""识别,需声明的同时给出常量的值;单个字符和其他变量用var声明,可同时声明和初始化多个变量,单个字符以''识别
- 字符串常量在输出声明和初始化时,先输出字符串常量本身(为避免转义字符\r对输出造成的影响，直接输出转义字符),再依次输出字符串常量中每个字符的ASCII码(转义字符会输出为转义字符的ASCII码,如\n输出为10而非92, 110).单个字符在输出声明和初始化时,输出格式为VAR(字符本身,字符对应ASCII码)