import sys

FIELD_DICTIONARY = {}
FIELD_KEY = 1
CLASS_NAME = ""

CONSTRUCTOR_DICTIONARY = {}
CONSTRUCTOR_KEY = 1

CONSTRUCTOR_PARAM_KEY = 1

METHOD_DICTIONARY = {}
METHOD_KEY = 1

METHOD_PARAM_KEY = 1

GLOBAL_CONSTRUCTOR_VARIABLE_TABLE = []
GLOBAL_METHOD_VARIABLE_TABLE = []

VARIABLE_TABLE = []
VARIABLE_KEY = 1

GLOBAL_CLASS_RECORD = {}

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
        built_in_types = ["int", "float", "boolean", "string"]
        if not type_value in built_in_types:
            self.type_value = f"user({type_value})"
        else:
            self.type_value = type_value
    def __str__(self):
        return str(self.type_value)

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
                    print("Error: Variables must be declared at the top of the block before any other statements other than variable declarations")
                    sys.exit()
            else:
                variableStatus = False
    
        VARIABLE_TABLE.append(insideVariableTable)
    def __str__(self):
        result = 'Block([\n'
        add_var_decl_status = True
        for stmt in self.stmtList.stmts[::-1]:
            if (not isinstance(stmt, Var_Decl) and add_var_decl_status):
                add_var_decl_status = False
            if (stmt == ';'):
                result += "Skip-stmt()\n"
            elif (isinstance(stmt, Block)):
                result = result + str(stmt) + ",\n"
            elif (stmt == 'continue'):
                result += "Continue-stmt() "
            elif (stmt == 'break'):
                result += "Break-stmt()\n"
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
        return f'Return-stmt({str(self.return_val)})'
    

METHOD_DICTIONARY[METHOD_KEY] = {
    'methodName': 'scan_int',
    'modifier': Modifier("public", "static"),
    'formals': Formals_const(),
    'type': Type("int"),
    'block': Block(Stmt_List())
}

METHOD_KEY += 1

METHOD_DICTIONARY[METHOD_KEY] = {
    'methodName': 'scan_float',
    'modifier': Modifier("public", "static"),
    'formals': Formals_const(),
    'type': Type("float"),
    'block': Block(Stmt_List())
}

METHOD_KEY += 1

GLOBAL_CLASS_RECORD["In"] = {
    'className': "In",
    'superClassName': '',
    'constructors': {},
    'fields': {},
    'methods': METHOD_DICTIONARY,   
}

METHOD_DICTIONARY = {}
FIELD_DICTIONARY = {}
METHOD_DICTIONARY = {}

stmt_list = Stmt_List()
stmt_list.stmts.append(Return(""))

METHOD_DICTIONARY[METHOD_KEY] = {
    'methodName': 'print',
    'modifier': Modifier("public", "static"),
    'formals': Formals_const(),
    'type': Type("int"),
    'block': Block(stmt_list)
}

METHOD_KEY += 1

METHOD_DICTIONARY[METHOD_KEY] = {
    'methodName': 'print',
    'modifier': Modifier("public", "static"),
    'formals': Formals_const(),
    'type': Type("float"),
    'block': Block(stmt_list)
}

METHOD_KEY += 1

METHOD_DICTIONARY[METHOD_KEY] = {
    'methodName': 'print',
    'modifier': Modifier("public", "static"),
    'formals': Formals_const(),
    'type': Type("boolean"),
    'block': Block(stmt_list)
}

METHOD_KEY += 1

METHOD_DICTIONARY[METHOD_KEY] = {
    'methodName': 'print',
    'modifier': Modifier("public", "static"),
    'formals': Formals_const(),
    'type': Type("string"),
    'block': Block(stmt_list)
}

METHOD_KEY += 1

GLOBAL_CLASS_RECORD["Out"] = {
    'className': "Out",
    'superClassName': '',
    'constructors': {},
    'fields': {},
    'methods': METHOD_DICTIONARY,   
}

METHOD_DICTIONARY = {}
FIELD_DICTIONARY = {}
METHOD_DICTIONARY = {}

class Program(Node):
    def __init__(self, classes):
        super().__init__()
        self.classes = classes
    def __str__(self):
        global GLOBAL_CLASS_RECORD, VARIABLE_TABLE
        result = ""
        for key, value in GLOBAL_CLASS_RECORD.items():
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

            
            result = result + f'Class Name: {key}\nSuperclass Name: {value["superClassName"]}\n{field_result}{constructor_result}{method_result}' + "-------------------------------------------------------------------------------------\n"
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

        global CONSTRUCTOR_KEY, VARIABLE_TABLE, VARIABLE_KEY

        CONSTRUCTOR_DICTIONARY[CONSTRUCTOR_KEY] = {
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
        return f'Expr( Assign({str(self.lhs)}, {str(self.expr)}) )'

class Field_Access(Node):
    def __init__(self, primary, id):
        super().__init__()
        self.primary = primary
        self.id = id
    def __str__(self):
        return f'Field-access({self.primary}, {self.id})'
    

class Literal(Node):
    def __init__(self, literal):
        super().__init__()
        self.literal = literal
    def __str__(self):
        if (self.literal == "true"):
            return f'Constant(True)'
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
        
class Uminus(Node):
    def __init__(self, type = None, expr = None):
        super().__init__()
        self.type = type
        self.expr = expr
    def __str__(self):
        return f'Unary-expression(MINUS, {str(self.expr)})'

class Method_Invocation(Node):
    def __init__(self, fieldAccess, arguments):
        super().__init__()
        self.fieldAccess = fieldAccess
        self.arguments = arguments
    def __str__(self):
        return f'Method-call({self.fieldAccess.primary}, {self.fieldAccess.id}, {str(self.arguments.args[::-1])})'
    
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
        return f'New-object({self.id}, {str(self.arguments.args)})'
    
class If_decl(Node):
    def __init__(self, expr, stmtOne, stmtTwo):
        super().__init__()
        self.expr = expr
        self.stmtOne = stmtOne
        self.stmtTwo = stmtTwo
    def __str__(self):
        return f'If-stmt({str(self.expr)}, {str(self.stmtOne)}, else {str(self.stmtTwo)})'
    
class Not(Node):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr
    def __str__(self):
        return f'Unary-expression(NEG, {str(self.expr)})'

class ID(Node):
    def __init__(self, id):
        super().__init__()
        self.id = id
    def __str__(self):
        global VARIABLE_TABLE, GLOBAL_CLASS_RECORD
        variableId = ''
        for variableTable in VARIABLE_TABLE[::-1]:
            for key, value in variableTable.items():
                if self.id == value["variableName"]:
                    variableId = f'Variable({key})'
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
        return f"While-stmt({str(self.expr)}, {str(self.stmt)})"
    
class Paren(Node):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr
    def __str__(self):
        return str(self.expr)