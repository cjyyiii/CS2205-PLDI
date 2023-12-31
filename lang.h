#ifndef LANG_H_INCLUDED
#define LANG_H_INCLUDED

#include <stdio.h>
#include <stdlib.h>
#include "lib.h"

enum BinOpType {
  T_PLUS,
  T_MINUS,
  T_MUL,
  T_DIV,
  T_MOD,
  T_LT,
  T_GT,
  T_LE,
  T_GE,
  T_EQ,
  T_NE,
  T_AND,
  T_OR
};

enum UnOpType {
  T_UMINUS,
  T_NOT
};

enum ExprType {
  T_CONST = 0,
  T_VAR,
  T_CHAR,
  T_STRING,
  T_ARRAY,
  T_BINOP,
  T_UNOP,
  T_MALLOC,
  T_RI,
  T_RC
};

enum DeclType {//变量定义和赋初值
    T_DECL = 0,
    T_DECLANDASGN,
    T_DECL_ARRAY,
    T_DECLANDASGN_ARRAY,
    T_DECLANDASGN_STRING,
};

enum CmdType {
  T_ASGN,
  T_SEQ,
  T_IF,
  T_WHILE,
  T_WI,
  T_WC,
  T_DECL_STH,
};

struct expr {
  enum ExprType t;
  union {
    struct {unsigned int value; } CONST;
    struct {char ch; unsigned int value; } CHAR;//单个字符
    struct {char * str; unsigned int * value; unsigned int size; unsigned int * value1; } STRING;//字符串类型
    struct {char * name; } VAR;
    struct {char * name; struct expr * num; } ARRAY;//数组类型
    struct {enum BinOpType op; struct expr * left; struct expr * right; } BINOP;
    struct {enum UnOpType op; struct expr * arg; } UNOP;
    struct {struct expr * arg; } MALLOC;
    struct {void * none; } RI;
    struct {void * none; } RC;
  } d;
};

struct expr_list {
  struct expr * data;
  struct expr_list * next;
};

struct decl {
    enum DeclType t;
    union {
        struct {char * name; } DECL;
        struct {char * name; struct expr * value; } DECLANDASGN;//变量声明的同时初始化
        struct {char * name; unsigned int size; } DECL_ARRAY;
        struct {char * name; unsigned int size; struct expr_list * value; } DECLANDASGN_ARRAY;
        struct {char * name; unsigned int size; struct expr * value; } DECLANDASGN_STRING;
    }d;
};

struct decl_list {
    struct decl * data;
    struct decl_list * next;
};

struct cmd {
  enum CmdType t;
  union {
    struct {struct expr * left; struct expr * right; } ASGN;
    struct {struct cmd * left; struct cmd * right; } SEQ;
    struct {struct expr * cond; struct cmd * left; struct cmd * right; } IF;
    struct {struct expr * cond; struct cmd * body; } WHILE;
    struct {struct expr * arg; } WI;
    struct {struct expr * arg; } WC;
    struct {struct decl_list * decl_sth;}DECL_STH;
  } d;
};


struct expr_list * TENil();
struct expr_list * TECons(struct expr * data, struct expr_list * next);
struct decl_list * TDNil();
struct decl_list * TDCons(struct decl * data, struct decl_list * next);
struct expr * TConst(unsigned int value);
struct expr * TVar(char * name);
struct expr * TChar(char * value);
struct expr * TString(char * value);
struct expr * TArray(char * name, struct expr * num);
struct expr * TBinOp(enum BinOpType op, struct expr * left, struct expr * right);
struct expr * TUnOp(enum UnOpType op, struct expr * arg);
struct expr * TMalloc(struct expr * arg);
struct expr * TReadInt();
struct expr * TReadChar();
struct decl * TDecl(char * name);
struct decl * TDecl_Array(char * name, unsigned int size);
struct decl * TDeclAndAsgn(char * name, struct expr * value);
struct decl * TDeclAndAsgn_Array(char * name, unsigned int size, struct expr_list * value);
struct decl * TDeclAndAsgn_String(char * name, struct expr * value);
struct cmd * TAsgn(struct expr * left, struct expr * right);
struct cmd * TSeq(struct cmd * left, struct cmd * right);
struct cmd * TIf(struct expr * cond, struct cmd * left, struct cmd * right);
struct cmd * TWhile(struct expr * cond, struct cmd * body);
struct cmd * TWriteInt(struct expr * arg);
struct cmd * TWriteChar(struct expr * arg);
struct cmd * TDeclSth(struct decl_list * decl_sth);

void print_binop(enum BinOpType op);
void print_unop(enum UnOpType op);
void print_expr(struct expr * e);
void print_expr_list(struct expr_list * es);
void print_cmd(struct cmd * c);
void print_decl(struct decl * d);
void print_decl_list(struct decl_list * ds);

#endif // LANG_H_INCLUDED
