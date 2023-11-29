import sys

FIELD_DICTIONARY = {}
FIELD_KEY = 1
CLASS_NAME = ""

CONSTRUCTOR_DICTIONARY = {}
CONSTRUCTOR_KEY = 1
CONSTRUCTOR_BLOCK = False

CONSTRUCTOR_PARAM_KEY = 1

METHOD_DICTIONARY = {}
METHOD_KEY = 1
METHOD_BLOCK = False

METHOD_PARAM_KEY = 1

GLOBAL_CONSTRUCTOR_VARIABLE_TABLE = []
GLOBAL_METHOD_VARIABLE_TABLE = []


GLOBAL_CLASS_RECORD = {}

def create_in_class():
    global CONSTRUCTOR_DICTIONARY, METHOD_DICTIONARY, FIELD_DICTIONARY

    pub_sta_mod = Modifier("public", "static")
    scan_int = Method_Decl(pub_sta_mod, Type("int"), "scan_int", Formals_const(), Block(Stmt_List())) #Initializing scan_int
    scan_float = Method_Decl(pub_sta_mod, Type("float"), "scan_int", Formals_const(), Block(Stmt_List())) #Initializing scan_float
    class_in_body_decl = Class_Body_List(scan_int)
    class_in_body_decl.classBodyItems.append(scan_float)
    class_in = Class_decl("In", class_in_body_decl) #Append the two methods to In's class_body_decl
    return class_in

def create_out_class():
    global CONSTRUCTOR_DICTIONARY, METHOD_DICTIONARY, FIELD_DICTIONARY

    pub_sta_mod = Modifier("public", "static")
    print_int_formal_cont = Formals_const()
    print_int_formal_cont.formals.append(Formal_param(Type("int"), Variable("i")))
    stmt_list = Stmt_List()
    stmt_list.stmts.append(Return(""))
    print_int = Method_Decl(pub_sta_mod, Type("int"),"print", print_int_formal_cont, Block(stmt_list)) #Initializing print_int

    print_float_formal_cont = Formals_const()
    print_float_formal_cont.formals.append(Formal_param(Type("float"), Variable("f")))
    print_float = Method_Decl(pub_sta_mod, Type('float'), "print", print_float_formal_cont, Block(stmt_list)) #Initializing print_float

    print_boolean_formal_cont = Formals_const()
    print_boolean_formal_cont.formals.append(Formal_param(Type("boolean"), Variable("b")))
    print_boolean = Method_Decl(pub_sta_mod, Type("boolean"), "print", print_boolean_formal_cont, Block(stmt_list)) #Initializing print_boolean

    print_string_formal_cont = Formals_const()
    print_string_formal_cont.formals.append(Formal_param(Type("string"), Variable("s")))
    print_string = Method_Decl(pub_sta_mod, Type("string"), "print", print_string_formal_cont, Block(stmt_list)) #Initializing print_string

    class_out_body_decl = Class_Body_List(print_int)
    class_out_body_decl.classBodyItems.append(print_float)
    class_out_body_decl.classBodyItems.append(print_boolean)
    class_out_body_decl.classBodyItems.append(print_string)
    class_out = Class_decl("Out", class_out_body_decl) #Append the four methods to Out's class_body_decl
    return class_out

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
    
class Program(Node):
    def __init__(self, classes):
        super().__init__()
        self.classes = classes
        create_in_class()
        create_out_class()
    def __str__(self):
        global CLASS_NAME, METHOD_DICTIONARY, CONSTRUCTOR_DICTIONARY, GLOBAL_CLASS_RECORD, FIELD_DICTIONARY
        result = ""



        # for class_object in self.classes.classList[::-1]:
        #     CLASS_NAME = class_object.className
        #     result = result + (str(class_object) + "\n") + "----------------------\n"
        #     if (class_object.className in GLOBAL_CLASS_RECORD.keys()):
        #         print("we have a problem, why is there 2 classes with the same name")
        #         sys.exit()
        #     GLOBAL_CLASS_RECORD[class_object.className] = {
        #         'constructors': CONSTRUCTOR_DICTIONARY,
        #         'fields': FIELD_DICTIONARY,
        #         'methods': METHOD_DICTIONARY,
        #     }
        #     METHOD_DICTIONARY = {}
        #     CONSTRUCTOR_DICTIONARY = {} 
        #     FIELD_DICTIONARY = {}
        result = ""
        for key, value in GLOBAL_CLASS_RECORD.items():
            # print(key, value)
            field_result = "Fields:\n"
            for field_key, field_value in value["fields"].items():
                field_result += f'FIELD {field_key}, {field_value["variableName"]}, {field_value["className"]}, {field_value["fieldModifier"]}, {field_value["type"]}\n'
            result = result + f'Class Name: {key}\nSuperclass Name: {value["superClassName"]}\n{field_result}\n' 
            # print("\n\n")
        print(result)
        # return result
        return ""
    
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
        
        global GLOBAL_CLASS_RECORD, CONSTRUCTOR_DICTIONARY, FIELD_DICTIONARY, METHOD_DICTIONARY, CLASS_NAME

        CLASS_NAME = self.className

        GLOBAL_CLASS_RECORD[self.className] = {
            'className': self.className,
            'superClassName': self.superClassName,
            'constructors': CONSTRUCTOR_DICTIONARY,
            'fields': FIELD_DICTIONARY,
            'methods': METHOD_DICTIONARY,            
        } 

        CONSTRUCTOR_DICTIONARY = {}
        FIELD_DICTIONARY = {}
        METHOD_DICTIONARY = {}

    def __str__(self):            
        global CONSTRUCTOR_PARAM_KEY, METHOD_PARAM_KEY, GLOBAL_CONSTRUCTOR_VARIABLE_TABLE, GLOBAL_METHOD_VARIABLE_TABLE, METHOD_DICTIONARY, CONSTRUCTOR_DICTIONARY, FIELD_DICTIONARY
# ============================================================================================
        field_result = "Fields:\n"
        for key, value in FIELD_DICTIONARY.items():
            field_result += f'FIELD {key}, {value["variableName"]}, {CLASS_NAME}, {value["fieldModifier"]}, {value["type"]}\n'
# ============================================================================================
        constructor_result = "Constructors:\n"
        for key, value in CONSTRUCTOR_DICTIONARY.items():
            constructorParamsId = []
            
            variableTable = {}
            variable_result = "Variable Table:\n"
            constructor_result += f'CONSTRUCTOR: {key}, {value["modifier"].visibility}\nConstructor Paramters:'
            for formal in value["formals"].formals[::-1]:
                variableTable[CONSTRUCTOR_PARAM_KEY] = {
                    'variableName': formal.variable,
                    'variableKind': 'formal',
                    'variableType': formal.type
                }
                CONSTRUCTOR_PARAM_KEY += 1
            GLOBAL_CONSTRUCTOR_VARIABLE_TABLE.append(variableTable)
            block_string_representation = str(value['block'])
            for variableTable in GLOBAL_CONSTRUCTOR_VARIABLE_TABLE:
                for key, stuff, in variableTable.items():
                    variable_result = variable_result + f'VARIABLE {key}, {stuff["variableName"]}, {stuff["variableKind"]}, {stuff["variableType"]}\n'
                    constructorParamsId.append(key)

            constructor_result = f'{constructor_result} {str(constructorParamsId)[1:-1]}\n{variable_result}Constructor Body:\n{block_string_representation}\n'

            GLOBAL_CONSTRUCTOR_VARIABLE_TABLE = []
# ============================================================================================
        method_result = "Methods:\n"
        for key, value in METHOD_DICTIONARY.items():
            methodParamsId = []

            variableTable = {}
            variable_result = "Variable Table:\n"
            method_result += f'METHOD: {key}, {value["methodName"]}, {CLASS_NAME}, {value["type"]}\nMethod Parameters:'
            for formal in value["formals"].formals[::-1]:
                variableTable[METHOD_PARAM_KEY] = {
                    'variableName': formal.variable,
                    'variableKind': 'formal',
                    'variableType': formal.type
                }
                METHOD_PARAM_KEY += 1
            GLOBAL_METHOD_VARIABLE_TABLE.append(variableTable)
            block_string_representation = str(value['block'])
            for variableTable in GLOBAL_METHOD_VARIABLE_TABLE:
                for key, stuff in variableTable.items():
                    variable_result = variable_result + f'VARIABLE {key}, {stuff["variableName"]}, {stuff["variableKind"]}, {stuff["variableType"]}\n'
                    methodParamsId.append(key)

            method_result = f'{method_result} {str(methodParamsId)[1:-1]}\n{variable_result}Method Body:\n{block_string_representation}\n'
            GLOBAL_METHOD_VARIABLE_TABLE = []
# ============================================================================================

        return f'Class Name: {self.className}\nSuperclass Name: {self.superClassName}\n{field_result}{constructor_result}{method_result}'
    
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
        
        # result = ''
        for variable in self.fieldVarDecl.variable_list.vars[::-1]:
            FIELD_DICTIONARY[FIELD_KEY] = {
                'className': CLASS_NAME,
                'variableName': variable,
                'fieldModifier': str(self.fieldModifier),
                'type': str(self.fieldVarDecl.type)
            }
            # result = result + f'FIELD {FIELD_KEY}, {variable}, {CLASS_NAME}, {str(self.fieldModifier)}, {str(self.fieldVarDecl.type)}\n' 
            FIELD_KEY += 1

class Constructor_Decl(Node):
    def __init__(self, modifier, constructorName, formals, block):
        super().__init__()
        self.modifier = modifier
        self.constructorName = constructorName
        self.formals = formals
        self.block = block

        global CONSTRUCTOR_KEY, CONSTRUCTOR_BLOCK, METHOD_BLOCK
        CONSTRUCTOR_BLOCK = True
        METHOD_BLOCK = False

        CONSTRUCTOR_DICTIONARY[CONSTRUCTOR_KEY] = {
            'modifier': self.modifier,
            'constructorName': self.constructorName,
            'formals': self.formals,
            'block': self.block
        }
        CONSTRUCTOR_KEY += 1
    
class Method_Decl(Node):
    def __init__(self, modifier, type, id, formals, block):
        super().__init__()
        self.modifier = modifier
        self.methodName = id
        self.type = type
        self.formals = formals
        self.block = block
        global METHOD_KEY, METHOD_BLOCK, CONSTRUCTOR_BLOCK
        CONSTRUCTOR_BLOCK = False
        METHOD_BLOCK = True

        METHOD_DICTIONARY[METHOD_KEY] = {
            'methodName': self.methodName,
            'modifier': self.modifier,
            'formals': self.formals,
            'type': self.type,
            'block': self.block
        }
        METHOD_KEY += 1

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
    
class Var_Decl(Node):
    def __init__(self, type, variable_list):
        super().__init__()
        self.type = type
        self.variable_list = variable_list
    
class Variables_cont(Node):
    def __init__(self):
        super().__init__()
        self.vars = []
    
class Formals_const(Node):
    def __init__(self):
        super().__init__()
        self.formals = []
    
class Formal_param(Node):
    def __init__(self, type, variable):
        super().__init__()
        self.type = type
        self.variable = variable

class Block(Node):
    def __init__(self, stmtList):
        super().__init__()
        self.stmtList = stmtList
    def __str__(self):
        global CONSTRUCTOR_PARAM_KEY, METHOD_KEY, METHOD_BLOCK, CONSTRUCTOR_BLOCK, VAR_DECL_AVALIABILITY, GLOBAL_METHOD_VARIABLE_TABLE, GLOBAL_CONSTRUCTOR_VARIABLE_TABLE
        currentKey = 0
        if METHOD_BLOCK:
            currentKey = METHOD_PARAM_KEY
        else:
            currentKey = CONSTRUCTOR_PARAM_KEY
        variableTable = {}
        result = 'Block([\n'
        prevStmt = None
        add_var_decl_status = True
        for stmt in self.stmtList.stmts[::-1]:
            # print(type(stmt))
            if (not isinstance(stmt, Var_Decl) and add_var_decl_status):
                add_var_decl_status = False
                if METHOD_BLOCK:
                    GLOBAL_METHOD_VARIABLE_TABLE.append(variableTable)
                else:
                    GLOBAL_CONSTRUCTOR_VARIABLE_TABLE.append(variableTable)
            if (isinstance(stmt, Var_Decl)):
                if (not isinstance(prevStmt, Var_Decl) and prevStmt != None):
                    print("we have a problem, why are you adding another variable decl")
                    sys.exit()
                for variable in stmt.variable_list.vars[::-1]:
                    variableTable[currentKey] = {
                        'variableName': variable,
                        'variableKind': 'local',
                        'variableType': stmt.type,
                    }
                    currentKey += 1

            elif (stmt == ';'):
                result += "Skip-stmt()\n"
            elif (isinstance(stmt, Block)):
                pass
            elif (stmt == 'continue'):
                result += "Continue-stmt()\n"
            elif (stmt == 'break'):
                result += "Break-stmt()\n"
            elif (isinstance(stmt, Auto)):
                result += str(stmt)
            elif (isinstance(stmt, Assign)):
                result += str(stmt)
            elif (isinstance(stmt, Return)):
                result += str(stmt)
            elif (isinstance(stmt, For_decl)):
                result += str(stmt)
            elif (isinstance(stmt, Method_Invocation)):
                result += str(stmt)
            prevStmt = stmt
        return result + "\n])"

class Stmt_List(Node):
    def __init__(self):
        super().__init__()
        self.stmts = []

class Auto(Node):
    def __init__(self, post = None, pre = None, lhs = None):
        super().__init__()
        self.post = post
        self.pre = pre
        self.lhs = lhs
    def __str__(self):
        if (self.pre == "++"):
            return f'Auto-expr({self.lhs}, auto-increment, pre) '
        elif (self.pre == "--"):
            return f'Auto-expr({self.lhs}, auto-decrement, pre) '
        elif (self.post == "++"):
            return f'Auto-expr({self.lhs}, auto-increment, post) '
        elif (self.post == "--"):
            return f'Auto-expr({self.lhs}, auto-decrement, post) '

class Assign(Node):
    def __init__(self, lhs = None, expr = None):
        super().__init__()
        self.lhs = lhs
        self.expr = expr
    def __str__(self):
        return f'Assign-expr({str(self.lhs)}, {str(self.expr)}) '

class Field_Access(Node):
    def __init__(self, primary, id):
        super().__init__()
        self.primary = primary
        self.id = id
    def __str__(self):
        return f'Field-access({self.primary}, {self.id})'
    
class Return(Node):
    def __init__(self, return_val):
        super().__init__()
        self.return_val = return_val
    def __str__(self):
        return f'Return-stmt({str(self.return_val)})'
    
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

class Variable(Node):
    def __init__(self, variable_name):
        super().__init__()
        self.variable_name = variable_name
    def __str__(self):
        return str(self.variable_name)