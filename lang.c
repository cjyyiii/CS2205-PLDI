#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "lang.h"

struct expr * new_expr_ptr() {
  struct expr * res = (struct expr *) malloc(sizeof(struct expr));
  if (res == NULL) {
    printf("Failure in malloc.\n");
    exit(0);
  }
  return res;
}

struct expr_list * new_expr_list_ptr() {
  struct expr_list * res =
    (struct expr_list *) malloc(sizeof(struct expr_list));
  if (res == NULL) {
    printf("Failure in malloc.\n");
    exit(0);
  }
  return res;
}

struct cmd * new_cmd_ptr() {
  struct cmd * res = (struct cmd *) malloc(sizeof(struct cmd));
  if (res == NULL) {
    printf("Failure in malloc.\n");
    exit(0);
  }
  return res;
}

struct expr_list * TENil() {
  return NULL;
}

struct expr_list * TECons(struct expr * data, struct expr_list * next) {
  struct expr_list * res = new_expr_list_ptr();
  res -> data = data;
  res -> next = next;
  return res;
}

struct cmd_list * TCNil() {
  return NULL;
}

struct cmd_list * TCCons(struct cmd * data, struct cmd_list * next) {
  struct cmd_list * res = new_cmd_list_ptr();
  res -> data = data;
  res -> next = next;
  return res;
}

struct expr * TConst(unsigned int value) {
  struct expr * res = new_expr_ptr();
  res -> t = T_CONST;
  res -> d.CONST.value = value;
  return res;
}

struct expr * TVar(char * name) {
  struct expr * res = new_expr_ptr();
  res -> t = T_VAR;
  res -> d.VAR.name = name;
  return res;
}

struct expr * TChar(char * value) {
  struct expr * res = new_expr_ptr();
  res -> t = T_VAR;
  res -> d.VAR.name = name;
  return res;
}//todo

struct expr * TString(char * value) {
  struct expr * res = new_expr_ptr();
  res -> t = T_VAR;
  res -> d.VAR.name = name;
  return res;
}//todo

struct expr * TArray(char * name, struct expr * num) {
  struct expr * res = new_expr_ptr();
  res -> t = T_ARRAY;
  res -> d.ARRAY.name = name;
  res -> d.ARRAY.num = new_expr_ptr();
  res -> d.ARRAY.num->d= num->d;
  res -> d.ARRAY.num->t= num->t;
  return res;
}

struct expr * TBinOp(enum BinOpType op, struct expr * left, struct expr * right) {
  struct expr * res = new_expr_ptr();
  res -> t = T_BINOP;
  res -> d.BINOP.op = op;
  res -> d.BINOP.left = left;
  res -> d.BINOP.right = right;
  return res;
}

struct expr * TUnOp(enum UnOpType op, struct expr * arg) {
  struct expr * res = new_expr_ptr();
  res -> t = T_UNOP;
  res -> d.UNOP.op = op;
  res -> d.UNOP.arg = arg;
  return res;
}

struct expr * TMalloc(struct expr * arg) {
  struct expr * res = new_expr_ptr();
  res -> t = T_MALLOC;
  res -> d.MALLOC.arg = arg;
  return res;
}

struct expr * TReadInt() {
  struct expr * res = new_expr_ptr();
  res -> t = T_RI;
  return res;
}

struct expr * TReadChar() {
  struct expr * res = new_expr_ptr();
  res -> t = T_RC;
  return res;
}

struct cmd * TDecl(char * name) {
  struct cmd * res = new_cmd_ptr();
  res -> t = T_DECL;
  res -> d.DECL.name = name;
  return res;
}

struct cmd * TDeclAndAsgn(char * name, struct expr * value) {
  struct cmd * res = new_cmd_ptr();
  res -> t = T_DECLANDASGN;
  res -> d.DECLANDASGN.name = name;
  res -> d.DECLANDASGN.value = value;
  return res;
}

struct cmd * TDecl_Array(char * name, unsigned int size) {
  struct cmd * res = new_cmd_ptr();
  res -> t = T_DECL_ARRAY;
  res -> d.DECL_ARRAY.name = name;
  res -> d.DECL_ARRAY.size = size;
  return res;
}

struct cmd * TDeclAndAsgn_Array(char * name, unsigned int size, struct expr_list * value) {
  struct cmd * res = new_cmd_ptr();
  res -> t = T_DECLANDASGN_ARRAY;
  res -> d.DECLANDASGN_ARRAY.name = name;
  res -> d.DECLANDASGN_ARRAY.size = size;
  res -> d.DECLANDASGN_ARRAY.value = value;
  return res;
}

struct cmd * TDeclAndAsgn_String(char * name, struct expr * value) {
  struct cmd * res = new_cmd_ptr();
  res -> t = T_DECLANDASGN_ARRAY;
  res -> d.DECLANDASGN_ARRAY.name = name;
  res -> d.DECLANDASGN_ARRAY.size = size;
  res -> d.DECLANDASGN_ARRAY.value = value;
  return res;
}//todo

struct cmd * TAsgn(struct expr * left, struct expr * right) {
  struct cmd * res = new_cmd_ptr();
  res -> t = T_ASGN;
  res -> d.ASGN.left = left;
  res -> d.ASGN.right = right;
  return res;
}

struct cmd * TSeq(struct cmd * left, struct cmd * right) {
  struct cmd * res = new_cmd_ptr();
  res -> t = T_SEQ;
  res -> d.SEQ.left = left;
  res -> d.SEQ.right = right;
  return res;
}

struct cmd * TIf(struct expr * cond, struct cmd * left, struct cmd * right) {
  struct cmd * res = new_cmd_ptr();
  res -> t = T_IF;
  res -> d.IF.cond = cond;
  res -> d.IF.left = left;
  res -> d.IF.right = right;
  return res;
}

struct cmd * TWhile(struct expr * cond, struct cmd * body) {
  struct cmd * res = new_cmd_ptr();
  res -> t = T_WHILE;
  res -> d.WHILE.cond = cond;
  res -> d.WHILE.body = body;
  return res;
}

struct cmd * TWriteInt(struct expr * arg) {
  struct cmd * res = new_cmd_ptr();
  res -> t = T_WI;
  res -> d.WI.arg = arg;
  return res;
}

struct cmd * TWriteChar(struct expr * arg) {
  struct cmd * res = new_cmd_ptr();
  res -> t = T_WC;
  res -> d.WC.arg = arg;
  return res;
}

void print_binop(enum BinOpType op) {
  switch (op) {
  case T_PLUS:
    printf("PLUS");
    break;
  case T_MINUS:
    printf("MINUS");
    break;
  case T_MUL:
    printf("MUL");
    break;
  case T_DIV:
    printf("DIV");
    break;
  case T_MOD:
    printf("MOD");
    break;
  case T_LT:
    printf("LT");
    break;
  case T_GT:
    printf("GT");
    break;
  case T_LE:
    printf("LE");
    break;
  case T_GE:
    printf("GE");
    break;
  case T_EQ:
    printf("EQ");
    break;
  case T_NE:
    printf("NE");
    break;
  case T_AND:
    printf("AND");
    break;
  case T_OR:
    printf("OR");
    break;
  }
}

void print_unop(enum UnOpType op) {
  switch (op) {
  case T_UMINUS:
    printf("UMINUS");
    break;
  case T_NOT:
    printf("NOT");
    break;
  }
}

void print_expr(struct expr * e) {
  switch (e -> t) {
  case T_CONST:
    printf("CONST(%d)", e -> d.CONST.value);
    break;
  case T_VAR:
    printf("VAR(%s)", e -> d.VAR.name);
    break;
  case T_ARRAY:
    printf("ARRAY(%s,", e -> d.ARRAY.name);
    print_expr( e -> d.ARRAY.num);
    printf(")");
    break;
  case T_BINOP:
    print_binop(e -> d.BINOP.op);
    printf("(");
    print_expr(e -> d.BINOP.left);
    printf(",");
    print_expr(e -> d.BINOP.right);
    printf(")");
    break;
  case T_UNOP:
    print_unop(e -> d.UNOP.op);
    printf("(");
    print_expr(e -> d.UNOP.arg);
    printf(")");
    break;
  case T_MALLOC:
    printf("MALLOC(");
    print_expr(e -> d.MALLOC.arg);
    printf(")");
    break;
  case T_RI:
    printf("READ_INT()");
    break;
  case T_RC:
    printf("READ_CHAR()");
    break;
  }
}

void print_expr_list(struct expr_list * es) {
  if (es == NULL) {
    return;
  }
  printf(",");
  print_expr(es -> data);
  print_expr_list(es -> next);
}

void print_cmd(struct cmd * c) {
  switch (c -> t) {
  case T_DECL:
    printf("DECL(%s)", c -> d.DECL.name);
    break;
  case T_DECLANDASGN:
    printf("DECLANDASGN(%s", c -> d.DECLANDASGN.name);
    print_expr(c -> d.DECLANDASGN.value);
    printf(")");
    break;
  case T_DECL_ARRAY:
    printf("DECL_ARRAY(%s,%d)", c -> d.DECL_ARRAY.name, c -> d.DECL_ARRAY.size);
    break;
  case T_DECLANDASGN_ARRAY:
    printf("DECLANDASGN_ARRAY(%s,%d", c -> d.DECLANDASGN_ARRAY.name, c -> d.DECLANDASGN_ARRAY.size);
    print_expr_list(c -> d.DECLANDASGN_ARRAY.value);
    printf(")");
    break;  
  case T_ASGN:
    printf("ASGN(");
    print_expr(c -> d.ASGN.left);
    printf(",");
    print_expr(c -> d.ASGN.right);
    printf(")");
    break;
  case T_SEQ:
    printf("SEQ(");
    print_cmd(c -> d.SEQ.left);
    printf(",");
    print_cmd(c -> d.SEQ.right);
    printf(")");
    break;
  case T_IF:
    printf("IF(");
    print_expr(c -> d.IF.cond);
    printf(",");
    print_cmd(c -> d.IF.left);
    printf(",");
    print_cmd(c -> d.IF.right);
    printf(")");
    break;
  case T_WHILE:
    printf("WHILE(");
    print_expr(c -> d.WHILE.cond);
    printf(",");
    print_cmd(c -> d.WHILE.body);
    printf(")");
    break;
  case T_WI:
    printf("WRITE_INT(");
    print_expr(c -> d.WI.arg);
    printf(")");
    break;
  case T_WC:
    printf("WRITE_CHAR(");
    print_expr(c -> d.WC.arg);
    printf(")");
    break;
  }
}
