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
        return "boolean"
    # doing == and !=
    elif binaryType in equalityComparisons:
        result = check_subtype(rightType, leftType)
        if (result == False):
            return "error"
        else:
            return "boolean"
    return 'error'
     
def get_this_type(fieldDictionary, id):
    for key, value in fieldDictionary.items():
        if (id == value["variableName"]):
            return(value["type"])
    if (ast.CURRENT_CLASS_DICTIONARY["superClassName"] == ""):
        print("NON-STATIC FIELD ACCESS - No such field")
        sys.exit()
    fieldDictionary = (ast.GLOBAL_CLASS_RECORD[ast.CURRENT_CLASS_DICTIONARY["superClassName"]])["fields"]
    for key, value in fieldDictionary.items():
        if (id == value["variableName"]):
            return(value["type"])

def get_super_type(currentClassDirectory, globalClassRecord, id):
    superClassName = currentClassDirectory["superClassName"]
    if superClassName == "":
        print("SUPER EXPRESSION - No super class")
        sys.exit()
    classObject = globalClassRecord[superClassName]
    classField = classObject['fields']
    for key, value in classField.items():
        if (id == value["variableName"]):
            return(value["type"])

def get_type(variableTable, id):
    if (id == "null"):
        return "null"
    if (isinstance(id, int)):
        return "int"
    if (isinstance(id, float)):
        return 'float'
    if (id == "true"):
        return "boolean"
    if (id == "false"):
        return "boolean"
    if (id.startswith('"') and id.endswith('"')):
        return "string"
    for table in variableTable[::-1]:
        for key, value in table.items():
            if id == value["variableName"]:
                return value["variableType"]
    currentFieldDictionary = ast.CURRENT_CLASS_DICTIONARY["fields"]
    for key, value in currentFieldDictionary.items():
        if (id == value["variableName"]):
            return value["type"]

    if (ast.CURRENT_CLASS_DICTIONARY["superClassName"] == ""):
        print("NON-STATIC FIELD ACCESS - No such field")
        sys.exit()
    fieldDictionary = (ast.GLOBAL_CLASS_RECORD[ast.CURRENT_CLASS_DICTIONARY["superClassName"]])["fields"]
    for key, value in fieldDictionary.items():
        if (id == value["variableName"]):
            return(value["type"])
        

        

    
def get_object_type(variableTable, id):
    for table in variableTable[::-1]:
        for key, value in table.items():
            if (value["variableName"] == id):
               return(value["variableType"])    

def get_method_invocation_type(fieldAccess, arguments):
    if (isinstance(fieldAccess, ast.ID)):
        for key, value in ast.CURRENT_CLASS_DICTIONARY["methods"].items():
            if (value["methodName"] == fieldAccess.id):
                return(value['type'])

    if (isinstance(fieldAccess, ast.Field_Access)):
        if (fieldAccess.primary == "this"):
            classObject = ast.CURRENT_CLASS_DICTIONARY
            method = ""
            for key, value in classObject["methods"].items():
                if (value["methodName"] == fieldAccess.id):
                    method = value
                    break
            if (method == ""):
                if(classObject["superClassName"] != ""):
                    superClassMethods = ast.GLOBAL_CLASS_RECORD[classObject["superClassName"]]["methods"]
                    for key, value in superClassMethods.items():
                        if (fieldAccess.id == value["methodName"]):
                            method = value
                else:
                    print("NON-STATIC METHOD INVOCATION - No such method")
                    sys.exit()
            applicability = method['modifier'].applicability
            if applicability == "instance":
                applicability = "non-static"
            else:
                applicability = "static"
            if applicability == "static":
                print("NON-STATIC METHOD INVOCATION - No such method")
                sys.exit()

            list1 = []
            list2 = []
            for arg in arguments.args:
                list1.append(find_expr_type(arg))
            for formal in method["formals"].formals:
                list2.append(formal.type)
            for i in range(len(list1)):
                result = check_subtype(list1[i], list2[i])
                if (result == False):
                    print("NON-STATIC METHOD INVOCATION - Bad arguments")
                    sys.exit()
            return method["type"]



        if (fieldAccess.primary == 'super'):
            superClassName = ast.CURRENT_CLASS_DICTIONARY["superClassName"]
            if superClassName == "":
                print("SUPER EXPRESSION - No super class")
                sys.exit()
            classObject = ast.GLOBAL_CLASS_RECORD[superClassName]
            classField = classObject['methods']
            for key, value in classField.items():
                if (fieldAccess.id == value["methodName"]):
                    return(value['type'])
                
        if (isinstance(fieldAccess.primary, ast.ID)):
            status = False
            if (fieldAccess.primary.id in ast.GLOBAL_CLASS_RECORD.keys()):
                className = fieldAccess.primary.id
            else:
                status = True
                className = get_type(ast.VARIABLE_TABLE, fieldAccess.primary.id)
            classObject = ast.GLOBAL_CLASS_RECORD[className]
            classMethods = classObject['methods']
            method = None
            for key, value in classMethods.items():
                if (fieldAccess.id == value["methodName"]):
                    method = value
                    break
            if (method is None):
                if (classObject["superClassName"] != ""):
                    superClassMethods = ast.GLOBAL_CLASS_RECORD[classObject["superClassName"]]["methods"]
                    for key, value in superClassMethods.items():
                        if (fieldAccess.id == value["methodName"]):
                            method = value
                else:
                    print("STATIC METHOD INVOCATION - No such method")
                    sys.exit()
                
            if (status == True):
                list1 = []
                list2 = []
                for arg in arguments.args:
                    list1.append(find_expr_type(arg))
                for formal in method["formals"].formals:
                    list2.append(formal.type)
                for i in range(len(list1)):
                    result = check_subtype(list1[i], list2[i])
                    if (result == False):
                        print("STATIC METHOD INVOCATION - Bad arguments")
                        sys.exit()
                if (isinstance(method["type"], ast.Type)):
                    return method["type"].type_value
                else:
                    return method["type"]

            applicability = method['modifier'].applicability
            if applicability == "instance":
                applicability = "non-static"
            else:
                applicability = "static"
            if (ast.CURRENT_CLASS_DICTIONARY == classObject):
                list1 = []
                list2 = []
                for arg in arguments.args:
                    list1.append(find_expr_type(arg))
                for formal in method["formals"].formals:
                    list2.append(formal.type)
                for i in range(len(list1)):
                    result = check_subtype(list1[i], list2[i])
                    if (result == False):
                        print("STATIC METHOD INVOCATION - Bad arguments")
                        sys.exit()
                if (isinstance(method["type"], ast.Type)):
                    return method["type"].type_value
                else:
                    return method["type"]
            if (className == fieldAccess.primary.id):
                if (applicability == "non-static"):
                    print("STATIC METHOD INVOCATION - No such method")
                    sys.exit()
                else:
                    list1 = []
                    list2 = []
                    for arg in arguments.args:
                        list1.append(find_expr_type(arg))
                    for formal in method["formals"].formals:
                        list2.append(formal.type)
                    for i in range(len(list1)):
                        result = check_subtype(list1[i], list2[i])
                        if (result == False):
                            print("STATIC METHOD INVOCATION - Bad arguments")
                            sys.exit()
                    if (isinstance(method["type"], ast.Type)):
                        return method["type"].type_value
                    else:
                        return method["type"]
            if applicability == "non-static":
                print("STATIC METHOD INVOCATION - No such method")
                sys.exit()

            list1 = []
            list2 = []
            for arg in arguments.args:
                list1.append(find_expr_type(arg))
            for formal in method["formals"].formals:
                list2.append(formal.type)
            for i in range(len(list1)):
                result = check_subtype(list1[i], list2[i])
                if (result == False):
                    print("STATIC METHOD INVOCATION - Bad arguments")
                    sys.exit()
            if (isinstance(method["type"], ast.Type)):
                return method["type"].type_value
            else:
                return method["type"]

def get_lhs_type(lhs):
    if (isinstance(lhs, ast.ID)):
        result = get_type(ast.VARIABLE_TABLE, lhs.id)
        return(result)
    if (isinstance(lhs, ast.Field_Access)):
        if (lhs.primary == 'this'):
            result =(get_this_type(ast.FIELD_DICTIONARY, lhs.id))
            return result
        if (lhs.primary == "super"):
            return(get_super_type(ast.CURRENT_CLASS_DICTIONARY, ast.GLOBAL_CLASS_RECORD, lhs.id))
        if (isinstance(lhs.primary, ast.ID)):
            field_status = ""
            if (lhs.primary.id in ast.GLOBAL_CLASS_RECORD.keys()):
                field_status = "static"
                className = lhs.primary.id
            else:
                field_status = "non-static"
                className = get_type(ast.VARIABLE_TABLE, lhs.primary.id)
            classObject = ast.GLOBAL_CLASS_RECORD[className]
            classField = classObject['fields']
            for key, value in classField.items():
                if (lhs.id == value["variableName"]):
                    visibility = value['fieldModifier'].split(", ")[0]
                    applicability = value['fieldModifier'].split(", ")[1]
                    if (applicability == "class"):
                        applicability = "static"
                    else:
                        applicability = "non-static"
                    if (field_status == "static"):
                        if (applicability == "static"):
                            return(value['type'])
                        else:
                            print("STATIC FIELD ACCESS - No such field")
                            sys.exit()
                    if (field_status == "non-static"):
                        if (applicability == "non-static"):
                            return(value['type'])
                        else:
                            print("NON-STATIC FIELD ACCESS - No such field")
                            sys.exit() 
                    return(value['type'])
                
def get_auto_type(lhs, post, pre):
    auto_type = get_lhs_type(lhs)
    if (auto_type != "int" and auto_type != "float"):
        if (pre == '++' or post == "++"):
            print("AUTO-INCREMENT - Operand is not a number")
            sys.exit()
        else:
            print("AUTO-DECREMENT - Operand is not a number")
            sys.exit()
    return auto_type

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
                    visibility = value['fieldModifier'].split(", ")[0]
                    applicability = value['fieldModifier'].split(", ")[1]
                    if (applicability == "class"):
                        applicability = "static"
                    else:
                        applicability = "non-static"
                    if (applicability != "static"):
                        print("STATIC FIELD ACCESS - No such field")
                        sys.exit()
                    return(value['type'])
    if (isinstance(expr, ast.Paren)):
        return(find_expr_type(expr.expr))
    if (isinstance(expr, ast.New)):
        return(get_new_type(expr))
    if (isinstance(expr, ast.Method_Invocation)):
        result = get_method_invocation_type(expr.fieldAccess, expr.arguments)
        return(result)
    if (isinstance(expr, ast.Assign)):
        return get_assign_type(expr.lhs, expr.expr)
    if (isinstance(expr, ast.Auto)):
        return(get_auto_type(expr.lhs, expr.post, expr.pre))
    if (isinstance(expr, ast.Binary_Expr)):
        result = get_binary_type(expr.leftExpr, expr.rightExpr, expr.binaryType)
        return result
    if (isinstance(expr, ast.Not)):
        result = get_neg_type(expr.expr)
        return result
    if (isinstance(expr, ast.Uminus)):
        result = get_uminus_type(expr.expr)
        return result
    if (isinstance(expr, ast.Uplus)):
        result = get_uplus_type(expr.expr)
        return result

def get_new_type(expr):
    list1 = []
    list2 = []
    for arg in expr.arguments.args:
        list1.append(find_expr_type(arg))

    constructorObject = {}
    for key, value in ast.GLOBAL_CONSTRUCTOR_DICTIONARY.items():
        if (expr.id.id == value["constructorName"]):
            constructorObject = value

    if len(list1) != len(constructorObject["formals"].formals):
        print("CONSTRUCTOR INVOCATION - Bad arguments")
        sys.exit()
    for formal in constructorObject["formals"].formals:
        list2.append(formal.type)
    for i in range(len(list1)):
        result = check_subtype(list1[i], list2[i])
        if (result == False):
            print("CONSTRUCTOR INVOCATION - Bad arguments")
            sys.exit()
    return expr.id.id



def get_paren_type(expr):
    return(find_expr_type(expr))

def get_neg_type(expr):
    result = find_expr_type(expr)
    if (result != "boolean"):
        return "error"
    else:
        return "boolean"

def get_uminus_type(expr):
    result = find_expr_type(expr)
    return result

def get_uplus_type(expr):
    return(find_expr_type(expr))

def get_binary_type(leftExpr, rightExpr, binaryType):
    leftExprType = None
    rightExprType = None
    leftExprType = find_expr_type(leftExpr)
    rightExprType = find_expr_type(rightExpr)
    result = combine_type(leftExprType, rightExprType, binaryType)
    return result
    
def get_assign_type(lhs, expr):
    lhs_type = get_lhs_type(lhs)
    if (lhs_type == "error"):
        return "error"
    expr_type = find_expr_type(expr)
    if (lhs_type in ast.GLOBAL_CLASS_RECORD):
        if (expr_type == "null"):
            return lhs_type
    if (expr_type == "error"):
        return "error"
    result = check_subtype(expr_type, lhs_type)
    if (result == True):
        return lhs_type
    else:
        return "error"

def get_stmt_type(stmt):
    if (isinstance(stmt, ast.If_decl)):
        expr_type = find_expr_type(stmt.expr)
        if (expr_type != "boolean"):
            return "error"
        stmt_one_type = get_stmt_type(stmt.stmtOne)
        if (stmt_one_type != "correct"):
            return "error"
        stmt_two_type = get_stmt_type(stmt.stmtTwo)
        if(stmt_two_type != "correct"):
            return "error"
        return "correct"

    if (isinstance(stmt, ast.While_decl)):
        expr_type = find_expr_type(stmt.expr)
        if (expr_type != "boolean"):
            return "error"
        stmt_type = get_stmt_type(stmt.stmt)
        if(stmt_type == "correct"):
            return "correct"
        else:
            print("Error: invalid stmt")

    if (isinstance(stmt, ast.For_decl)):
        for_cond_1_type = get_stmt_expr_type(stmt.cond1)
        if (for_cond_1_type != "correct"):
            print("Type error in initializer")
            
        for_cond_2_type = find_expr_type(stmt.cond2)
        for_cond_3_type = get_stmt_expr_type(stmt.cond3)
        for_body_type = ""
        if (for_cond_1_type == "correct" and for_cond_2_type == "boolean" and for_cond_3_type == "correct" and for_body_type == "correct"):
            return "correct"
        else:
           return "error"

    if (isinstance(stmt, ast.Return)):
        return_val_type = ""
        if (stmt.return_val == None):
            return_val_type = "void"
        else:
            return_val_type = find_expr_type(stmt.return_val)
        method_type = ast.CURRENT_METHOD_DICTIONARY["type"]
        if (method_type == return_val_type):
            return "correct"
        if (method_type != "void" and return_val_type == "void"):
            return "error"
        if (method_type == "void" and return_val_type != "void"):
            return "error"
        if (method_type != return_val_type):
            return "error"

    if (isinstance(stmt, ast.Method_Invocation)):
        return(get_method_invocation_type(stmt.fieldAccess, stmt.arguments))

    if(isinstance(stmt, ast.Assign)):
        result = get_assign_type(stmt.lhs, stmt.expr)
        return result
    
    if (stmt == "break"):
        return "correct"

    if (stmt == "continue"):
        return "correct"

    if (isinstance(stmt, ast.Block)):
        result = check_block_type_correct(stmt.stmtList.stmts)
        if (result == "error"):
            return result
    
    if (stmt == ';'):
        return "correct"
    
    if (stmt is None):
        return 'correct'
    
def get_stmt_expr_type(stmtExpr):
    if (isinstance(stmtExpr, ast.Assign)):
        result = get_assign_type(stmtExpr.lhs, stmtExpr.expr)
        if (result == False):
            return "error"
        else:
            return result
    if (isinstance(stmtExpr, ast.Auto)):
        result = get_auto_type(stmtExpr.lhs, stmtExpr.post, stmtExpr.pre)
        if (result == "error"):
            return "error"
        else:
            return "correct"
    if (isinstance(stmtExpr, ast.Method_Invocation)):
        result = get_method_invocation_type(stmtExpr.fieldAccess, stmtExpr.arguments)
        if (result):
            return "correct"
        
def check_block_type_correct(stmts):
    for stmt in stmts:
        result = get_stmt_type(stmt)
        if (result == "error"):
            return result

def check_subtype(subType, superType):
    if (subType == superType):
        return True
    if (subType == "int" and superType == "float"):
        return True
    if ("user" in superType and subType == "null"):
        return True
    return False
    # todo null
    # todoc class literal

def get_return_type(return_val):
    if (isinstance(return_val, ast.Return)):
        return_val_type = ""
    if (return_val == None):
        return_val_type = "void"
    else:
        return_val_type = find_expr_type(return_val)
    method_type = ast.CURRENT_METHOD_DICTIONARY["type"]
    if (method_type == return_val_type):
        return "correct"
    if (method_type != "void" and return_val_type == "void"):
        return "error non-void method"
    if (method_type == "void" and return_val_type != "void"):
        return "error void method"
    if (method_type != return_val_type):
        return "error"
    
    