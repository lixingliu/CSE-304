'''
Name: Li Xing Liu
Netid: lixiliu
Student Id: 113318331

Name: Andy You
Netid: Andyou
Student Id: 113494190
'''

import sys

FIELD_DICTIONARY = {}
FIELD_KEY = 1
CLASS_NAME = ""
GLOBAL_CONSTRUCTOR_DICTIONARY = {}
CONSTRUCTOR_DICTIONARY = {}
CONSTRUCTOR_KEY = 1

CONSTRUCTOR_PARAM_KEY = 1

METHOD_DICTIONARY = {}
METHOD_KEY = 1

METHOD_PARAM_KEY = 1

VARIABLE_TABLE = []
VARIABLE_KEY = 1

GLOBAL_CLASS_RECORD = {}
CURRENT_CLASS_DICTIONARY = {}
CURRENT_METHOD_DICTIONARY = {}
import decaf_typecheck as typechecker

class Node():
    def __init__(self):
        self.parent = None
    def parentCount(self):
        count = 0
        current = self.parent
        while current is not None:
            count += 1
            current = current.parent
        return count
    
class Modifier(Node):
    def __init__(self, visibility, applicability = None):
        super().__init__()
        self.visibility = visibility
        self.applicability = applicability
        if self.visibility == None:
            self.visibility = "private"
        if self.applicability == "static":
            self.applicability = "class"
        else:
            self.applicability = "instance"
    def __str__(self):
        return f'{str(self.visibility)}, {str(self.applicability)}'

class Formals_const(Node):
    def __init__(self):
        super().__init__()
        self.formals = []

class Var_Decl(Node):
    def __init__(self, type, variable_list):
        super().__init__()
        self.type = type
        self.variable_list = variable_list
    

class Type(Node):
    def __init__(self, type_value):
        super().__init__()
        built_in_types = ["int", "float", "boolean", "string", "void", "error", "null", "class-literal"]
        if not type_value in built_in_types:
            self.type_value = f"user({type_value})"
        else:
            self.type_value = type_value
    def __str__(self):
        return str(self.type_value)

    #def __eq__(self)!!!
class Block(Node):
    def __init__(self, stmtList):
        super().__init__()
        self.stmtList = stmtList
        global VARIABLE_TABLE, VARIABLE_KEY
        insideVariableTable = {}
        variableStatus = True
        for stmt in self.stmtList.stmts[::-1]:
            if (isinstance(stmt, Var_Decl)):
                if (variableStatus):
                    for variable in stmt.variable_list.vars[::-1]:
                        if any(entry.get('variableName') == variable for entry in insideVariableTable.values()):
                            print(f"Error: Variable names must be unique within a block. You are trying to declare multiple variables of the name {variable}")
                            sys.exit()
                        insideVariableTable[VARIABLE_KEY] = {
                            'variableName': variable,
                            'variableKind': 'local',
                            'variableType': stmt.type,
                        }
                        VARIABLE_KEY += 1
                else:
                    print(f"Error: Invalid Variable Declaration: {str(stmt.type)} {str(stmt.variable_list.vars[::-1][0])}. Variables must be declared at the top of the block before any other statements other than variable declarations")
                    sys.exit()
            else:
                variableStatus = False
    
        VARIABLE_TABLE.append(insideVariableTable)
    def __str__(self):
        result = 'Block([\n'
        add_var_decl_status = True
        if len(self.stmtList.stmts) == 0:
            result += "Skip-stmt()\n"
        for stmt in self.stmtList.stmts[::-1]:
            if (not isinstance(stmt, Var_Decl) and add_var_decl_status):
                add_var_decl_status = False
            if (stmt == ';'):
                result += "Skip-stmt()\n"
            elif (isinstance(stmt, Block)):
                result = result + str(stmt) + ",\n"
            elif (stmt == 'continue'):
                result += "Continue-stmt()" + ",\n"
            elif (stmt == 'break'):
                result += "Break-stmt()" + ",\n"
            elif (isinstance(stmt, Auto)):
                result = result + str(stmt) + ",\n"
            elif (isinstance(stmt, Assign)):
                result = result + str(stmt) + ",\n"
            elif (isinstance(stmt, Return)):
                result = result + str(stmt) + ",\n"
            elif (isinstance(stmt, For_decl)):
                result = result + str(stmt) + ",\n"
            elif (isinstance(stmt, Method_Invocation)):
                result = result + str(stmt) + ",\n"
            elif (isinstance(stmt, If_decl)):
                result = result + str(stmt) + ",\n"
            elif (isinstance(stmt, While_decl)):
                result = result + str(stmt) + ",\n"
        return result[:-2] + result[-1] + "])"

class Stmt_List(Node):
    def __init__(self):
        super().__init__()
        self.stmts = []

class Return(Node):
    def __init__(self, return_val):
        super().__init__()
        self.return_val = return_val
    def __str__(self):
        return_val = typechecker.get_return_type(self.return_val)
        if (return_val == "error non-void method"):
            print("RETURN statement - NON-VOID method returns nothing")
            sys.exit()
        if (return_val == "error void method"):
            print("RETURN statement - VOID method returns a value")
            sys,exit()
        if (return_val == "error"):
            print("RETURN statement - return variable does not match method type")
            sys.exit()
        return f'Return-stmt({str(self.return_val)})'
    

# METHOD_DICTIONARY[METHOD_KEY] = {
#     'methodName': 'scan_int',
#     'modifier': Modifier("public", "static"),
#     'formals': Formals_const(),
#     'type': Type("int"),
#     'block': Block(Stmt_List())
# }

# METHOD_KEY += 1

# METHOD_DICTIONARY[METHOD_KEY] = {
#     'methodName': 'scan_float',
#     'modifier': Modifier("public", "static"),
#     'formals': Formals_const(),
#     'type': Type("float"),
#     'block': Block(Stmt_List())
# }

# METHOD_KEY += 1

# GLOBAL_CLASS_RECORD["In"] = {
#     'className': "In",
#     'superClassName': '',
#     'constructors': {},
#     'fields': {},
#     'methods': METHOD_DICTIONARY,   
# }

# METHOD_DICTIONARY = {}
# FIELD_DICTIONARY = {}
# METHOD_DICTIONARY = {}

# stmt_list = Stmt_List()
# stmt_list.stmts.append(Return(""))

# METHOD_DICTIONARY[METHOD_KEY] = {
#     'methodName': 'print',
#     'modifier': Modifier("public", "static"),
#     'formals': Formals_const(),
#     'type': Type("int"),
#     'block': Block(stmt_list)
# }

# METHOD_KEY += 1

# METHOD_DICTIONARY[METHOD_KEY] = {
#     'methodName': 'print',
#     'modifier': Modifier("public", "static"),
#     'formals': Formals_const(),
#     'type': Type("float"),
#     'block': Block(stmt_list)
# }

# METHOD_KEY += 1

# METHOD_DICTIONARY[METHOD_KEY] = {
#     'methodName': 'print',
#     'modifier': Modifier("public", "static"),
#     'formals': Formals_const(),
#     'type': Type("boolean"),
#     'block': Block(stmt_list)
# }

# METHOD_KEY += 1

# METHOD_DICTIONARY[METHOD_KEY] = {
#     'methodName': 'print',
#     'modifier': Modifier("public", "static"),
#     'formals': Formals_const(),
#     'type': Type("string"),
#     'block': Block(stmt_list)
# }

# METHOD_KEY += 1

# GLOBAL_CLASS_RECORD["Out"] = {
#     'className': "Out",
#     'superClassName': '',
#     'constructors': {},
#     'fields': {},
#     'methods': METHOD_DICTIONARY,   
# }

# METHOD_DICTIONARY = {}
# FIELD_DICTIONARY = {}
# METHOD_DICTIONARY = {}

class Program(Node):
    def __init__(self, classes):
        super().__init__()
        self.classes = classes
    def __str__(self):
        global GLOBAL_CLASS_RECORD, VARIABLE_TABLE, FIELD_DICTIONARY, CURRENT_CLASS_DICTIONARY, CURRENT_METHOD_DICTIONARY
        result = ""
        for key, value in GLOBAL_CLASS_RECORD.items():
            FIELD_DICTIONARY = value["fields"]
            CURRENT_CLASS_DICTIONARY = value
            if value["className"] == 'Out' or value["className"] == "In":
                continue

# ============================================================================================
            field_result = "Fields:\n"
            for field_key, field_value in value["fields"].items():
                field_result += f'FIELD {field_key}, {field_value["variableName"]}, {key}, {field_value["fieldModifier"]}, {field_value["type"]}\n'
# ========================================================================================================================================================================================
            constructor_result = "Constructors:\n"
            for constructor_key, constructor_value in value["constructors"].items():
                constructor_result += f'CONSTRUCTOR: {constructor_key}, {constructor_value["modifier"].visibility}\nConstructor Paramters:'
                variableTableResult = "Variable Table:\n"
                constructorParamId = []
                for variableTable in constructor_value["variableTable"]:
                    for variable_key, variable_value in variableTable.items():
                        if (variable_value["variableKind"] == "formal"):
                            constructorParamId.append(variable_key)
                        variableTableResult = variableTableResult + f'VARIABLE {variable_key}, {variable_value["variableName"]}, {variable_value["variableKind"]}, {variable_value["variableType"]}\n'
                VARIABLE_TABLE = constructor_value["variableTable"]

                constructor_result = f'{constructor_result} {str(constructorParamId)[1:-1]}\n{variableTableResult}Constructor Body:\n{constructor_value["block"]}\n'
# ========================================================================================================================================================================================
            method_result = "Methods:\n"
            for method_key, method_value in value["methods"].items():
                CURRENT_METHOD_DICTIONARY = method_value
                method_result += f'METHOD: {method_key}, {method_value["methodName"]}, {key}, {method_value["modifier"].visibility}, {method_value["modifier"].applicability}, {method_value["type"]}\nMethod Parameters:'
                variableTableResult = "Variable Table:\n"
                methodParamId = []
                for variableTable in method_value["variableTable"]:
                    for variable_key, variable_value in variableTable.items():
                        if (variable_value["variableKind"] == "formal"):
                            methodParamId.append(variable_key)
                        variableTableResult = variableTableResult + f'VARIABLE {variable_key}, {variable_value["variableName"]}, {variable_value["variableKind"]}, {variable_value["variableType"]}\n'
                VARIABLE_TABLE = method_value["variableTable"]
                method_result = f'{method_result} {str(methodParamId)[1:-1]}\n{variableTableResult}Method Body:\n{method_value["block"]}\n'
# ========================================================================================================================================================================================

            
            result = result + f'Class Name: {key}\nSuperclass Name: {value["superClassName"]}\n{field_result}{constructor_result}{method_result}' + "--------------------------------------------------------------------------\n"
        return result
    
class Class_decl_list(Node):
    def __init__(self):
        super().__init__()
        self.classList = []

class Class_decl(Node):
    def __init__(self, className, classBody, superClassName = ''):
        super().__init__()
        self.className = className
        self.superClassName = superClassName
        self.classBody = classBody
        
        global GLOBAL_CLASS_RECORD, CONSTRUCTOR_DICTIONARY, FIELD_DICTIONARY, METHOD_DICTIONARY, CLASS_NAME, VARIABLE_KEY

        if self.className in GLOBAL_CLASS_RECORD.keys():
            print(f"Error: Class Names must be unique. You have multiple class names of {self.className}")
            sys.exit()

        CLASS_NAME = self.className
        GLOBAL_CLASS_RECORD[self.className] = {
            'className': self.className,
            'superClassName': self.superClassName,
            'constructors': CONSTRUCTOR_DICTIONARY,
            'fields': FIELD_DICTIONARY,
            'methods': METHOD_DICTIONARY,            
        } 
        VARIABLE_KEY = 1
        CONSTRUCTOR_DICTIONARY = {}
        FIELD_DICTIONARY = {}
        METHOD_DICTIONARY = {}

class Class_Body_List(Node):
    def __init__(self, singleItem):
        super().__init__()
        self.classBodyItems = [singleItem]
    
class Field_Decl(Node):
    def __init__(self, fieldModifier, fieldVarDecl):
        super().__init__()
        self.fieldModifier = fieldModifier
        self.fieldVarDecl = fieldVarDecl
        global FIELD_KEY, CLASS_NAME, FIELD_DICTIONARY
        built_in_types = ["int", "float", "boolean", "string"]

        if (str(self.fieldVarDecl.type) not in built_in_types):
            self.fieldVarDecl.type = f'user({self.fieldVarDecl.type})'

        for variable in self.fieldVarDecl.variable_list.vars[::-1]:
            if any(entry.get('variableName') == variable for entry in FIELD_DICTIONARY.values()):
                print(f"Error: Multiple Fields with the name {variable} has been detected. Field variables must have unique names")
                sys.exit()
            FIELD_DICTIONARY[FIELD_KEY] = {
                'className': CLASS_NAME,
                'variableName': variable,
                'fieldModifier': str(self.fieldModifier),
                'type': str(self.fieldVarDecl.type)
            }
            FIELD_KEY += 1

class Constructor_Decl(Node):
    def __init__(self, modifier, constructorName, formals, block):
        super().__init__()
        self.modifier = modifier
        self.constructorName = constructorName
        self.formals = formals
        self.block = block

        global CONSTRUCTOR_KEY, VARIABLE_TABLE, VARIABLE_KEY, GLOBAL_CONSTRUCTOR_DICTIONARY

        CONSTRUCTOR_DICTIONARY[CONSTRUCTOR_KEY] = {
            'modifier': self.modifier,
            'constructorName': self.constructorName,
            'formals': self.formals,
            'block': self.block,
            'variableTable': VARIABLE_TABLE
        }
        
        GLOBAL_CONSTRUCTOR_DICTIONARY[CONSTRUCTOR_KEY] = {
            'modifier': self.modifier,
            'constructorName': self.constructorName,
            'formals': self.formals,
            'block': self.block,
            'variableTable': VARIABLE_TABLE
        }
        VARIABLE_TABLE = []
        CONSTRUCTOR_KEY += 1
        VARIABLE_KEY = 1
    
class Method_Decl(Node):
    def __init__(self, modifier, type, id, formals, block):
        super().__init__()
        self.modifier = modifier
        self.methodName = id
        self.type = type
        self.formals = formals
        self.block = block
        global METHOD_KEY, VARIABLE_TABLE, VARIABLE_KEY

        METHOD_DICTIONARY[METHOD_KEY] = {
            'methodName': self.methodName,
            'modifier': self.modifier,
            'formals': self.formals,
            'type': self.type,
            'block': self.block,
            'variableTable': VARIABLE_TABLE
        }
        METHOD_KEY += 1
        VARIABLE_TABLE = []
        VARIABLE_KEY = 1

class Variables_cont(Node):
    def __init__(self):
        super().__init__()
        self.vars = []
    
class Formal_param(Node):
    def __init__(self, type, variable):
        super().__init__()
        self.type = type
        self.variable = variable
        global VARIABLE_KEY, VARIABLE_TABLE
        variableTableDict = {}
        variableTableDict[VARIABLE_KEY] = {
            'variableName': self.variable,
            'variableKind': 'formal',
            'variableType': self.type
        }
        VARIABLE_KEY += 1
        VARIABLE_TABLE.append(variableTableDict)




class Auto(Node):
    def __init__(self, post = None, pre = None, lhs = None):
        super().__init__()
        self.post = post
        self.pre = pre
        self.lhs = lhs
    def __str__(self):
        if (self.pre == "++"):
            return f'Expr( Auto({self.lhs}, auto-increment, pre) )'
        elif (self.pre == "--"):
            return f'Expr( Auto({self.lhs}, auto-decrement, pre) )'
        elif (self.post == "++"):
            return f'Expr( Auto({self.lhs}, auto-increment, post) )'
        elif (self.post == "--"):
            return f'Expr( Auto({self.lhs}, auto-decrement, post) )'

class Assign(Node):
    def __init__(self, lhs = None, expr = None):
        super().__init__()
        self.lhs = lhs
        self.expr = expr
    def __str__(self):
        global VARIABLE_TABLE
        assign_type = typechecker.get_assign_type(self.lhs, self.expr)
        if (assign_type == "error"):
            if (isinstance(self.expr, ID)):
                print("Variable not the same type as assigner")
                sys.exit()
            if (isinstance(self.expr, Literal)):
                print("Literal not the same type as assigner")
                sys.exit()
            if (isinstance(self.expr, Field_Access)):
                print("Field access not the same type as the assigner")
                sys.exit()
            if (isinstance(self.expr, New)):
                print("New object does not match assigner")
                sys.exit()
            if (isinstance(self.expr, Method_Invocation)):
                print("Method type is not the same as the assigner")
                sys.exit()
            if (isinstance(self.expr, Assign)):
                print("ASSIGN statement - type not equal to assigner")
                sys.exit()
            if (isinstance(self.expr, Auto)):
                print("AUTO statement - type not equal to assigner")
                sys.exit()            
            if (isinstance(self.expr, Binary_Expr)):
                if (self.expr.binaryType == "+"):
                    print("BINARY ADDITION - Operand not a number")
                    sys.exit()
                if (self.expr.binaryType == "-"):
                    print("BINARY SUBTRACTION  - Operand not a number")
                    sys.exit()
                if (self.expr.binaryType == "*"):
                    print("BINARY MULTIPLICATION  - Operand not a number")
                    sys.exit()
                if (self.expr.binaryType == "/"):
                    print("BINARY DIVISION  - Operand not a number")
                    sys.exit()
                if (self.expr.binaryType == "&&"):
                    print("BINARY AND - Operand not a boolean")
                    sys.exit()
                if (self.expr.binaryType == "||"):
                    print("BINARY OR - Operand not a boolean")
                    sys.exit()
                if (self.expr.binaryType == "<"):
                    print("BINARY LESS THAN - Operand not a number")
                    sys.exit()
                if (self.expr.binaryType == "<="):
                    print("BINARY LESS THAN OR EQUAL - Operand not a number")
                    sys.exit()
                if (self.expr.binaryType == ">"):
                    print("BINARY GREATER THAN - Operand not a number")
                    sys.exit()
                if (self.expr.binaryType == ">="):
                    print("BINARY GREATER THAN OR EQUAL - Operand not a number")
                    sys.exit()
                if (self.expr.binaryType == "=="):
                    print("BINARY EQUALITY - Operands are not of congruent types")
                    sys.exit()
                if (self.expr.binaryType == "!="):
                    print("BINARY INEQUALITY - Operands are not of congruent types")
                    sys.exit()
            if (isinstance(self.expr, Not)):
                print("UNARY NEGATION - Expression is not boolean")
                sys.exit()  
            if (isinstance(self.expr, Uminus)):
                print("UNARY MINUS - Expression is not a number")
                sys.exit()  
            if (isinstance(self.expr, Uplus)):
                print("UNARY PLUS - Expression is not a number")
                sys.exit()  
            return "error"
        left = typechecker.get_lhs_type(self.lhs)
        right = typechecker.find_expr_type(self.expr)
        return(f'Expr( Assign({str(self.lhs)}, {str(self.expr)}), {str(left)}, {str(right)} )')

class Field_Access(Node):
    def __init__(self, primary, id):
        super().__init__()
        self.primary = primary
        self.id = id
    def __str__(self):
        global FIELD_DICTIONARY, GLOBAL_CLASS_RECORD, VARIABLE_TABLE, CURRENT_CLASS_DICTIONARY

        if (isinstance(self.primary, ID)):
            if (self.primary.id in GLOBAL_CLASS_RECORD.keys()):
                className = self.primary.id
            else:
                className = typechecker.get_type(VARIABLE_TABLE, self.primary.id)
            classObject = GLOBAL_CLASS_RECORD[className]
            classField = classObject["fields"]
            for key, value in classField.items():
                if (self.id == value["variableName"]):
                    return f'Field-access({self.primary}, {self.id}, {key})'
                
        if (self.primary == "this"):
            for key, value in FIELD_DICTIONARY.items():
                if (self.id == value["variableName"]):
                    return f'Field-access({self.primary}, {self.id}, {key})'
            fieldDictionary = (GLOBAL_CLASS_RECORD[CURRENT_CLASS_DICTIONARY['superClassName']])['fields']
            for key, value in fieldDictionary.items():
                if (self.id == value["variableName"]):
                    return f'Field-access({self.primary}, {self.id}, {key})'
        if(self.primary == "super"):
            superClassName = CURRENT_CLASS_DICTIONARY["superClassName"]
            if superClassName == "":
                print("Error: Super class does not exist")
                sys.exit()
            classObject = GLOBAL_CLASS_RECORD[superClassName]
            classField = classObject['fields']
            for key, value in classField.items():
                if (self.id == value["variableName"]):
                    return f'Field-access({self.primary}, {self.id}, {key})'
        
    

class Literal(Node):
    def __init__(self, literal):
        super().__init__()
        self.literal = literal
    def __str__(self):
        if (self.literal == "true"):
            return f'Constant(True)'
        if (self.literal == "false"):
            return f'Constant(False)'
        if (isinstance(self.literal, int)):
            return f'Constant(Integer-constant({self.literal}))'
        elif (isinstance(self.literal, float)):
            return f'Constant(Float-constant({self.literal}))'
        elif (isinstance(self.literal, str)):
            return f'Constant(String-constant({self.literal}))'
        else:
            return

class For_decl(Node):
    def __init__(self, cond1, cond2, cond3, forBody):
        super().__init__()
        self.cond1 = cond1
        self.cond2 = cond2
        self.cond3 = cond3
        self.forBody = forBody
    def __str__(self):
        cond1_type = typechecker.get_stmt_expr_type(self.cond1)
        if (cond1_type == "error"):
            print("FOR statement - Type error in initializer")
            sys.exit()
        cond2_type = typechecker.find_expr_type(self.cond2)
        if (cond2_type != "boolean"):
            print("FOR statement - Condition not boolean")
            sys.exit()
        cond3_type = typechecker.get_stmt_expr_type(self.cond3)
        if (cond3_type == "error"):
            print("FOR statement - Type error in update expression")
            sys.exit()
        loop_body_type = typechecker.get_stmt_type(self.forBody)
        if (loop_body_type == "error"):
            print("FOR statement - Type error in loop body")
            sys.exit()
        
        if (self.forBody == ';'):
            self.forBody = "Skip-stmt()"
        return f'For-stmt({str(self.cond1)}, {str(self.cond2)}, {str(self.cond3)}, {str(self.forBody)})'
    
class Binary_Expr(Node):
    def __init__(self, leftExpr, rightExpr, binaryType):
        super().__init__()
        self.leftExpr = leftExpr
        self.rightExpr = rightExpr
        self.binaryType = binaryType
    def __str__(self):
        if (self.binaryType == '+'):
            return f'Binary(add, {str(self.leftExpr)}, {str(self.rightExpr)})'
        elif (self.binaryType == '-'):
            return f'Binary(sub, {str(self.leftExpr)}, {str(self.rightExpr)})'
        elif(self.binaryType == '*'):
            return f'Binary(mul, {str(self.leftExpr)}, {str(self.rightExpr)})'
        elif(self.binaryType == '/'):
            return f'Binary(div, {str(self.leftExpr)}, {str(self.rightExpr)})'
        elif(self.binaryType == '&&'):
            return f'Binary(and, {str(self.leftExpr)}, {str(self.rightExpr)})'
        elif(self.binaryType == '||'):
            return f'Binary(or, {str(self.leftExpr)}, {str(self.rightExpr)})'
        elif(self.binaryType == '=='):
            return f'Binary(eq, {str(self.leftExpr)}, {str(self.rightExpr)})'
        elif(self.binaryType == '!='):
            return f'Binary(neq, {str(self.leftExpr)}, {str(self.rightExpr)})'
        elif(self.binaryType == '<'):
            return f'Binary(lt, {str(self.leftExpr)}, {str(self.rightExpr)})'
        elif(self.binaryType == '<='):
            return f'Binary(leq, {str(self.leftExpr)}, {str(self.rightExpr)})'
        elif(self.binaryType == '>'):
            return f'Binary(gt, {str(self.leftExpr)}, {str(self.rightExpr)})'
        elif(self.binaryType == '>='):
            return f'Binary(geq, {str(self.leftExpr)}, {str(self.rightExpr)})'
        
#todo CREATE A UPLUS
class Uplus(Node):
    def __init__(self, type = None, expr = None):
        super().__init__()
        self.type = type
        self.expr = expr
    def __str__(self):
        expr_type = typechecker.find_expr_type(self.expr)
        if (expr_type != "int" and expr_type != "float"):
            print("UNARY MINUS - Expression is not a number")
            sys.exit()
        return f'Unary-expression(PLUS, {str(self.expr)})'
class Uminus(Node):
    def __init__(self, type = None, expr = None):
        super().__init__()
        self.type = type
        self.expr = expr
    def __str__(self):
        # expr_type = typechecker.find_expr_type(self.expr)
        # if (expr_type != "int" and expr_type != "float"):
        #     print("UNARY MINUS - Expression is not a number")
        #     sys.exit()
        return f'Unary-expression(MINUS, {str(self.expr)})'

class Method_Invocation(Node):
    def __init__(self, fieldAccess, arguments):
        super().__init__()
        self.fieldAccess = fieldAccess
        self.arguments = arguments
    def __str__(self):
        arguments = []
        for arg in self.arguments.args[::-1]:
            arguments.append(str(arg))
        
        if(isinstance(self.fieldAccess, ID)):
           return f"Method-call({self.fieldAccess.id}, {str(arguments)})"
        return f'Method-call({self.fieldAccess.primary}, {self.fieldAccess.id}, {str(arguments)})'
    
class Arguments_cont(Node):
    def __init__(self):
        super().__init__()
        self.args = []   

class New(Node):
    def __init__(self, id, arguments):
        super().__init__()
        self.id = id    
        self.arguments = arguments
    def __str__(self):
        arguments = []
        for args in self.arguments.args:
            arguments.append(str(args))
        return f'New-object({self.id}, {str(arguments)})'
    
class If_decl(Node):
    def __init__(self, expr, stmtOne, stmtTwo):
        super().__init__()
        self.expr = expr
        self.stmtOne = stmtOne
        self.stmtTwo = stmtTwo
    def __str__(self):
        expr_type = typechecker.find_expr_type(self.expr)
        print(expr_type)
        if(expr_type != "boolean"):
            print("IF statement - Condition not boolean")
            sys.exit()
        stmt_one_type = typechecker.get_stmt_type(self.stmtOne)
        if (stmt_one_type == "error"):
            print("IF statement - Type error in THEN statement")
            sys.exit()
        stmt_two_type = typechecker.get_stmt_type(self.stmtTwo)
        if (stmt_two_type == "error"):
            print("IF statement - Type error in ELSE statement")
            sys.exit()
        return f'If-stmt({str(self.expr)}, {str(self.stmtOne)}, else {str(self.stmtTwo)})'
    
class Not(Node):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr
    def __str__(self):
        expr_type = typechecker.find_expr_type(self.expr)
        if (expr_type != "boolean"):
            print("UNARY NEGATION - Expression is not boolean")
            sys.exit()
        return f'Unary-expression(NEG, {str(self.expr)})'

class ID(Node):
    def __init__(self, id):
        super().__init__()
        self.id = id
    def __str__(self):
        global VARIABLE_TABLE, GLOBAL_CLASS_RECORD, FIELD_DICTIONARY
        variableId = ''
        for variableTable in VARIABLE_TABLE[::-1]:
            for key, value in variableTable.items():
                if self.id == value["variableName"]:
                    variableId = f'Variable({key})'
                    return variableId
        for key, value in FIELD_DICTIONARY.items():
            if (self.id == value["variableName"]):
                return f'Field-access({self.id})'
        if (self.id in GLOBAL_CLASS_RECORD.keys()):
            return str(self.id)
        if (variableId == ''):
            print(f'ERROR: Variable {self.id} has not been declared')
            sys.exit()
        return variableId


    
class While_decl(Node):
    def __init__(self, expr, stmt):
        super().__init__()
        self.expr = expr
        self.stmt = stmt
    def __str__(self):
        expr_type = typechecker.find_expr_type(self.expr)
        if (expr_type != "boolean"):
            print("WHILE statement - Condition not boolean")
            sys.exit()
        stmt_type = typechecker.get_stmt_type(self.stmt)
        if (stmt_type == "error"):
            print("WHILE statement - Type error in loop body")
            sys.exit()
        return f"While-stmt({str(self.expr)}, {str(self.stmt)})"
    
class Paren(Node):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr
    def __str__(self):
        return str(self.expr)