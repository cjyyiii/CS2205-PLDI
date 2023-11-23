# CS2205-PLDI
大作业选题：带数组与字符串类型的程序语言的词法分析与语法分析  
这个任务中，你需要在 While 语言中加入数组与字符串。
要求 1：在 While 语言中加入数组相关的变量声明与表达式，并完成词法分析、语法分析与语法树输出。
要求 2：支持变量声明的同时初始化，包括对于数组的初始化。
要求 3：支持字符串常量，以及一句语句同时声明多个变量。

while语言
E :: = N | V | -E | E+E | E-E | E*E | E/E | E%E |
E<E | E<=E | E==E | E!=E | E>=E | E>E |
E&&E | E||E | !E

C :: = var V |
V = E |
C; C |
if (E) then { C } else { C } |
while (E) do { C }

要求1：在 While 语言中加入数组相关的变量声明与表达式
E :: = N | V | V[E] | -E | E+E | E-E | E*E | E/E | E%E |
E<E | E<=E | E==E | E!=E | E>=E | E>E |
E&&E | E||E | !E

C :: = var V | array V[N]
V = E | V[E] = E
C; C |
if (E) then { C } else { C } |
while (E) do { C } |

要求2：支持变量声明的同时初始化，包括对于数组的初始化
E :: = N | V | V[E] | -E | E+E | E-E | E*E | E/E | E%E |
E<E | E<=E | E==E | E!=E | E>=E | E>E |
E&&E | E||E | !E

L::= E,E,……,E

C :: = var V | array V[N] | var V = E | array V[N]={L}
V = E | V[E] = E
C; C |
if (E) then { C } else { C } |
while (E) do { C } |

（最终版）要求3：支持字符串常量，以及一句语句同时声明多个变量
E :: = N | V | S | CH | V[E] | -E | E+E | E-E | E*E | E/E | E%E |
E<E | E<=E | E==E | E!=E | E>=E | E>E |
E&&E | E||E | !E

L :: = E,E,……,E

D1 :: = V | V = E | V = CH
D2 :: = V[N] | V[N] = {L} | V[N] = S
Q1 :: = var D1,D1,……,D1
Q2 :: = array D2,D2,……,D2

C :: = Q1 | Q2
V = E | V[E] = E
C; C |
if (E) then { C } else { C } |
while (E) do { C } |