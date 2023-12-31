#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "lang.h"

struct expr *new_expr_ptr() {
    struct expr *res = (struct expr *) malloc(sizeof(struct expr));
    if (res == NULL) {
        printf("Failure in malloc.\n");
        exit(0);
    }
    return res;
}

struct expr_list *new_expr_list_ptr() {
    struct expr_list *res =
            (struct expr_list *) malloc(sizeof(struct expr_list));
    if (res == NULL) {
        printf("Failure in malloc.\n");
        exit(0);
    }
    return res;
}

struct cmd *new_cmd_ptr() {
    struct cmd *res = (struct cmd *) malloc(sizeof(struct cmd));
    if (res == NULL) {
        printf("Failure in malloc.\n");
        exit(0);
    }
    return res;
}

struct decl *new_decl_ptr() {
    struct decl *res = (struct decl *) malloc(sizeof(struct decl));
    if (res == NULL) {
        printf("Failure in malloc.\n");
        exit(0);
    }
    return res;
}

struct decl_list *new_decl_list_ptr() {
    struct decl_list *res =
            (struct decl_list *) malloc(sizeof(struct decl_list));
    if (res == NULL) {
        printf("Failure in malloc.\n");
        exit(0);
    }
    return res;
}

struct expr_list *TENil() {
    return NULL;
}

struct expr_list *TECons(struct expr *data, struct expr_list *next) {//合并expr_list
    struct expr_list *res = new_expr_list_ptr();
    res->data = data;
    res->next = next;
    return res;
}

struct decl_list *TDNil() {
    return NULL;
}

struct decl_list *TDCons(struct decl *data, struct decl_list *next) {//合并decl_list
    struct decl_list *res = new_decl_list_ptr();
    res->data = data;
    res->next = next;
    return res;
}

struct cmd *TDeclSth(struct decl_list *decl_sth) {//每行decl_list实质上为一个命令语句
    struct cmd *res = new_cmd_ptr();
    res->t = T_DECL_STH;
    res->d.DECL_STH.decl_sth = decl_sth;
    return res;
}

struct expr *TConst(unsigned int value) {
    struct expr *res = new_expr_ptr();
    res->t = T_CONST;
    res->d.CONST.value = value;
    return res;
}

struct expr *TChar(char *value) {
    struct expr *res = new_expr_ptr();
    res->t = T_CHAR;
    if (strlen(value) == 3) {
        res->d.CHAR.ch = value[1];
        res->d.CHAR.value = (unsigned int) value[1];
    } else {
        switch (value[2]) {
            case 97://a
                res->d.CHAR.value = 7;
                break;
            case 98://b
                res->d.CHAR.value = 8;
                break;
            case 116://t
                res->d.CHAR.value = 9;
                break;
            case 110://n
                res->d.CHAR.value = 10;
                break;
            case 118://v
                res->d.CHAR.value = 11;
                break;
            case 102://f
                res->d.CHAR.value = 12;
                break;
            case 114://r
                res->d.CHAR.value = 13;
                break;
            case 34://双引号
                res->d.CHAR.value = 34;
                break;
            case 39://单引号
                res->d.CHAR.value = 39;
                break;
            case 92://杠
                res->d.CHAR.value = 92;
                break;
        }
        res->d.CHAR.ch = (char) res->d.CHAR.value;
    }
    free(value);
    return res;
}

struct expr *TString(char *value) {
    struct expr *res = new_expr_ptr();
    res->t = T_STRING;
    unsigned int *x1 = malloc(sizeof(unsigned int) * (strlen(value) - 2));
    unsigned int *x = malloc(sizeof(unsigned int) * (strlen(value) - 2));
    int flag = -1;
    int num = 0;
    for (int i = 0; i < strlen(value) - 2; ++i) {
        x1[i] = (unsigned int) value[i + 1];
        if (flag == 1) {
            switch (value[i + 1]) {
                case 97://a
                    x[i - num - 1] = 7;
                    break;
                case 98://b
                    x[i - num - 1] = 8;
                    break;
                case 116://t
                    x[i - num - 1] = 9;
                    break;
                case 110://n
                    x[i - num - 1] = 10;
                    break;
                case 118://v
                    x[i - num - 1] = 11;
                    break;
                case 102://f
                    x[i - num - 1] = 12;
                    break;
                case 114://r
                    x[i - num - 1] = 13;
                    break;
                case 34://双引号
                    x[i - num - 1] = 34;
                    break;
                case 39://单引号
                    x[i - num - 1] = 39;
                    break;
                case 92://杠
                    x[i - num - 1] = 92;
                    break;
            }
//        if(value[i + 1] == 110) {
//          x[i - num - 1] = 10;
//          num++;
//        } else {
//          x[i - num - 1] = 92;
//        }
            num++;
            flag = 0;
        } else {
            if (value[i + 1] == 92) flag = 1;
            else {
                x[i - num] = (unsigned int) value[i + 1];
            }
        }
    }
    res->d.STRING.str = value + 1;
    res->d.STRING.value = x;
    res->d.STRING.value1 = x1;
    res->d.STRING.size = strlen(value) - 2 - num;
    free(value);
    return res;
}

struct expr *TVar(char *name) {
    struct expr *res = new_expr_ptr();
    res->t = T_VAR;
    res->d.VAR.name = name;
    return res;
}

struct expr *TArray(char *name, struct expr *num) {
    struct expr *res = new_expr_ptr();
    res->t = T_ARRAY;
    res->d.ARRAY.name = name;
    res->d.ARRAY.num = new_expr_ptr();
    res->d.ARRAY.num->d = num->d;
    res->d.ARRAY.num->t = num->t;
    return res;
}

struct expr *TBinOp(enum BinOpType op, struct expr *left, struct expr *right) {
    struct expr *res = new_expr_ptr();
    res->t = T_BINOP;
    res->d.BINOP.op = op;
    res->d.BINOP.left = left;
    res->d.BINOP.right = right;
    return res;
}

struct expr *TUnOp(enum UnOpType op, struct expr *arg) {
    struct expr *res = new_expr_ptr();
    res->t = T_UNOP;
    res->d.UNOP.op = op;
    res->d.UNOP.arg = arg;
    return res;
}

struct expr *TMalloc(struct expr *arg) {
    struct expr *res = new_expr_ptr();
    res->t = T_MALLOC;
    res->d.MALLOC.arg = arg;
    return res;
}

struct expr *TReadInt() {
    struct expr *res = new_expr_ptr();
    res->t = T_RI;
    return res;
}

struct expr *TReadChar() {
    struct expr *res = new_expr_ptr();
    res->t = T_RC;
    return res;
}

struct decl *TDecl(char *name) {
    struct decl *res = new_decl_ptr();
    res->t = T_DECL;
    res->d.DECL.name = name;
    return res;
}

struct decl *TDeclAndAsgn(char *name, struct expr *value) {
    struct decl *res = new_decl_ptr();
    res->t = T_DECLANDASGN;
    res->d.DECLANDASGN.name = name;
    res->d.DECLANDASGN.value = value;
    return res;
}

struct decl *TDecl_Array(char *name, unsigned int size) {
    struct decl *res = new_decl_ptr();
    res->t = T_DECL_ARRAY;
    res->d.DECL_ARRAY.name = name;
    res->d.DECL_ARRAY.size = size;
    return res;
}

struct decl *TDeclAndAsgn_Array(char *name, unsigned int size, struct expr_list *value) {
    struct decl *res = new_decl_ptr();
    res->t = T_DECLANDASGN_ARRAY;
    res->d.DECLANDASGN_ARRAY.name = name;
    res->d.DECLANDASGN_ARRAY.size = size;
    res->d.DECLANDASGN_ARRAY.value = value;
    return res;
}

struct decl *TDeclAndAsgn_String(char *name, struct expr *value) {//声明字符串（必须赋初值且以双引号标记时识别为字符串类型）
    struct decl *res = new_decl_ptr();
    res->t = T_DECLANDASGN_STRING;
    res->d.DECLANDASGN_STRING.name = name;
    res->d.DECLANDASGN_STRING.size = value->d.STRING.size;
    res->d.DECLANDASGN_STRING.value = value;
    return res;
}

struct cmd *TAsgn(struct expr *left, struct expr *right) {
    struct cmd *res = new_cmd_ptr();
    res->t = T_ASGN;
    res->d.ASGN.left = left;
    res->d.ASGN.right = right;
    return res;
}

struct cmd *TSeq(struct cmd *left, struct cmd *right) {
    struct cmd *res = new_cmd_ptr();
    res->t = T_SEQ;
    res->d.SEQ.left = left;
    res->d.SEQ.right = right;
    return res;
}

struct cmd *TIf(struct expr *cond, struct cmd *left, struct cmd *right) {
    struct cmd *res = new_cmd_ptr();
    res->t = T_IF;
    res->d.IF.cond = cond;
    res->d.IF.left = left;
    res->d.IF.right = right;
    return res;
}

struct cmd *TWhile(struct expr *cond, struct cmd *body) {
    struct cmd *res = new_cmd_ptr();
    res->t = T_WHILE;
    res->d.WHILE.cond = cond;
    res->d.WHILE.body = body;
    return res;
}

struct cmd *TWriteInt(struct expr *arg) {
    struct cmd *res = new_cmd_ptr();
    res->t = T_WI;
    res->d.WI.arg = arg;
    return res;
}

struct cmd *TWriteChar(struct expr *arg) {
    struct cmd *res = new_cmd_ptr();
    res->t = T_WC;
    res->d.WC.arg = arg;
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

void print_expr(struct expr *e) {
    switch (e->t) {
        case T_CONST:
            printf("CONST(%d)", e->d.CONST.value);
            break;
        case T_CHAR:
            printf("CHAR(%c", e->d.CHAR.value);
            printf(",%d)", e->d.CHAR.value);
            break;
        case T_STRING:
            printf("STRING(%ls,", e->d.STRING.value1);
            for (int i = 0; i < e->d.STRING.size; ++i) {
                if (i == e->d.STRING.size - 1) {
                    printf("%d)", e->d.STRING.value[i]);
                    break;
                }
                printf("%d,", e->d.STRING.value[i]);
            }
            break;
        case T_VAR:
            printf("VAR(%s)", e->d.VAR.name);
            break;
        case T_ARRAY:
            printf("ARRAY(%s,", e->d.ARRAY.name);
            print_expr(e->d.ARRAY.num);
            printf(")");
            break;
        case T_BINOP:
            print_binop(e->d.BINOP.op);
            printf("(");
            print_expr(e->d.BINOP.left);
            printf(",");
            print_expr(e->d.BINOP.right);
            printf(")");
            break;
        case T_UNOP:
            print_unop(e->d.UNOP.op);
            printf("(");
            print_expr(e->d.UNOP.arg);
            printf(")");
            break;
        case T_MALLOC:
            printf("MALLOC(");
            print_expr(e->d.MALLOC.arg);
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

void print_expr_list(struct expr_list *es) {
    if (es == NULL) {
        return;
    }
    printf(",");
    print_expr(es->data);
    print_expr_list(es->next);
}

void print_cmd(struct cmd *c) {
    switch (c->t) {
        case T_ASGN:
            printf("ASGN(");
            print_expr(c->d.ASGN.left);
            printf(",");
            print_expr(c->d.ASGN.right);
            printf(")");
            break;
        case T_SEQ:
            printf("SEQ(");
            print_cmd(c->d.SEQ.left);
            printf(",");
            print_cmd(c->d.SEQ.right);
            printf(")");
            break;
        case T_IF:
            printf("IF(");
            print_expr(c->d.IF.cond);
            printf(",");
            print_cmd(c->d.IF.left);
            printf(",");
            print_cmd(c->d.IF.right);
            printf(")");
            break;
        case T_WHILE:
            printf("WHILE(");
            print_expr(c->d.WHILE.cond);
            printf(",");
            print_cmd(c->d.WHILE.body);
            printf(")");
            break;
        case T_WI:
            printf("WRITE_INT(");
            print_expr(c->d.WI.arg);
            printf(")");
            break;
        case T_WC:
            printf("WRITE_CHAR(");
            print_expr(c->d.WC.arg);
            printf(")");
            break;
        case T_DECL_STH:
            print_decl_list(c->d.DECL_STH.decl_sth);
            break;
    }
}

void print_decl(struct decl *d) {
    switch (d->t) {
        case T_DECL:
            printf("DECL(%s)", d->d.DECL.name);
            break;
        case T_DECLANDASGN:
            printf("DECLANDASGN(%s,", d->d.DECLANDASGN.name);
            print_expr(d->d.DECLANDASGN.value);
            printf(")");
            break;
        case T_DECL_ARRAY:
            printf("DECL_ARRAY(%s,%d)", d->d.DECL_ARRAY.name, d->d.DECL_ARRAY.size);
            break;
        case T_DECLANDASGN_ARRAY:
            printf("DECLANDASGN_ARRAY(%s,%d", d->d.DECLANDASGN_ARRAY.name, d->d.DECLANDASGN_ARRAY.size);
            print_expr_list(d->d.DECLANDASGN_ARRAY.value);
            printf(")");
            break;
        case T_DECLANDASGN_STRING:
            printf("DECLANDASGN_STRING(%s,%d,", d->d.DECLANDASGN_STRING.name, d->d.DECLANDASGN_STRING.size);
            print_expr(d->d.DECLANDASGN_STRING.value);
            printf(")");
            break;
        default:
            break;
    }
}

void print_decl_list(struct decl_list *ds) {
    print_decl(ds->data);
    if (ds->next == NULL) {
        return;
    } else {
        printf(",");
        print_decl_list(ds->next);
    }
}