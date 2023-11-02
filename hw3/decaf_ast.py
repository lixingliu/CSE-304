class_body = dict()

FIELD_COUNTER = 0
CONSTRUCTOR_COUNTER = 0
METHOD_COUNTER = 0

def create_body(stmt):
    if type(stmt) == type(Stmt(None, None)):
        return f"{stmt.type}({stmt.component})"
    if type(stmt) == type(Ifelsewhile_stmt(None, None, None, None)):
        if_body_stuff = ""
        else_body_stuff = ""
        for if_stuff in stmt.then.stmt_list.things[::-1]:
            if_body_stuff = if_body_stuff + create_body(if_stuff)
        for else_stuff in stmt.els.stmt_list.things[::-1]:
            else_body_stuff = else_body_stuff + create_body(else_stuff)
        
        result = f"{stmt.type}({stmt.cond}) Block ([\n{if_body_stuff}])"

        if else_body_stuff != "":
            return result + f" {stmt.type_2} Block ([\n{create_body(else_stuff)}])"
        else:
            return result

    return "hi"
    
        # return str(stmt.)
# def inner_block_creator(inner_block):
#     result = ""
#     if type(inner_block) == type([]):
#         print("type list")
#         if len(inner_block) == 1:
#             print("list length one")
#             if type(inner_block[0]) == type(Ifelsewhile_stmt(None, None, None, None)):
#                 print("list length one if else")
#                 then_else = inner_block_creator(inner_block[0].then.stmt_list.things[::-1])
#                 return f"Block ([\n{str(inner_block[0].type)}({str(inner_block[0].cond)}) {then_else}])"
#             return f"Block ([\n{inner_block[0].type} ({inner_block[0].component}])"
#         elif len(inner_block) > 1:
#             print("greater than 1")
#             block_stuff = ""
#             print(len(inner_block))
#             for stuff in inner_block:
#                 print("greater than 1 check all contents")
#                 print(type(stuff))
#                 block_stuff = block_stuff + inner_block_creator(stuff)
#             result = f"Blockkkk ([\n{block_stuff}])"
#             return result
#         else:
#             return 'nothing'
#     if type(inner_block) == type(Ifelsewhile_stmt(None, None, None, None)):
#         print("not list but type if else")
#         print(len(inner_block.then.stmt_list.things))
#         for thing in inner_block.then.stmt_list.things[::-1]:
#             print(type(thing))
#             if (type.thing == type(Stmt(None, None))){
                
#             }
#             print("type if else not list inside stuff")
#             print(result)
#             then_else = inner_block_creator(thing)
#             print("line 37")
#             print(then_else)
#             result = result + f"{str(inner_block.type)}({str(inner_block.cond)}) Blockqqq ([\n{then_else} ]) "
#             print("ppp")
#             print(result)
#             print("GGG")
#         return result
#     if type(inner_block) == type(Stmt(None, None)):
#         print("stmt")
#         return f"{inner_block.type} ({inner_block.component})"
#     return result

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
        #In class intialization
        pub_sta_mod = Modifier("public", "static")
        scan_int = Method_decl("scan_int", pub_sta_mod, Type("int"), Formals(Formals_cont()), Stmt_list()) #Initializing scan_int
        scan_float = Method_decl("scan_float", pub_sta_mod, Type("float"), Formals(Formals_cont()), Stmt_list()) #Initializing scan_float
        class_in_body_decl = Class_body_decl()
        class_in_body_decl.things.append(scan_int)
        class_in_body_decl.things.append(scan_float)
        class_in = Class_decl("In", "", class_in_body_decl)

        #Out class intialization
        print_int_formal_cont = Formals_cont()
        print_int_formal_cont.things.append(Formal_param(Type("int"), Variable("i")))
        print_int_formal = Formals(print_int_formal_cont)
        print_int = Method_decl("print", pub_sta_mod, None, print_int_formal, Stmt_list()) #Initializing print_int

        print_float_formal_cont = Formals_cont()
        print_float_formal_cont.things.append(Formal_param(Type("float"), Variable("f")))
        print_float_formal = Formals(print_float_formal_cont)
        print_float = Method_decl("print", pub_sta_mod, None, print_float_formal, Stmt_list()) #Initializing print_float

        print_boolean_formal_cont = Formals_cont()
        print_boolean_formal_cont.things.append(Formal_param(Type("boolean"), Variable("b")))
        print_boolean_formal = Formals(print_boolean_formal_cont)
        print_boolean = Method_decl("print", pub_sta_mod, None, print_boolean_formal, Stmt_list()) #Initializing print_boolean

        print_string_formal_cont = Formals_cont()
        print_string_formal_cont.things.append(Formal_param(Type("string"), Variable("s")))
        print_string_formal = Formals(print_string_formal_cont)
        print_string = Method_decl("print", pub_sta_mod, None, print_string_formal, Stmt_list()) #Initializing print_string

        class_out_body_decl = Class_body_decl()
        class_out_body_decl.things.append(print_int)
        class_out_body_decl.things.append(print_float)
        class_out_body_decl.things.append(print_boolean)
        class_out_body_decl.things.append(print_string)
        class_out = Class_decl("Out", "", class_out_body_decl) #Append the four methods to Out's class_body_decl

        self.classes.append(class_in)
        self.classes.append(class_out) #Append predefined In and Out class to class table

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
                    if (len(stuff.formals.formal_param) != 0):
                        for constructor_stuff in stuff.formals.formal_param.things[::-1]:
                            constructor_param_list_counter = constructor_param_list_counter + 1
                            constructor_param_list.append(constructor_param_list_counter)
                            variable_table = variable_table + f"\nVARIABLE {constructor_param_list_counter}, {constructor_stuff.variable.variable_name}, ?, {constructor_stuff.type.type_value}"

                    # then_else = inner_block_creator(stuff.body.stmt_list.things[::-1])
                    # constructor_body = "\n" + constructor_body + then_else

                    # body_items = []
                    # for constructor_stmt in stuff.body.stmt_list.things[::-1]:
                    #     then_else = block_creator(constructor_stmt)
                    #     body_items.append(then_else)
                    #     string_body_items = str(body_items).strip('[]\'')
                    # constructor_body = f"\nBlock ([\n{string_body_items}\n])"

                    # for constructor_stmt in stuff.body.stmt_list.things[::-1]:
                    #     then_else = inner_block_creator(constructor_stmt)
                    #     constructor_body = "\n" + constructor_body + then_else

                        # if(type(constructor_stmt) == type(Ifelsewhile_stmt(None, None, None))):   
                        #     print("aaa")                            
                        #     then_else = inner_block_creator(constructor_stmt)
                        #     constructor_body = "\n" + then_else
                        # if(type(constructor_stmt) == type(Stmt(None, None))):
                        #     if(constructor_stmt.type != None):
                        #         constructor_body = constructor_body + f"\nBlock ([\n{str(constructor_stmt.type)}({str(constructor_stmt.component)})\n)]"

                        # if(type(constructor_stmt) == type(Var_decl(None))):
                        #     constructor_body = constructor_body + f"\n{str(constructor_stmt.type)}( {str(constructor_stmt.variables)} ),"
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
    def __init__(self, cond1, cond2, cond3, body):
        super().__init__()
        self.cond1 = cond1
        self.cond2 = cond2
        self.cond3 = cond3
        self.then = body
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