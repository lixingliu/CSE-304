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
    p[0] = Program(p[1])
    return True
     
def p_class_decl_list(p):
    '''class_decl_list : class_decl class_decl_list
                    | empty'''
    if len(p) == 2:
        p[0] = Class_decl_list()
    else:
        p[2].classList.append(p[1])
        p[0] = p[2] 

def p_class_decl(p):
    '''class_decl : CLASS ID EXTENDS ID '{' class_body_decl '}'
                | CLASS ID '{' class_body_decl '}' '''
    if len(p) == 6:
        p[0] = Class_decl(className=p[2], classBody=p[4])
    else:
        p[0] = Class_decl(className=p[2], superClassName=p[4], classBody=p[6])
    
def p_class_body_decl(p):
    '''class_body_decl : field_decl
                        | method_decl
                        | constructor_decl
                        | class_body_decl field_decl
                        | class_body_decl method_decl
                        | class_body_decl constructor_decl'''
    if len(p) == 2:
        p[0] = Class_Body_List(p[1])
    else:
        p[1].classBodyItems.append(p[2])
        p[0] = p[1]

def p_field_decl(p):
    '''field_decl : modifier var_decl'''
    p[0] = Field_Decl(p[1], p[2])
    
def p_modifier(p):
    '''modifier : PUBLIC STATIC
            | PRIVATE STATIC
            | PUBLIC
            | PRIVATE
            | STATIC
            | empty'''
    if len(p) == 2:
        p[0] = Modifier(p[1])
    else:
        p[0] = Modifier(p[1], p[2])
  
def p_var_decl(p):
    '''var_decl : type variables ';' '''
    p[0] = Var_Decl(p[1], p[2])

def p_type(p):
    '''type : INT
        | FLOAT
        | BOOLEAN
        | ID'''
    p[0] = str(p[1])

def p_variables(p):
    '''variables : variable variables_cont'''
    p[2].vars.append(p[1])
    p[0] = p[2]

def p_variables_cont(p):
    '''variables_cont : ',' variable variables_cont
		                | empty'''
    if len(p) == 2:
        p[0] = Variables_cont()
    else:
        p[3].vars.append(p[2])
        p[0] = p[3]

def p_variable(p):
    '''variable : ID'''
    p[0] = str(p[1])
            
def p_method_decl(p):
    '''method_decl : modifier type ID LEFTPAREN formals RIGHTPAREN block
				| modifier VOID ID LEFTPAREN formals RIGHTPAREN block'''
    p[0] = Method_Decl(p[1], p[2], p[3], p[5], p[7])

def p_constructor_decl(p):
    '''constructor_decl : modifier ID LEFTPAREN formals RIGHTPAREN block'''
    p[0] = Constructor_Decl(p[1], p[2], p[4], p[6])

def p_formals(p):
    '''formals : formal_param formals_cont
            | empty'''
    if len(p) == 2:
        p[0] = Formals_const()
    else:
        p[2].formals.append(p[1])
        p[0] = p[2]

def p_formals_cont(p):
    '''formals_cont : ',' formal_param formals_cont
            | empty'''
    if len(p) == 2:
        p[0] = Formals_const()
    else:
        p[3].formals.append(p[2])
        p[0] = p[3]

def p_formal_param(p):
    '''formal_param : type variable'''
    p[0] = Formal_param(p[1], p[2])

def p_block(p):
    '''block : '{' stmt_list '}' '''
    p[0] = Block(p[2], p.lineno(2))

def p_stmt_list(p):
    ''' stmt_list : stmt stmt_list
                | empty'''
    if len(p) == 2:
        p[0] = Stmt_List() 
    else:
        p[2].stmts.append(p[1])
        p[0] = p[2]

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
    if len(p) == 6 and p[1] == 'if':
        p[0] = If_decl(p[3], p[5], None, p.lineno(2))
    elif len(p) == 8 and p[1] == 'if':
        p[0] = If_decl(p[3], p[5], p[7], p.lineno(2))
    elif len(p) == 6 and p[1] == 'while':
        p[0] = While_decl(p[3], p[5], p.lineno(2))
    elif len(p) == 10 and p[1] == 'for':
      p[0] = For_decl(p[3], p[5], p[7], p[9], p.lineno(2))
    elif len(p) == 4 and p[1] == 'return':
        p[0] = Return(p[2], p.lineno(2))
    elif len(p) == 3 and p[1] == 'break':
       p[0] = p[1]
    elif len(p) == 3 and p[1] == 'continue':
        p[0] = p[1]
    else:
        p[0] = p[1]


def p_for_cond_1(p):
    '''for_cond_1 : stmt_expr
                | empty'''
    p[0] = p[1]

def p_for_cond_2(p):
    '''for_cond_2 : expr
                | empty'''
    p[0] = p[1]

def p_for_cond_3(p):
    '''for_cond_3 : stmt_expr
                | empty'''
    p[0] = p[1]

def p_return_val(p):
    '''return_val : expr
                | empty'''
    p[0] = p[1]

def p_literal(p):
    '''literal : INT_CONST
                | FLOAT_CONST
                | STRING_CONST
                | NULL
                | TRUE
                | FALSE''' 
    # p[0] = str(Literal(p[1]))
    p[0] = (Literal(p[1]))

def p_primary(p):
    '''primary : literal
                | THIS
                | SUPER
                | LEFTPAREN expr RIGHTPAREN 
                | NEW ID LEFTPAREN arguments RIGHTPAREN
                | lhs
                | method_invocation '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4 and p[1] == '(':
        p[0] = Paren(p[2])
    elif len(p) == 6:
        p[0] = New(ID(p[2]), p[4])

def p_arguments(p):
    ''' arguments : expr arguments_cont
            | empty '''
    if len(p) == 2:
        p[0] = Arguments_cont()
    else:
        p[2].args.append((p[1]))
        p[0] = p[2]

def p_arguments_cont(p):
    ''' arguments_cont : ',' expr arguments_cont 
                    | empty '''
    if len(p) == 2:
        p[0] = Arguments_cont()
    else:
        p[3].args.append(p[2])
        p[0] = p[3]

def p_lhs(p):
    '''lhs : field_access'''
    p[0] = p[1]  

def p_field_access(p):
    '''field_access : primary '.' ID
                    | ID'''
    if len(p) == 2:
        p[0] = ID(p[1])
    else:
        p[0] = Field_Access(p[1], p[3])
    
def p_method_invocation(p):
    ''' method_invocation : field_access LEFTPAREN arguments RIGHTPAREN '''
    p[0] = Method_Invocation(p[1], p[3], p.lineno(2))

def p_expr(p):
    '''expr : primary
            | assign'''
    p[0] = p[1]

def p_assign(p):
    '''assign : lhs '=' expr
                | lhs INCREMENT
                | INCREMENT lhs 
                | lhs DECREMENT
                | DECREMENT lhs'''
    if(len(p) == 4):
        p[0] = Assign(p.lineno(2), p[1], p[3], )
    if(len(p) == 3):
        if(p[2] == '++' or p[2] == '--'):
            p[0] = Auto(p[2], None, p[1])
        if(p[1] == '--' or p[1] == "++"):
            p[0] = Auto(None, p[1], p[2])

def p_add_expr(p):
    '''expr : expr PLUS expr'''
    p[0] = Binary_Expr(p[1], p[3], p[2])

def p_sub_expr(p):
    '''expr : expr MINUS expr'''
    p[0] = Binary_Expr(p[1], p[3], p[2])

def p_mult_expr(p):
    '''expr : expr MULTIPLY expr'''
    p[0] = Binary_Expr(p[1], p[3], p[2])

def p_div_expr(p):
    '''expr : expr DIVIDE expr '''
    p[0] = Binary_Expr(p[1], p[3], p[2])

def p_conj_expr(p):
    '''expr : expr BOOL_AND expr'''
    p[0] = Binary_Expr(p[1], p[3], p[2])

def p_disj_expr(p):
    '''expr : expr BOOL_OR expr'''
    p[0] = Binary_Expr(p[1], p[3], p[2])

def p_equals_expr(p):
    '''expr : expr EQUALITY expr'''
    p[0] = Binary_Expr(p[1], p[3], p[2])

def p_notequals_expr(p):
    '''expr : expr DISQUALITY expr'''
    p[0] = Binary_Expr(p[1], p[3], p[2])

def p_lt_expr(p):
    '''expr : expr LESSTHAN expr'''
    p[0] = Binary_Expr(p[1], p[3], p[2])

def p_lte_expr(p):
    '''expr : expr LEQ expr'''
    p[0] = Binary_Expr(p[1], p[3], p[2])

def p_gt_expr(p):
    '''expr : expr GREATERTHAN expr'''
    p[0] = Binary_Expr(p[1], p[3], p[2])

def p_gte_expr(p):
    '''expr : expr GEQ expr'''
    p[0] = Binary_Expr(p[1], p[3], p[2])

def p_pos_expr(p):
    '''expr : PLUS expr %prec UPLUS'''
    p[0] = Uplus(p.lineno(2), p[1], p[2])

def p_minus_expr(p):
    '''expr : MINUS expr %prec UMINUS'''
    p[0] = Uminus(p[1], p[2])

def p_not_expr(p):
    '''expr : NOT expr'''
    p[0] = Not(p[2], p.lineno(2))

def p_stmt_expr(p):
    '''stmt_expr : assign
                | method_invocation'''
    p[0] = p[1]
    
def p_empty(p):
    '''empty :'''

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
    
				


                

