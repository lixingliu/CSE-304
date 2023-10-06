import sys
from decaf_lexer import *
# program ::= class_decl* 
# this means that the program consists of zero or more classes
def p_program(p):
    '''program : class_decl program
                | empty'''
    
def p_class_decl(p):
    '''class_decl : CLASS ID '(' EXTENDS ID ')' '{' temp_1 '}'
                | CLASS ID '{' temp_1 '}' 
                
        temp_1 : class_body_decl temp_2
        
        temp_2 : class_body_decl temp_2
                | empty'''
    
def p_class_body_decl(p):
    '''class_body_decl : field_decl
                        | method_decl
                        | constructor_decl'''

def p_field_decl(p):
    '''field_decl : modifier var_decl
    
    modifier : PUBLIC STATIC
            | PUBLIC
            | PRIVATE STATIC
            | PRIVATE
            | STATIC
            | empty
            
    var_decl : type variables ';'
    
    type : INT
        | FLOAT
        | BOOLEAN
        | ID
        
    variables : variable temp_3
    
    temp_3 : ',' variable temp_3
            | empty
            
    variable : ID '''
    
def p_method_decl(p):
    '''method_decl : modifier temp_5 ID '(' formals ')' block
     
    constructor_decl : modifier ID '(' formals ')' block

    temp_5 : type
            | VOID
            
    formals : formal_param temp_6
            | empty
            
    temp_6 : ',' formal_param temp_6
            | empty
            
    formal_param : type variable'''

def p_block(p):
    '''block : '{' temp_7 '}' 
    temp_7 : stmt temp_7 
            | empty
            
    stmt : IF '(' expr ')' stmt
        | IF '(' expr ')'  stmt ELSE stmt
        | WHILE '(' expr ')' stmt
        | FOR '(' stmt_expr ';' expr ';' stmt_expr ')' stmt
        | FOR '(' ';' expr ';' stmt_expr ')' stmt
        | FOR '(' stmt_expr ';' expr ';' ')' stmt
        | FOR '(' stmt_expr ';' ';' stmt_expr ')' stmt
        | FOR '(' stmt_expr ';' ';' ')' stmt
        | FOR '(' ';' expr ';' ')' stmt
        | FOR '(' ';' ';' stmt_expr ')' stmt
        | RETURN expr ';'
        | RETURN ';'
        | stmt_expr ';'
        | BREAK ';'
        | CONTINUE ';'
        | block
        | var_decl
        | ';'
        '''

def expression(p):
    '''
    literal : INT_CONST
        | FLOAT_CONST
        | STRING_CONST
        | NULL
        | TRUE
        | FALSE

    primary : literal
        | THIS
        | SUPER
        | '(' expr ')'
        | NEW ID
        | lhs
        | method_invocation

    arguments : expr '(' commaexpr ')'

    commaexpr : , expr commaexpr
        |empty

    lhs : field_access

    field access : primary '.' ID
        | ID

    method_invocation : field_access
        | field_access '(' arguments ')'

    expr : primary
        | assign
        | expr arith_op expr
        | expr bool_op expr
        | unary_op expr

    assign : lhs '=' expr
        | lhs INCREMENT
        | INCREMENT lhs
        | lhs DECREMENT
        | DECREMENT lhs

    arith_op : '+'
        | '-'
        | '*'
        | '/'

    bool_op : BOOL_AND
        | BOOL_OR
        | EQUALITY
        | DISEQUALITY
        | '<' 
        | '>'
        | LEQ  
        | GEQ

    unary op : '+' 
        | '−' 
        | '!'

    stmt expr : assign
        | method_invocation
        '''
    
def p_empty(p):
    'empty :'
    pass
                

