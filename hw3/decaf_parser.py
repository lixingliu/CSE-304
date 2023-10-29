'''
Name: Li Xing Liu
Netid: lixiliu
Student Id: 113318331

Name: Andy You
Netid: Andyou
Student Id: 113494190
'''

import sys
from decaf_lexer import *
from decaf_ast import *
# program ::= class_decl* 
# this means that the program consists of zero or more classes

FIELD_COUNTER = 0
CONSTRUCTOR_COUNTER = 0
METHOD_COUNTER = 0
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
    '''program : class_decl_list'''
    p[0] = Program(p[1].things) #Starting with the program, we create a list of classes
    return True
     
def p_class_decl_list(p):
    '''class_decl_list : class_decl class_decl_list
                    | empty'''
    if len(p) == 2:
        p[0] = Class_decl_list() #if we dont have a class_decl to add, we create the list and return it up
    else:
        p[2].things.append(p[1])    #after getting the class_decl_list, we add the class to the list and send it up
        p[0] = p[2] 
    pass

def p_class_decl(p):
    '''class_decl : CLASS ID EXTENDS ID '{' class_body_decl '}'
                | CLASS ID '{' class_body_decl '}' '''
    if len(p) == 6:
        p[0] = Class_decl(p[2], "", p[4])
    else:
        p[0] = Class_decl(p[2], p[4], p[6])
    pass
    
def p_class_body_decl(p):
    '''class_body_decl : field_decl
                        | method_decl
                        | constructor_decl
                        | class_body_decl field_decl
                        | class_body_decl method_decl
                        | class_body_decl constructor_decl'''
    if len(p) == 3:
        p[1].things.append(p[2])
        p[0] = p[1]
    else:
        p[0] = Class_body_decl()
        p[0].things.append(p[1])

def p_field_decl(p):
    '''field_decl : modifier var_decl'''
    p[0] = Field_decl(p[1], p[2])
    pass

def p_modifier(p):
    '''modifier : PUBLIC STATIC
            | PRIVATE STATIC
            | PUBLIC
            | PRIVATE
            | STATIC
            | empty'''
    if len(p) == 3:
        p[0] = Modifier(p[1], p[2])
    elif len(p) == 2:
        if p[1] == None:
            p[0] = Modifier("private", "")
        else:
            p[0] = Modifier(p[1], "")
    pass

def p_var_decl(p):
    '''var_decl : type variables ';' '''
    p[0] = Var_decl(p[1], p[2])
    pass

def p_type(p):
    '''type : INT
        | FLOAT
        | BOOLEAN
        | ID'''
    p[0] = Type(p[1])
    pass

def p_variables(p):
    '''variables : variable variables_cont'''
    p[2].things.append(p[1])
    p[0] = Variables(p[2])
    pass

def p_variables_cont(p):
    '''variables_cont : ',' variable variables_cont
		                | empty'''
    if len(p) == 2:
        p[0] = Variables_cont()
    else:
        p[3].things.append(p[2])
        p[0] = p[3]
    pass

def p_variable(p):
    '''variable : ID'''
    p[0] = Variable(p[1])
    pass
            
def p_method_decl(p):
    '''method_decl : modifier type ID LEFTPAREN formals RIGHTPAREN block
				| modifier VOID ID LEFTPAREN formals RIGHTPAREN block'''
    p[0] = Method_decl(p[3], p[1], p[2], p[5], p[7])
    pass

def p_constructor_decl(p):
    '''constructor_decl : modifier ID LEFTPAREN formals RIGHTPAREN block'''
    p[0] = Constructor_decl(p[1], p[4], p[6])
    pass

def p_formals(p):
    '''formals : formal_param formals_cont
            | empty'''
    if len(p) == 2:
        p[0] = ""
    else:
        p[2].things.append(p[1])
        p[0] = Formals(p[2])
    pass

def p_formals_cont(p):
    '''formals_cont : ',' formal_param formals_cont
            | empty'''
    if len(p) == 2:
        p[0] = Formals_cont()
    else:
        p[3].things.append(p[2])
        p[0] = p[3]
    pass

def p_formal_param(p):
    '''formal_param : type variable'''
    p[0] = Formal_param(p[1], p[2])
    pass

def p_block(p):
    ''' block : stmt block
                | empty '''
    if len(p) == 2:
        p[0] = Block()
    else:
        p[2].things.append(p[1])
        p[0] = p[2]
    pass

def p_stmt(p):
    '''stmt : IF LEFTPAREN expr RIGHTPAREN stmt
            | IF LEFTPAREN expr RIGHTPAREN stmt ELSE stmt
            | WHILE LEFTPAREN expr RIGHTPAREN stmt 
            | FOR LEFTPAREN for_cond_1 ';' for_cond_2 ';' for_cond_3 RIGHTPAREN stmt
            | RETURN return_val ';'
            | stmt_expr ';'
            | BREAK ';'
            | CONTINUE ';'
            | block
            | var_decl
            | ';' '''
    if(p[1] == 'if' or p[1] == 'while'):
        if(len(p) == 6):
            p[0] = Ifelsewhile_stmt(p[1], p[3], [p[5], None])
        if(len(p) == 8):
            p[0] = Ifelsewhile_stmt(p[1], [p[3], p[5], p[7]])  
    if(p[1] == 'for' and len(p) == 10):
        p[0] = For_stmt([p[3], p[5], p[7], p[9]])
    if(p[1] == 'return' and len(p) == 4):
        p[0] = Stmt(p[1], [p[2]])
    if(p[1] == 'break' and len(p) == 3):
        p[0] = Stmt(p[1], [])
    if(p[1] == 'continue' and len(p) == 3):
        p[0] = Stmt(p[1], [])
    elif(len(p) == 3):
        p[0] = p[1]
    if(type(p[1]) == type(Block(None)) and len(p) == 2):
        p[0] = p[1]
    if(type(p[1]) == type(Var_decl(None)) and len(p) == 2):
        p[0] = p[1]
    if(p[1] == ';' and len(p) == 2):
        p[0] = Stmt('empty', [])
    pass

def p_for_cond_1(p):
    '''for_cond_1 : stmt_expr
                | empty'''
    p[0] = p[1]
    pass

def p_for_cond_2(p):
    '''for_cond_2 : expr
                | empty'''
    p[0] = p[1]
    pass

def p_for_cond_3(p):
    '''for_cond_3 : stmt_expr
                | empty'''
    p[0] = p[1]
    pass

def p_return_val(p):
    '''return_val : expr
                | empty'''
    p[0] = p[1]
    pass

def p_literal(p):
    '''literal : INT_CONST
                | FLOAT_CONST
                | STRING_CONST
                | NULL
                | TRUE
                | FALSE'''   
    pass
    
def p_primary(p):
    '''primary : literal
                | THIS
                | SUPER
                | LEFTPAREN expr RIGHTPAREN 
                | NEW ID LEFTPAREN arguments RIGHTPAREN
                | lhs
                | method_invocation '''
    pass

def p_arguments(p):
    ''' arguments : expr arguments_cont
            | empty '''
    pass

def p_arguments_cont(p):
    ''' arguments_cont : ',' expr arguments_cont 
                    | empty '''
    pass

def p_lhs(p):
    '''lhs : field_access'''  
    p[0] = p[1]       
    pass

def p_field_access(p):
    '''field_access : primary '.' ID
                    | ID'''
    if(len(p) == 2):
        p[0] = p[1]
    #Missing primary.ID
    pass

def p_method_invocation(p):
    ''' method_invocation : field_access LEFTPAREN arguments RIGHTPAREN '''
    pass

def p_expr(p):
    '''expr : primary
            | assign'''
pass

def p_assign(p):
    '''assign : lhs '=' expr
                | lhs INCREMENT
                | INCREMENT lhs 
                | lhs DECREMENT
                | DECREMENT lhs'''
    if(len(p) == 4):
        p[1] = p[3]
        p[0] = p[1]
    if(len(p) == 3):
        if(p[2] == r'\+\+'):
            p[0] = p[1]
            p[1] = p[1] + 1
        if(p[1] == r'\+\+'):
            p[1] = p[1] + 1
            p[0] = p[1]
        if(p[2] == r'--'):
            p[0] = p[1]
            p[1] = p[1] - 1
        if(p[1] == r'--'):
            p[1] = p[1] - 1
            p[0] = p[1]
    pass

def p_add_expr(p):
    '''expr : expr PLUS expr'''
    pass
def p_sub_expr(p):
    '''expr : expr MINUS expr'''
    pass

def p_mult_expr(p):
    '''expr : expr MULTIPLY expr'''
    pass

def p_div_expr(p):
    '''expr : expr DIVIDE expr '''
    pass

def p_conj_expr(p):
    '''expr : expr BOOL_AND expr'''
    pass

def p_disj_expr(p):
    '''expr : expr BOOL_OR expr'''
    pass

def p_equals_expr(p):
    '''expr : expr EQUALITY expr'''
    pass

def p_notequals_expr(p):
    '''expr : expr DISQUALITY expr'''
    pass

def p_lt_expr(p):
    '''expr : expr LESSTHAN expr'''
    pass

def p_lte_expr(p):
    '''expr : expr LEQ expr'''
    pass

def p_gt_expr(p):
    '''expr : expr GREATERTHAN expr'''
    pass

def p_gte_expr(p):
    '''expr : expr GEQ expr'''
    pass

def p_pos_expr(p):
    '''expr : PLUS expr %prec UPLUS'''
    pass

def p_minus_expr(p):
    '''expr : MINUS expr %prec UMINUS'''
    pass

def p_not_expr(p):
    '''expr : NOT expr'''
    pass
def p_stmt_expr(p):
    '''stmt_expr : assign
                | method_invocation'''
    p[0] = p[1]
    pass
    
def p_empty(p):
    '''empty :'''
    pass

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
    
				


                

