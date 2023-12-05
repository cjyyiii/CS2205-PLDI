%{
	// this part is copied to the beginning of the parser 
	#include <stdio.h>
	#include "lang.h"
	#include "lexer.h"
	void yyerror(char *);
	int yylex(void);
        struct cmd * root;
%}

%union {
unsigned int n;
char * i;
struct expr * e;
struct expr_list * es;
struct cmd * c;
struct cmd_list * cs;
void * none;
}

// Terminals
%token <n> TM_NAT
%token <i> TM_IDENT TM_CHAR TM_STRING
%token <none> TM_LEFT_BRACE TM_RIGHT_BRACE
%token <none> TM_LEFT_BRACKET TM_RIGHT_BRACKET
%token <none> TM_LEFT_PAREN TM_RIGHT_PAREN
%token <none> TM_SEMICOL TM_COMMA
%token <none> TM_MALLOC TM_RI TM_RC TM_WI TM_WC
%token <none> TM_VAR TM_ARRAY TM_IF TM_THEN TM_ELSE TM_WHILE TM_DO
%token <none> TM_ASGNOP
%token <none> TM_OR
%token <none> TM_AND
%token <none> TM_NOT
%token <none> TM_LT TM_LE TM_GT TM_GE TM_EQ TM_NE
%token <none> TM_PLUS TM_MINUS
%token <none> TM_MUL TM_DIV TM_MOD

// Nonterminals
%type <c> NT_WHOLE
%type <c> NT_CMD
%type <e> NT_EXPR_2
%type <e> NT_EXPR
%type <es> NT_EXPR_LIST
%type <cs> NT_DECL_VAR
%type <cs> NT_DECL_ARRAY
%type <cs> NT_DECL_LIST_VAR
%type <cs> NT_DECL_LIST_ARRAY

// Priority
%nonassoc TM_ASGNOP
%left TM_OR
%left TM_AND
%left TM_LT TM_LE TM_GT TM_GE TM_EQ TM_NE
%left TM_PLUS TM_MINUS
%left TM_MUL TM_DIV TM_MOD
%left TM_NOT
%left TM_LEFT_PAREN TM_RIGHT_PAREN
%left TM_LEFT_BRACKET TM_RIGHT_BRACKET
%right TM_SEMICOL

%%

NT_WHOLE:
  NT_CMD
  {
    $$ = ($1);
    root = $$;
  }
;

NT_CMD:
  TM_VAR NT_DECL_LIST_VAR
  {
    $$ = (TDeclList_Var($2));
  }
| TM_ARRAY NT_DECL_LIST_ARRAY
  {
    $$ = (TDeclList_Array($2));
  }
| NT_CMD TM_SEMICOL NT_CMD
  {
    $$ = (TSeq($1,$3));
  }
| TM_IF NT_EXPR TM_THEN TM_LEFT_BRACE NT_CMD TM_RIGHT_BRACE TM_ELSE TM_LEFT_BRACE NT_CMD TM_RIGHT_BRACE
  {
    $$ = (TIf($2,$5,$9));
  }
| TM_WHILE NT_EXPR TM_DO TM_LEFT_BRACE NT_CMD TM_RIGHT_BRACE
  {
    $$ = (TWhile($2,$5));
  }
| TM_WI TM_LEFT_PAREN NT_EXPR TM_RIGHT_PAREN
  {
    $$ = (TWriteInt($3));
  }
| TM_WC TM_LEFT_PAREN NT_EXPR TM_RIGHT_PAREN
  {
    $$ = (TWriteChar($3));
  }
;


NT_EXPR_2:
  TM_NAT
  {
    $$ = (TConst($1));
  }
| TM_LEFT_PAREN NT_EXPR TM_RIGHT_PAREN
  {
    $$ = ($2);
  }
| TM_IDENT TM_LEFT_BRACKET NT_EXPR TM_RIGHT_BRACKET
  {
  $$ = (TArray($1,$3));
  }
| TM_CHAR
  {
    $$ = (TChar($1));
  }
| TM_STRING
  {
    $$ = (TString($1));
  }
| TM_IDENT
  {
    $$ = (TVar($1));
  }
| TM_RI TM_LEFT_PAREN TM_RIGHT_PAREN
  {
    $$ = (TReadInt());
  }
| TM_RC TM_LEFT_PAREN TM_RIGHT_PAREN
  {
    $$ = (TReadChar());
  }
| TM_MALLOC TM_LEFT_PAREN NT_EXPR TM_RIGHT_PAREN
  {
    $$ = (TMalloc($3));
  }
| TM_NOT NT_EXPR_2
  {
    $$ = (TUnOp(T_NOT,$2));
  }
| TM_MINUS NT_EXPR_2
  {
    $$ = (TUnOp(T_UMINUS,$2));
  }
;

NT_EXPR:
  NT_EXPR_2
  {
    $$ = ($1);
  }
| NT_EXPR TM_MUL NT_EXPR
  {
    $$ = (TBinOp(T_MUL,$1,$3));
  }
| NT_EXPR TM_PLUS NT_EXPR
  {
    $$ = (TBinOp(T_PLUS,$1,$3));
  }
| NT_EXPR TM_MINUS NT_EXPR
  {
    $$ = (TBinOp(T_MINUS,$1,$3));
  }
| NT_EXPR TM_DIV NT_EXPR
  {
    $$ = (TBinOp(T_DIV,$1,$3));
  }
| NT_EXPR TM_MOD NT_EXPR
  {
    $$ = (TBinOp(T_MOD,$1,$3));
  }
| NT_EXPR TM_LT NT_EXPR
  {
    $$ = (TBinOp(T_LT,$1,$3));
  }
| NT_EXPR TM_GT NT_EXPR
  {
    $$ = (TBinOp(T_GT,$1,$3));
  }
| NT_EXPR TM_LE NT_EXPR
  {
    $$ = (TBinOp(T_LE,$1,$3));
  }
| NT_EXPR TM_GE NT_EXPR
  {
    $$ = (TBinOp(T_GE,$1,$3));
  }
| NT_EXPR TM_EQ NT_EXPR
  {
    $$ = (TBinOp(T_EQ,$1,$3));
  }
| NT_EXPR TM_NE NT_EXPR
  {
    $$ = (TBinOp(T_NE,$1,$3));
  }
| NT_EXPR TM_AND NT_EXPR
  {
    $$ = (TBinOp(T_AND,$1,$3));
  }
| NT_EXPR TM_OR NT_EXPR
  {
    $$ = (TBinOp(T_OR,$1,$3));
  }
;

NT_EXPR_LIST:
  NT_EXPR
  {
  $$ = (TECons($1,TENil()));
  }
| NT_EXPR TM_COMMA NT_EXPR_LIST
  {
  $$ = (TECons($1,$3));
  }
;

NT_DECL_VAR:
  TM_IDENT
  {
    $$ = (TDecl($1));
  }
|
  TM_IDENT TM_ASGNOP NT_EXPR
  {
    $$ = (TDeclAndAsgn($1,$3));
  }
;

NT_DECL_ARRAY:
  TM_IDENT TM_LEFT_BRACKET TM_NAT TM_RIGHT_BRACKET
  {
    $$ = (TDecl_Array($1,$3));
  }
|
  TM_IDENT TM_LEFT_BRACKET TM_NAT TM_RIGHT_BRACKET TM_ASGNOP TM_LEFT_BRACE NT_EXPR_LIST TM_RIGHT_BRACE
  {
    $$ = (TDeclAndAsgn_Array($1,$3,$7));
  }
| TM_IDENT TM_ASGNOP TM_STRING
  {
    $$ = (TDeclAndAsgn_String($1,$4));
  }
;

NT_DECL_LIST_VAR:
  NT_DECL_VAR
  {
  $$ = (TCCons($1,TCNil()));
  }
| NT_DECL_VAR TM_COMMA NT_DECL_LIST_VAR
  {
  $$ = (TCCons($1,$3));
  }
;

NT_DECL_LIST_ARRAY:
  NT_DECL_ARRAY
  {
  $$ = (TCCons($1,TCNil()));
  }
| NT_DECL_ARRAY TM_COMMA NT_DECL_LIST_ARRAY
  {
  $$ = (TCCons($1,$3));
  }
;

%%

void yyerror(char* s)
{
    fprintf(stderr , "%s\n",s);
}
