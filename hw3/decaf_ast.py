class_body = dict()

FIELD_COUNTER = 0
CONSTRUCTOR_COUNTER = 0
METHOD_COUNTER = 0

def create_body(stmt):
    print(type(stmt))
    if type(stmt) == type(Stmt(None, None)):
        return f"{stmt.type}({stmt.component})"
    if type(stmt) == type(Ifelsewhile_stmt(None, None, None, None)):
        if_body_stuff = ""
        else_body_stuff = ""
        for if_stuff in stmt.then.stmt_list.things[::-1]:
            if_body_stuff = if_body_stuff + create_body(if_stuff)
        if stmt.els != "":
            for else_stuff in stmt.els.stmt_list.things[::-1]:
                else_body_stuff = else_body_stuff + create_body(else_stuff)
        
        result = f"{stmt.type}({stmt.cond}) Block ([\n{if_body_stuff}])"

        if else_body_stuff != "":
            return result + f" {stmt.type_2} Block ([\n{create_body(else_stuff)}])"
        else:
            return result
    if type(stmt) == type(For_stmt(None, None, None, None, None)):
        for_body_stuff = ""
        for for_stuff in stmt.then.stmt_list.things[::-1]:
            print(type(for_stuff))
            for_body_stuff = for_body_stuff + create_body(for_stuff)
        result = f"{stmt.type}({stmt.cond1}, {stmt.cond2}, {stmt.cond3}) Block ([\n{for_body_stuff}])"
        return result
        
    if type(stmt) == type(""):
        return stmt

    return "hi"

def block_creator(block):
    print(type(block))
    if (type(block)) == type(Ifelsewhile_stmt(None, None, None)):
        return f"Block ([{str(block.type)}({str(block.cond)}) L ]) "
    if (type(block)) == type(Stmt(None, None)):
        return f"Block ([{block.type} ({block.component}) ]) "

    return "hi"

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
        
    def __str__(self):
        res = ""
        for thing in self.classes[::-1]:
            field = ""
            constructor = ""
            method = ""
            for stuff in thing.class_body_decl.things:
                if type(stuff) == type(Constructor_decl(None, None, None)):
                    global CONSTRUCTOR_COUNTER
                    CONSTRUCTOR_COUNTER = CONSTRUCTOR_COUNTER + 1

                    constructor_param_list = []
                    constructor_param_list_counter = 0
                    variable_table = ""
                    constructor_body = ""
                    if (hasattr(stuff.formals.formal_param, "things")):
                        for constructor_stuff in stuff.formals.formal_param.things[::-1]:
                            constructor_param_list_counter = constructor_param_list_counter + 1
                            constructor_param_list.append(constructor_param_list_counter)
                            variable_table = variable_table + f"\nVARIABLE {constructor_param_list_counter}, {constructor_stuff.variable.variable_name}, ?, {constructor_stuff.type.type_value}"

                    constructor_body_stuff = ""
                    for constructor_stmt in stuff.body.stmt_list.things[::-1]:
                        constructor_body_stuff = constructor_body_stuff + create_body(constructor_stmt)
                    
                    constructor_body = f"\nBlock ([\n{constructor_body_stuff}])"
                    constructor = constructor + f"\nCONSTRUCTOR {CONSTRUCTOR_COUNTER}, {str(stuff.modifier.visibility)}"
                    constructor = constructor + f"\nConstructor Parameters: {str(constructor_param_list).strip('[]')}"
                    constructor = constructor + f"\nVariable Table: {variable_table}"
                    constructor = constructor + f"\nConstructor Body: {constructor_body}"

                if type(stuff) == type(Field_decl(None, None)):
                    for field_stuff in stuff.var_decl.variables.variable.things[::-1]:
                        global FIELD_COUNTER
                        FIELD_COUNTER = FIELD_COUNTER + 1
                        field = field + f"\nFIELD {FIELD_COUNTER}, {str(field_stuff.variable_name)}, {str(thing.class_name)}, {str(stuff.modifier.visibility)}, {str(stuff.modifier.applicability)}, {str(stuff.var_decl.type.type_value)}"

                if type(stuff) == type(Method_decl(None, None, None, None, None)):
                    global METHOD_COUNTER
                    METHOD_COUNTER = METHOD_COUNTER + 1
                    
                    method_param_list = []
                    method_param_list_counter = 0
                    variable_table = ""
                    method_body = ""
                    for method_stuff in stuff.formals.formal_param.things[::-1]:
                        method_param_list_counter = method_param_list_counter + 1
                        method_param_list.append(method_param_list_counter)
                        variable_table = variable_table + f"\nVARIABLE {method_param_list_counter}, {method_stuff.variable.variable_name}, ?, {method_stuff.type.type_value}"
                    
                    for method_stmt in stuff.body.things[::-1]:
                        if(type(method_stmt) == type(Ifelsewhile_stmt(None, None, None))):
                            method_body = method_body + f"\n{str(method_stmt.type)}( {str(method_stmt.cond)}, {str(method_stmt.then)}, {str(method_stmt.els)} ),"
                        if(type(method_stmt) == type(For_stmt(None, None, None))):
                            method_body = method_body + f"\nFor( {str(method_stmt.cond1)}, {str(method_stmt.cond2)}, {str(method_stmt.cond3)},  {str(method_stmt.body)}),"
                        if(type(method_stmt) == type(Stmt(None, None))):
                            if(method_stmt.type != None):
                                method_body = method_body + f"\n{str(method_stmt.type)}( {str(method_stmt.component)} ),"
                        #stmt_expr ->
                        if(type(method_stmt) == type(Var_decl(None))):
                            method_body = method_body + f"\n{str(method_stmt.type)}( {str(method_stmt.variables)} ),"
                   
                    method = method + f"\nMETHOD: {METHOD_COUNTER}, {str(stuff.method_name)}, {str(thing.class_name)}, {str(stuff.modifier.visibility)}, {str(stuff.modifier.applicability)}, {str(stuff.type)}"
                    method = method + f"\nMethod Parameters: {str(method_param_list).strip('[]')}"
                    method = method + f"\nVariable Table:  {variable_table}"
                    method = method + f"\nMethod Body:   {method_body[:-1]}"
                    

            res = res +f"\nClass Name: {str(thing.class_name)}"
            res = res + f"\nSuperclass Name: {str(thing.superclass_name)}"
            res = res + "\nFields:"
            res = res + field
            res = res + f"\nConstructors: "
            res = res + constructor
            res = res + f"\nMethods: "
            res = res + method 
            res = res + "\n--------------------------------------------------------------------------"
        return res

class Class_decl_list(Node):
    def __init__(self):
        self.things = []
    def __str__(self):
        pass

class Class_decl(Node):
    def __init__(self, class_name, superclass_name, class_body_decl):
        super().__init__()
        self.class_name = class_name
        self.superclass_name = superclass_name
        self.class_body_decl = class_body_decl
    def __str__(self):
        pass

class Class_body_decl(Node):
    def __init__(self):
        super().__init__()
        self.things = []
    def __str__(self):
        pass
    
class Field_decl(Node):
    def __init__(self, modifier, var_decl):
        super().__init__()
        self.modifier = modifier
        self.var_decl = var_decl
    def __str__(self):
        pass
    
class Modifier(Node):
    def __init__(self, visibility, applicability):
        super().__init__()
        self.visibility = visibility
        self.applicability = applicability
        if self.applicability == "static":
            self.applicability = "class"
        else:
            self.applicability = "instance"
    def __str__(self):
        return str(self.visibility) + str(self.applicability)

class Var_decl(Node):
    def __init__(self, type, variables):
        super().__init__()
        self.type = type
        self.variables = variables
    def __str__(self):
        pass
    
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

class Variables(Node):
    def __init__(self, variable):
        super().__init__()
        self.variable = variable
    def __str__(self):
        pass

class Variable(Node):
    def __init__(self, variable_name):
        super().__init__()
        self.variable_name = variable_name
    def __str__(self):
        return str(self.variable_name)        

class Variables_cont(Node):
    def __init__(self):
        super().__init__()
        self.things = []
    def __str__(self):
        pass

class Constructor_decl(Node):
    def __init__(self, modifier, formals, body):
        super().__init__()
        self.modifier = modifier
        self.formals = formals
        self.body = body
    def __str__(self):
        pass

class Formals(Node):
    def __init__(self, formal_param):
        super().__init__()
        if formal_param == None:
            self.formal_param = []
        else:
            self.formal_param = formal_param
    def __str__(self):
        pass

class Formals_cont(Node):
    def __init__(self):
        super().__init__()
        self.things = []
    def __str__(self):
        pass

class Formal_param(Node):
    def __init__(self, type, variable):
        super().__init__()
        self.type = type
        self.variable = variable
    def __str__(self):
        pass
        
class Method_decl(Node):
    def __init__(self, method_name, modifier, type, formals, body):
        super().__init__()
        self.method_name = method_name
        self.modifier = modifier
        self.type = type
        self.formals = formals
        self.body = body
    def __str__(self):
        pass

class Block(Node):
    def __init__(self, stmt_list):
        super().__init__()
        self.stmt_list = stmt_list
    def __str__(self):
        pass

class Stmt_list(Node):
    def __init__(self):
        super().__init__()
        self.things = []
    def __str__(self):
        pass

class Stmt(Node):
    def __init__(self, type, component = ''):
        super().__init__()
        self.type = type
        if component == None:
            self.component = ''
        else:
            self.component = component
    def __str__(self):
        pass

class Ifelsewhile_stmt(Node):
    def __init__(self, type, cond, then, els = '', type_2 = ''):
        super().__init__()
        self.type = type
        self.cond = cond
        self.then = then
        self.els = els
        self.type_2 = type_2
    def __str__(self):
        pass

class For_stmt(Node):
    def __init__(self, cond1, cond2, cond3, body, type):
        super().__init__()
        self.cond1 = cond1
        self.cond2 = cond2
        self.cond3 = cond3
        self.then = body
        self.type = type
    def __str__(self):
        pass
    
class Arguments(Node):
    def __init__(self,  arguments):
        super().__init__()
        self.arguments = arguments
    def __str__(self):
        pass
class Arguments_cont(Node):
    def __init__(self):
        super().__init__()
        self.things = []
    def __str__(self):
        pass