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

enum CmdType {
  T_DECL = 0,
  T_DECLANDASGN,
  T_DECL_ARRAY,
  T_DECLANDASGN_ARRAY,
  T_DECLANDASGN_STRING,
  T_ASGN,
  T_SEQ,
  T_IF,
  T_WHILE,
  T_WI,
  T_WC
};

struct expr {
  enum ExprType t;
  union {
    struct {unsigned int value; } CONST;
    struct {char * name; } VAR;
    struct {char * value; } CHAR;
    struct {char * value; } STRING;
    struct {char * name; struct expr * num; } ARRAY;
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

struct cmd {
  enum CmdType t;
  union {
    struct {char * name; } DECL;
    struct {char * name; struct expr * value; } DECLANDASGN;
    struct {char * name; unsigned int size; } DECL_ARRAY;
    struct {char * name; unsigned int size; struct expr_list * value; } DECLANDASGN_ARRAY;
    struct {char * name; struct expr * value; } DECLANDASGN_STRING;
    struct {struct expr * left; struct expr * right; } ASGN;
    struct {struct cmd * left; struct cmd * right; } SEQ;
    struct {struct expr * cond; struct cmd * left; struct cmd * right; } IF;
    struct {struct expr * cond; struct cmd * body; } WHILE;
    struct {struct expr * arg; } WI;
    struct {struct expr * arg; } WC;
  } d;
};

struct cmd_list {
  struct cmd * data;
  struct cmd_list * next;
};

enum DeclItemType {

};

struct decl_item {

};

struct decl_list {
    struct decl_item * data;
    struct decl_list * next;
};


struct expr_list * TENil();
struct expr_list * TECons(struct expr * data, struct expr_list * next);
struct cmd_list * TCNil();
struct cmd_list * TCCons(struct cmd * data, struct cmd_list * next);
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
struct cmd * TDecl(char * name);
struct cmd * TDecl_Array(char * name, unsigned int size);
struct cmd * TDeclAndAsgn(char * name, struct expr * value);
struct cmd * TDeclAndAsgn_Array(char * name, unsigned int size, struct expr_list * value);
struct cmd * TDeclAndAsgn_String(char * name, struct expr * value);
struct cmd * TAsgn(struct expr * left, struct expr * right);
struct cmd * TSeq(struct cmd * left, struct cmd * right);
struct cmd * TIf(struct expr * cond, struct cmd * left, struct cmd * right);
struct cmd * TWhile(struct expr * cond, struct cmd * body);
struct cmd * TWriteInt(struct expr * arg);
struct cmd * TWriteChar(struct expr * arg);
struct decl_list * TDeclList_Var(struct decl_item * p);
struct decl_list * TDeclList_Array(struct decl_item * p);

void print_binop(enum BinOpType op);
void print_unop(enum UnOpType op);
void print_expr(struct expr * e);
void print_expr_list(struct expr_list * es);
void print_cmd(struct cmd * c);

#endif // LANG_H_INCLUDED
