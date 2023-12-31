

import sys
from decaf_lexer import *

names = {}

precedence = (('right', 'ASSIGN'),
              ('left', 'OR'),
              ('left', 'AND'),
              ('nonassoc', 'EQ', 'NOT_EQ'),
              ('nonassoc', 'LT', 'LTE', 'GT', 'GTE'),
              ('left', 'PLUS', 'MINUS'),
              ('left', 'STAR', 'F_SLASH'),
              ('right', 'UMINUS', 'UPLUS', 'NOT')
              )

def p_program(p):
    'program : class_decl_list'
    return True

def p_class_decl_list(p):
    '''class_decl_list : class_decl class_decl_list
                       | empty'''
    pass

def p_class_decl(p):
    '''class_decl : CLASS ID LEFT_CB class_body_decl_list RIGHT_CB
                  | CLASS ID EXTENDS ID LEFT_CB class_body_decl_list  RIGHT_CB'''
    pass

def p_class_body_decl_list(p):
    'class_body_decl_list : class_body_decl class_body_decl_cont'
    pass

def p_class_body_decl_cont(p):
    '''class_body_decl_cont : class_body_decl class_body_decl_cont
                            | empty'''
    pass

def p_class_body_decl(p):
    '''class_body_decl : field_decl
                       | method_decl
                       | constructor_decl'''
    pass

def p_field_decl(p):
    'field_decl : modifier var_decl'
    pass

def p_modifier(p):
    '''modifier : PUBLIC STATIC
                | PRIVATE STATIC
                | PUBLIC
                | PRIVATE
                | STATIC
                | empty'''
    pass

def p_var_decl(p):
    'var_decl : type variables SEMI_COLON'
    pass

def p_type(p):
    '''type : TYPE_INT
            | TYPE_FLOAT
            | TYPE_BOOLEAN
            | ID'''
    pass

def p_variables(p):
    'variables : variable variables_cont'
    pass

def p_variables_cont(p):
    '''variables_cont : COMMA variable variables_cont
                      | empty'''
    pass

def p_variable(p):
    'variable : ID'
    pass

def p_method_decl(p):
    '''method_decl : modifier type ID LEFT_PN formals RIGHT_PN block
                   | modifier TYPE_VOID ID LEFT_PN formals RIGHT_PN block'''
    pass

def p_constructor_decl(p):
    'constructor_decl : modifier ID LEFT_PN formals RIGHT_PN block'
    pass

def p_formals(p):
    '''formals : formal_param formals_cont
               | empty'''
    pass

def p_formals_cont(p):
    '''formals_cont : COMMA formal_param formals_cont
                    | empty'''
    pass

def p_formal_param(p):
    'formal_param : type variable'
    pass

def p_block(p):
    'block : LEFT_CB stmt_list RIGHT_CB'
    pass

def p_stmt_list(p):
    '''stmt_list : stmt stmt_list
                 | empty'''
    pass

def p_stmt(p):
    '''stmt : IF LEFT_PN expr RIGHT_PN stmt 
            | IF LEFT_PN expr RIGHT_PN stmt ELSE stmt
            | WHILE LEFT_PN expr RIGHT_PN stmt
            | FOR LEFT_PN for_cond1 SEMI_COLON for_cond2 SEMI_COLON for_cond3 RIGHT_PN stmt
            | RETURN return_val SEMI_COLON
            | stmt_expr SEMI_COLON
            | BREAK SEMI_COLON
            | CONTINUE SEMI_COLON
            | block
            | var_decl
            | SEMI_COLON'''
    pass

def p_for_cond1(p):
    '''for_cond1 : stmt_expr
                 | empty'''
    pass

def p_for_cond2(p):
    '''for_cond2 : expr
                 | empty'''
    pass

def p_for_cond3(p):
    '''for_cond3 : stmt_expr
                 | empty'''
    pass

def p_return_val(p):
    '''return_val : expr
                  | empty'''
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
               | LEFT_PN expr RIGHT_PN
               | NEW ID LEFT_PN arguments RIGHT_PN
               | lhs
               | method_invocation'''
    pass

def p_arguments(p):
    '''arguments : expr arguments_cont
                 | empty'''
    pass

def p_arguments_cont(p):
    '''arguments_cont : COMMA expr arguments_cont
                      | empty'''
    pass

def p_lhs(p):
    'lhs : field_access'
    pass

def p_field_access(p):
    '''field_access : primary DOT ID
                    | ID'''
    pass

def p_method_invocation(p):
    'method_invocation : field_access LEFT_PN arguments RIGHT_PN'
    pass

def p_expr(p):
    '''expr : primary
            | assign'''
    pass
    
#def p_expr(p):
#   '''expr : primary
#            | assign
#            | expr arith_op expr
#            | expr bool_op expr
#            | unary_op expr'''
#    pass

def p_assign(p):
    '''assign : lhs ASSIGN expr
              | lhs INCREMENT
              | INCREMENT lhs
              | lhs DECREMENT
              | DECREMENT lhs'''
    pass

#def p_assign(p):
#    '''assign : lhs ASSIGN expr
#              | lhs PLUS PLUS
#              | PLUS PLUS lhs
#              | lhs MINUS MINUS
#              | MINUS MINUS lhs'''
#    pass

def p_add_expr(p):
    'expr : expr PLUS expr'
    pass

def p_sub_expr(p):
    'expr : expr MINUS expr'
    pass

def p_mult_exp(p):
    'expr : expr STAR expr'
    pass

def p_div_expr(p):
    'expr : expr F_SLASH expr'
    pass

def p_conj_expr(p):
    'expr : expr AND expr'
    pass

def p_disj_expr(p):
    'expr : expr OR expr'
    pass

def p_equals_expr(p):
    'expr : expr EQ expr'
    pass

def p_notequals_expr(p):
    'expr : expr NOT_EQ expr'
    pass

def p_lt_expr(p):
    'expr : expr LT expr'
    pass

def p_lte_expr(p):
    'expr : expr LTE expr'
    pass

def p_gt_expr(p):
    'expr : expr GT expr'
    pass

def p_gte_expr(p):
    'expr : expr GTE expr'
    pass

def p_pos_expr(p):
    'expr : PLUS expr %prec UPLUS'
    pass

def p_minus_expr(p):
    'expr : MINUS expr %prec UMINUS'
    pass

def p_not_expr(p):
    'expr : NOT expr'
    pass

#def p_arith_op(p):
#    '''arith_op : PLUS
#                | MINUS
#                | STAR
#                | F_SLASH'''
#    pass

#def p_bool_op(p):
#    '''bool_op : AND
#               | OR
#               | EQ
#               | NOT_EQ
#               | LT
#               | GT
#               | LTE
#               | GTE'''
#    pass

#def p_unary_op(p):
#    '''unary_op : PLUS
#                | MINUS
#                | NOT'''
#    pass

def p_stmt_expr(p):
    '''stmt_expr : assign
                 | method_invocation'''
    pass

def p_empty(p):
    'empty :'
    pass

def p_error(p):
    print()
    if p:
        print("Syntax error at token,", p.type, ", line", p.lineno)
    else:
        print("Syntax error at EOF")
    print()
    sys.exit()
