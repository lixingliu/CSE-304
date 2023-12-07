import decaf_ast as ast
import sys
built_in_types = ["int", "float", "boolean", "string", "void", "error", "null", "class-literal"]

# combine type is for binary operation when combing values
def combine_type(leftType, rightType, binaryType):
    arithmeticOperations = ["+", "-", "*", "/"]
    booleanOperations = ["||", "&&"]
    arithmeticComparisons = [">", ">=", "<", "<="]
    equalityComparisons = ["==", "!="]
    # doing add, sub, mul, div: left and right must be of type float or int
    if binaryType in arithmeticOperations:
        #if the left is not a float or an int, then its an error
        if (leftType != "int" and leftType != 'float'):
            return "error"
        # if the right is not a float or an int, then it is an error
        if (rightType != "int" and rightType != "float"):
            return "error"
        # if the left and right is an int, then the result is int
        if (leftType == "int" and rightType == "int"):
            return "int"
        # evey other combination is a float
        else:
            return "float"
    # doing and, or
    elif binaryType in booleanOperations:
        #if the left and the right is a boolean, then the result is a boolean
        if (leftType == "boolean" and rightType == "boolean"):
            return "boolean"
        # everything else is false
        else:
            return "error"
    # doing >, >=, <, <=
    elif binaryType in arithmeticComparisons:
        # the result is boolean
        # the left has to be either a int or a float else error
        if (leftType != "int" and leftType != "float"):
            return "error"
        # the right has to be either a int or a float else error
        if (rightType != "int" and rightType != "float"):
            return "error"
        # everything else is a boolean
        else:
            return "boolean"
    # doing == and !=
    elif binaryType in equalityComparisons:
        #to do subtype
        pass
    return 'error'
     
def get_this_type(fieldDictionary, id):
    for key, value in fieldDictionary.items():
        if (id == value["variableName"]):
            return(value["type"])

def get_super_type(currentClassDirectory, globalClassRecord, id):
    superClassName = currentClassDirectory["superClassName"]
    if superClassName == "":
        print("Error: Super class does not exist")
        sys.exit()
    classObject = globalClassRecord[superClassName]
    classField = classObject['fields']
    for key, value in classField.items():
        if (id == value["variableName"]):
            return(value["type"])

def get_type(variableTable, id):
    for table in variableTable[::-1]:
        for key, value in table.items():
            if id == value["variableName"]:
                return value["variableType"]

    if (isinstance(id, int)):
        return "int"
    if (isinstance(id, float)):
        return 'float'
    if (id == "true"):
        return "boolean"
    if (id == "false"):
        return "boolean"
    if (isinstance(id, str)):
        return "string"
    
def get_object_type(variableTable, id):
    for table in variableTable[::-1]:
        for key, value in table.items():
            if (value["variableName"] == id):
               return(value["variableType"])    

def get_method_invocation_type(fieldAccess):
    if (isinstance(fieldAccess, ast.ID)):
        for key, value in ast.CURRENT_CLASS_DICTIONARY["methods"].items():
            if (value["methodName"] == fieldAccess.id):
                return(value['type'])

    if (isinstance(fieldAccess, ast.Field_Access)):
        if (fieldAccess.primary == "this"):
            classObject = ast.CURRENT_CLASS_DICTIONARY
            for key, value in classObject["methods"].items():
                if (value["methodName"] == fieldAccess.id):
                    return(value['type'])
                
        if (fieldAccess.primary == 'super'):
            superClassName = ast.CURRENT_CLASS_DICTIONARY["superClassName"]
            if superClassName == "":
                print("Error: Super class does not exist")
                sys.exit()
            classObject = ast.GLOBAL_CLASS_RECORD[superClassName]
            classField = classObject['methods']
            for key, value in classField.items():
                if (fieldAccess.id == value["methodName"]):
                    return(value['type'])
                
        if (isinstance(fieldAccess.primary, ast.ID)):
            className = get_type(ast.VARIABLE_TABLE, fieldAccess.primary.id)
            classObject = ast.GLOBAL_CLASS_RECORD[className]
            classField = classObject['methods']
            for key, value in classField.items():
                if (fieldAccess.id == value["methodName"]):
                    return(value['type'])
            return "aaa"

def get_lhs_type(lhs):
    if (isinstance(lhs, ast.ID)):
        return(get_type(ast.VARIABLE_TABLE, lhs.id))
    if (isinstance(lhs, ast.Field_Access)):
        if (lhs.primary == 'this'):
            return(get_this_type(ast.FIELD_DICTIONARY, lhs.id))
        if (lhs.primary == "super"):
            return(get_super_type(ast.CURRENT_CLASS_DICTIONARY, ast.GLOBAL_CLASS_RECORD, lhs.id))
        if (isinstance(lhs.primary, ast.ID)):
            className = get_type(ast.VARIABLE_TABLE, lhs.primary.id)
            classObject = ast.GLOBAL_CLASS_RECORD[className]
            classField = classObject['fields']
            for key, value in classField.items():
                if (lhs.id == value["variableName"]):
                    return(value['type'])
                
def get_auto_type(lhs):
    auto_type = get_lhs_type(lhs)
    if (auto_type != "int" and auto_type != "float"):
        print("Error: auto-expression has to have either type float or int")
        sys.exit()
    return(auto_type)

def find_expr_type(expr):
    if (isinstance(expr, ast.ID)):
        return(get_type(ast.VARIABLE_TABLE, expr.id))
    if (isinstance(expr, ast.Literal)):
        return(get_type([], expr.literal))
    if (isinstance(expr, ast.Field_Access)):
        if (expr.primary == 'this'):
            return(get_this_type(ast.FIELD_DICTIONARY, expr.id))
        if (expr.primary == 'super'):
            return(get_super_type(ast.CURRENT_CLASS_DICTIONARY, ast.GLOBAL_CLASS_RECORD, expr.id))
        if (isinstance(expr.primary, ast.ID)):
            className = get_type(ast.VARIABLE_TABLE, expr.primary.id)
            classObject = ast.GLOBAL_CLASS_RECORD[className]
            for key, value in classObject['fields'].items():
                if (expr.id == value["variableName"]):
                    return(value['type'])
    if (isinstance(expr, ast.Paren)):
        return(find_expr_type(expr.expr))
    if (isinstance(expr, ast.New)):
        return "NEW"    #todo
    if (isinstance(expr, ast.Method_Invocation)):
        return(get_method_invocation_type(expr.fieldAccess))
    if (isinstance(expr, ast.Assign)):
        return get_assign_type(expr)
    if (isinstance(expr, ast.Auto)):
        return(get_auto_type(expr.lhs))
    if (isinstance(expr, ast.Binary_Expr)):
        return(get_binary_type(expr))
    if (isinstance(expr, ast.Not)):
        result = get_neg_type(expr.expr)
        if (result != "boolean"):
            print("Error: Negation has to be boolean")
            sys.exit()
        return result
    if (isinstance(expr, ast.Uminus)):
        result = get_uminus_type(expr.expr)
        if (result != "int" and result != "float"):
            print("Error: Uminus has to be either a float or int")
            sys.exit()
        return result
    if (isinstance(expr, ast.Uplus)):
        result = get_uminus_type(expr.expr)
        if (result != "int" and result != "float"):
            print("Error: Uminus has to be either a float or int")
            sys.exit()
        return result
    
def get_paren_type(expr):
    return(find_expr_type(expr))

def get_neg_type(expr):
    return(find_expr_type(expr))

def get_uminus_type(expr):
    return(find_expr_type(expr))
    
def get_uplus_type(expr):
    return(find_expr_type(expr))

def get_binary_type(expr):
    leftExprType = None
    rightExprType = None
    leftExprType = find_expr_type(expr.leftExpr)
    rightExprType = find_expr_type(expr.rightExpr)
    result = combine_type(leftExprType, rightExprType, expr.binaryType)
    if (result == "error"):
        print("Invalid binary expression")
        sys.exit()
    else:
        return result
    
def get_assign_type(expr):
    lhs_type = get_lhs_type(expr.lhs)
    expr_type = find_expr_type(expr.expr)
    #todo check type correct
    return lhs_type

def get_stmt_type(stmt):
    if (isinstance(stmt, ast.If_decl)):
        expr_type = find_expr_type(stmt.expr)
        if (expr_type != "boolean"):
            print("Error: If condition has to be type boolean")
            sys.exit()
        stmt_one_type = get_stmt_type(stmt.stmtOne)
        stmt_two_type = get_stmt_type(stmt.stmtTwo)
        print("231", stmt_one_type)
        print("232", stmt_two_type)
        if (stmt_one_type == "correct" and stmt_two_type == "correct"):
            return "correct"
        else:
            print("Error: invalid stmt")

    if (isinstance(stmt, ast.While_decl)):
        expr_type = find_expr_type(stmt.expr)
        if (expr_type != "boolean"):
            print("Error: While condition has to be type boolean")
        stmt_type = get_stmt_type(stmt.stmt)
        print("238", expr_type)
        print("237", stmt_type)
        if(stmt_type == "correct"):
            return "correct"
        else:
            print("Error: invalid stmt")

    if (isinstance(stmt, ast.For_decl)):
        for_cond_1_type = get_stmt_expr_type(stmt.cond1)
        if (for_cond_1_type != "correct"):
            print("Type error in initializer")
            
        print("252", for_cond_1_type)
        for_cond_2_type = find_expr_type(stmt.cond2)
        print("253", for_cond_2_type)
        for_cond_3_type = get_stmt_expr_type(stmt.cond3)
        print("254", for_cond_3_type)
        for_body_type = ""
        if (for_cond_1_type == "correct" and for_cond_2_type == "boolean" and for_cond_3_type == "correct" and for_body_type == "correct"):
            return "correct"
        else:
            print("Error, for ")
    if (isinstance(stmt, ast.Block)):
        result = check_block_type_correct(stmt.stmtList.stmts)
        print("226", result)
    if (stmt == "continue"):
        return "correct"
    if (stmt == "break"):
        return "correct"
    if (stmt == ';'):
        return "correct"
    if (stmt is None):
        return 'correct'
    
def get_stmt_expr_type(stmtExpr):
    if (isinstance(stmtExpr, ast.Assign)):
        result = get_assign_type(stmtExpr)
        if (result):
            return "correct"
    if (isinstance(stmtExpr, ast.Auto)):
        result = get_auto_type(stmtExpr.lhs)
        if (result):
            return "correct"
    if (isinstance(stmtExpr, ast.Method_Invocation)):
        result = get_method_invocation_type(stmtExpr.fieldAccess)   #todo double check this
        if (result):
            return "correct"
def check_block_type_correct(stmts):
    for stmt in stmts:
        result = get_stmt_type(stmt)
        if (result != "correct"):
            print("ErrorErrorError")
            sys.exit()
def check_subtype(lhs, rhs):
    print("\nEnter check subtype")
    print(lhs)
    print(rhs)
    return "leave check subtype\n"