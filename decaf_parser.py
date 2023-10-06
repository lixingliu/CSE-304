import sys
from decaf_lexer import *
# program ::= class_decl* 
# this means that the program consists of zero or more classes

precedence = (
    ('right', '='),
    ('left', 'BOOL_OR'),
    ('left', 'BOOL_AND'),
    ('nonassoc', 'EQUALITY', 'DISQUALITY'),
    ('nonassoc', 'GREATERTHAN', 'LESSTHAN', 'LEQ', 'GEQ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE'),
    ('right', 'NOT', 'UMINUS', "UPLUS")
)

def p_program(p):
    '''program : stress
        
        stress : class_decl stress
                | empty'''
    
def p_class_decl(p):
    '''class_decl : CLASS ID EXTENDS ID '{' class_body_decl '}'
                | CLASS ID '{' class_body_decl '}' '''
    
def p_class_body_decl(p):
    '''class_body_decl : field_decl
                        | method_decl
                        | constructor_decl
                        | class_body_decl field_decl
                        | class_body_decl method_decl
                        | class_body_decl constructor_decl'''

def p_field_decl(p):
    '''field_decl : modifier var_decl
    
    modifier : PUBLIC STATIC
            | PUBLIC
            | PRIVATE STATIC
            | PRIVATE
            | STATIC
            | empty
            
    var_decl : type variables ';' '''
def p_type(p):
    '''type : INT
        | FLOAT
        | BOOLEAN
        | ID'''

def p_variables(p):
    '''variables : variable temp_3
    	
    temp_3 : ',' variable temp_3
		| empty
        
    variable : ID'''
            
def p_method_decl(p):
    '''method_decl : modifier type ID LEFTPAREN formals RIGHTPAREN block
				| modifier VOID ID LEFTPAREN formals RIGHTPAREN block
     
    constructor_decl : modifier ID LEFTPAREN formals RIGHTPAREN block
            
    formals : formal_param temp_6
            | empty
            
    temp_6 : ',' formal_param temp_6
            | empty
            
            
    formal_param : type variable'''

def p_block(p):
	'''block : '{' temp_7 '}'
	
    temp_7 : stmt temp_7
		| empty
        
    stmt : open_stmt
		| close_stmt
        
    open_stmt : IF LEFTPAREN expr RIGHTPAREN stmt
			| IF LEFTPAREN expr RIGHTPAREN close_stmt ELSE open_stmt
            | WHILE LEFTPAREN expr RIGHTPAREN open_stmt
            | FOR LEFTPAREN temp_8 ';' temp_9 ';' temp_8 RIGHTPAREN open_stmt
    close_stmt : RETURN temp_9 ';'
			| stmt_expr ';'
            | BREAK ';'
            | CONTINUE ';'
            | var_decl
            | ';'
            | block
			| IF LEFTPAREN expr RIGHTPAREN close_stmt ELSE close_stmt
            | WHILE LEFTPAREN expr RIGHTPAREN close_stmt
            | FOR LEFTPAREN temp_8 ';' temp_9 ';' temp_8 RIGHTPAREN close_stmt
    temp_8 : stmt_expr
		| empty
        
    temp_9 : expr
		| empty
    
	stmt_expr : assign
		| method_invocation  
	'''

def p_literal(p):
    '''literal : INT_CONST
                | FLOAT_CONST
                | STRING_CONST
                | NULL
                | TRUE
                | FALSE'''
    
def p_primary(p):
    '''primary : literal
                | THIS
                | SUPER
                | LEFTPAREN expr RIGHTPAREN 
                | NEW ID LEFTPAREN test_1 RIGHTPAREN
                | lhs
                | method_invocation
                 
        test_1 : expr test_2
                | empty
                 
        test_2 : ',' expr test_2 
                | empty

                
        lhs : field_access
        
        field_access : primary '.' ID
                | ID
                        
        method_invocation : field_access LEFTPAREN test_1 RIGHTPAREN '''


def p_expr(p):
    '''expr : primary
                | assign
                | arith_op
                | bool_op 
                | unary_op
        
        assign : lhs '=' expr
                | lhs INCREMENT
                | INCREMENT lhs
                | lhs DECREMENT
                | DECREMENT lhs
                        
        arith_op : expr PLUS expr
                | expr MINUS expr
                | expr MULTIPLY expr
                | expr DIVIDE expr
        
        bool_op : expr BOOL_AND expr
                | expr BOOL_OR expr
                | expr EQUALITY expr
                | expr DISQUALITY expr
                | expr LESSTHAN expr
                | expr GREATERTHAN expr
                | expr LEQ expr
                | expr GEQ expr
        
        unary_op : PLUS expr %prec UPLUS
                | MINUS expr %prec UMINUS
                | NOT expr'''

def p_error(p):
    print()
    if p:
        if not hasattr(p.lexer, "lineStart"): 
            print("Syntax error at '%s' (%d, %d)" %
          		(p.value, p.lineno, p.lexpos))
            sys.exit()
        print("Syntax error at '%s' (%d, %d)" %
          (p.value, p.lineno, p.lexpos - p.lexer.lineStart))
        print("Syntax error at token,", p.type, ", line", p.lineno)
    else:
        print("Syntax error at EOF")
    print()
    sys.exit()
    
				

def p_empty(p):
    '''empty :'''
    pass
                

