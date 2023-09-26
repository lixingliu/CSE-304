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
            
    variable : ID temp_4
    
    temp_4 : '[' ']' temp_4
        | empty'''
def p_method_decl(p):
    '''method_decl : modifier temp_5 ID '(' formals ')' block
     
    constructor_decl : modifier ID '(' formals ')' block

    temp_5 : type
            | VOID
            
    formals : empty
            | formal_param temp_6
            
    temp_6 : ',' formal_param temp_6
            | empty
            
    formal_param : type variable'''

def p_block(p):
    # '''block : '{' temp_7 '}' 
    # temp_7 : empty 
    #         | stmt temp_7
            
    # stmt : IF '(' expr ')' stmt
    #     | IF '(' expr ')'  stmt ELSE stmt
    #     | WHILE '(' expr ')' stmt
    #     '''
    

def p_empty(p):
    'empty :'
    pass
                

