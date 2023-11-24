import sys
class_body = dict()

FIELD_COUNTER = 0
CONSTRUCTOR_COUNTER = 0
METHOD_COUNTER = 0

def create_in_class():
    pub_sta_mod = Modifier("public", "static")
    scan_int = Method_decl("scan_int", pub_sta_mod, Type("int"), Formals(Formals_cont()), Stmt_list()) #Initializing scan_int
    scan_float = Method_decl("scan_float", pub_sta_mod, Type("float"), Formals(Formals_cont()), Stmt_list()) #Initializing scan_float
    class_in_body_decl = Class_body_decl()
    class_in_body_decl.things.append(scan_int)
    class_in_body_decl.things.append(scan_float)
    class_in = Class_decl("In", "", class_in_body_decl) #Append the two methods to In's class_body_decl
    return class_in

def create_out_class():
    pub_sta_mod = Modifier("public", "static")
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
    return class_out

def create_constructor(line):
    global CONSTRUCTOR_COUNTER
    CONSTRUCTOR_COUNTER = CONSTRUCTOR_COUNTER + 1
    constructor = ""

    constructor_parameters_counter = 0
    variable_table = ""
    constructor_body = ""
    constructor_body_stuff = ""
    constructor_parameters = []

    if (hasattr(line.formals.formal_param, "things")):
        constructor_parameters = []
        for constructor_stuff in line.formals.formal_param.things[::-1]:
            #Fixed
            if(constructor_stuff.variable.variable_name in constructor_parameters): #If param name already exist in list of params, throw error
                print("Error: constructor variable name not unique")
                sys.exit()
            constructor_parameters.append(constructor_stuff.variable.variable_name) 
            constructor_parameters_counter = constructor_parameters_counter + 1
            variable_table = variable_table + f"\nVARIABLE {constructor_parameters_counter}, {constructor_stuff.variable.variable_name}, formal, {constructor_stuff.type.type_value}"

    for constructor_stmt in line.body.stmt_list.things[::-1]:
        outcome = create_body(constructor_stmt, variable_table, constructor_parameters_counter)
        constructor_body_stuff = constructor_body_stuff + outcome[0]
        variable_table = outcome[1]
        #constructor_parameters_counter = outcome[2]
    
    constructor_body = f"\nBlock([\n{constructor_body_stuff}\n])"
    constructor = constructor + f"\nCONSTRUCTOR: {CONSTRUCTOR_COUNTER}, {str(line.modifier.visibility)}"
    if constructor_parameters_counter == 0:
        constructor_parameters_counter = ""
    constructor = constructor + f"\nConstructor Parameters: {constructor_parameters_counter}"
    constructor = constructor + f"\nVariable Table: {variable_table}"
    constructor = constructor + f"\nConstructor Body: {constructor_body}"

    return constructor

def create_field(line, class_object, field_name_list):
    field = ""
    for field_stuff in line.var_decl.variables.variable.things[::-1]:
        #li fixed
        global FIELD_COUNTER
        if (field_stuff.variable_name in field_name_list): #If field name is not unique, throw error
            print("Error: field name not unique")
            sys.exit()
        field_name_list.append(field_stuff.variable_name) #Add field name to list
        FIELD_COUNTER = FIELD_COUNTER + 1
        field = field + f"\nFIELD {FIELD_COUNTER}, {str(field_stuff.variable_name)}, {str(class_object.class_name)}, {str(line.modifier.visibility)}, {str(line.modifier.applicability)}, {str(line.var_decl.type.type_value)}"

    return field, field_name_list

def create_method(line, class_object, method_var_name_list):
    method = ""
    global METHOD_COUNTER
    METHOD_COUNTER = METHOD_COUNTER + 1
    method_param_list_counter = 0
    variable_table = ""
    method_body = ""
    if (hasattr(line.formals.formal_param, "things")):
        for method_stuff in line.formals.formal_param.things[::-1]:
            #Fixed
            if(method_stuff.variable.variable_name in method_var_name_list): #If var name is not unique, throw error
                print("Error: method variable name not unique")
                sys.exit()
            method_var_name_list.append(method_stuff.variable.variable_name) #Add var name to list
            method_param_list_counter = method_param_list_counter + 1
            variable_table = variable_table + f"\nVARIABLE {method_param_list_counter}, {method_stuff.variable.variable_name}, formal, {method_stuff.type.type_value}"

    method_body_stuff = ""
    for method_stmt in line.body.stmt_list.things[::-1]:
        outcome = create_body(method_stmt, variable_table, method_param_list_counter)
        variable_table = outcome[1]
        #method_param_list_counter = outcome[2]
        method_body_stuff = method_body_stuff + outcome[0]

    method_body = f"\nBlock([\n{method_body_stuff}\n])"
    method = method + f"\nMETHOD: {METHOD_COUNTER}, {str(line.method_name)}, {str(class_object.class_name)}, {str(line.modifier.visibility)}, {str(line.modifier.applicability)}, {str(line.type)}"
    if method_param_list_counter == 0:
        method_param_list_counter = ""
    method = method + f"\nMethod Parameters: {method_param_list_counter}"
    method = method + f"\nVariable Table:  {variable_table}"
    method = method + f"\nMethod Body:   {method_body}"
    
    return method, method_var_name_list

def create_body(stmt, variable_table, constructor_param_list_counter):
    if isinstance(stmt, NewObject):
        return [str(stmt), variable_table, constructor_param_list_counter]

    if isinstance(stmt, Paren):
        return create_body(stmt.expr, variable_table, constructor_param_list_counter)
    
    if stmt is None:
        return ["Skip-stmt, ", variable_table, constructor_param_list_counter]
    
    if isinstance(stmt, Stmt):
        result = create_body(stmt.component, variable_table, constructor_param_list_counter)
        if stmt.type == 'return' and isinstance(stmt.component, Field_access):
            result[0] = f"{stmt.type}( {result[0]} )"
            return result

        outcome = result
        outcome[0] = f"{stmt.type}( {result[0]} )"
        return outcome
    
    if isinstance(stmt, Ifelsewhile_stmt):
        if_body_stuff = ""
        else_body_stuff = ""
        outcome = [None, variable_table, constructor_param_list_counter]
        for if_stuff in stmt.then.stmt_list.things[::-1]:
            outcome = create_body(if_stuff, outcome[1], outcome[2])
            if_body_stuff = if_body_stuff + outcome[0]
            
        if stmt.els:
            for else_stuff in stmt.els.stmt_list.things[::-1]:
                outcome = create_body(else_stuff, variable_table, constructor_param_list_counter)
                else_body_stuff = else_body_stuff + outcome[0]

        if_condition = create_body(stmt.cond, outcome[1], outcome[2])
        outcome = [f"{stmt.type}({if_condition[0]}) Block ([\n{if_body_stuff}\n]) else", outcome[1], outcome[2]]

        if else_body_stuff == '':
            else_body_stuff = "Skip-stmt"

        if else_body_stuff != "":
            outcome[0] += f" Block ([\n{else_body_stuff} \n])"

        return outcome
    
    if isinstance(stmt, For_stmt):
        for_body_stuff = ""
        outcome = [None, variable_table, constructor_param_list_counter]
        for for_stuff in stmt.then.stmt_list.things[::-1]:
            outcome = create_body(for_stuff, outcome[1], outcome[2])
            if outcome[0] == 'empty( Skip-stmt )':
                for_body_stuff = 'Skip-stmt'
                break
            for_body_stuff = for_body_stuff + outcome[0]
            
        for_cond_1 = create_body(stmt.cond1, outcome[1], outcome[2])
        outcome[1] = for_cond_1[1]
        outcome[2] = for_cond_1[2]

        for_cond_2 = create_body(stmt.cond2, outcome[1], outcome[2])
        outcome[1] = for_cond_2[1]
        outcome[2] = for_cond_2[2]    

        for_cond_3 = create_body(stmt.cond3, outcome[1], outcome[2])
        outcome[1] = for_cond_3[1]
        outcome[2] = for_cond_3[2]

        outcome[0] = f"{stmt.type}-stmt({for_cond_1[0]}{for_cond_2[0]}, {for_cond_3[0]}) Block ([\n{for_body_stuff}\n])\n"
        return outcome
    
    if isinstance(stmt, Auto):
        find_indices = lambda strings, substring: next((int(s.split(",")[0].split(" ")[1]) for i, s in enumerate(strings) if substring in s), None)
        variable_value = f", {stmt.lhs.id},"
        variable_number = find_indices(variable_table.split("\n")[::-1], variable_value)


        if variable_number is not None:
            if (stmt.pre == "++"):
                return [f"Expr(Auto(Variable({variable_number}), inc, pre) ), ", variable_table, constructor_param_list_counter]
            elif (stmt.pre == "--"):
                return [f"Expr(Auto(Variable({variable_number}), dec, pre) ), ", variable_table, constructor_param_list_counter]
            elif (stmt.post == "++"):
                return [f"Expr(Auto(Variable({variable_number}), inc, post) ), ", variable_table, constructor_param_list_counter]
            elif (stmt.post == "--"):
                return [f"Expr(Auto(Variable({variable_number}), dec, post) ), ", variable_table, constructor_param_list_counter]
        return "AAAA"
    
    if isinstance(stmt, Var_decl):
        #constructor_param_list_counter +=  1
        vars = variable_table.split("\n")
        for var_str in vars:
            parts = var_str.split(', ')
            if len(parts) >= 2 and parts[1] == stmt.variables.variable.things[0].variable_name:
                print("Error: Local variable name not unique")
                sys.exit()
        variable_table +=  f"\nVARIABLE {constructor_param_list_counter}, {stmt.variables.variable.things[0].variable_name}, local, {stmt.type.type_value}"
        return ['', variable_table, constructor_param_list_counter]
    
    if isinstance(stmt, Assign):
        left = ""
        right = ""
        if stmt.lhs.type == ".":
            left = f"Field-access({stmt.lhs.primary}, {stmt.lhs.id})"
        elif stmt.lhs.type is None:
            find_indices = lambda strings, substring: next((int(s.split(",")[0].split(" ")[1]) for i, s in enumerate(strings) if substring in s), None)
            variable_value = f", {stmt.lhs.id},"
            variable_number = find_indices(variable_table.split("\n")[::-1], variable_value)
            if variable_number is not None:
                left = f"Variable({variable_number})"
            else:
                return ["Variable not found", variable_table, constructor_param_list_counter] #here


        right = create_body(stmt.expr, variable_table, constructor_param_list_counter)
        variable_table = right[1]
        constructor_param_list_counter = right[2]

        result = f"Expr( Assign({left}, {right[0]}) ), "
        outcome = [result, variable_table, constructor_param_list_counter]

        return outcome
    
    if stmt == "true":
        return [f"Constant({True})", variable_table, constructor_param_list_counter]
    if stmt == "false":
        return [f"Constant({False})", variable_table, constructor_param_list_counter]
    if stmt == "null":
        return [f"Constant(Null)", variable_table, constructor_param_list_counter]
    
    if isinstance(stmt, Uminus):
        outcome = create_body(stmt.expr, variable_table, constructor_param_list_counter)
        result = f"Unary-expression(MINUS, {outcome[0]})"
        return [result, outcome[1], outcome[2]]
    
    if isinstance(stmt, Field_access):
        outcome  = None
        if isinstance(stmt.primary, Field_access):
            outcome = create_body(stmt.primary, variable_table, constructor_param_list_counter)
            stmt.primary = outcome[0]
            variable_table = outcome[1]
            constructor_param_list_counter = outcome[2]
        if stmt.primary is None:
            variable_value = f", {stmt.id},"
            variable_number = next((i for i, s in enumerate(variable_table.split("\n")) if variable_value in s), None)

            if variable_number is not None:
                return [f"Variable({variable_number})", variable_table, constructor_param_list_counter]
            
        return[f"Field-access({stmt.primary}, {stmt.id})", variable_table, constructor_param_list_counter]
    
    
    if isinstance(stmt, float):
        return [f"Constant(Float-constant({stmt}))", variable_table, constructor_param_list_counter]
    if isinstance(stmt, int):
        return [f"Constant(Integer-constant({stmt}))", variable_table, constructor_param_list_counter]
    if isinstance(stmt, str):
        if stmt == 'empty':
            return ["Skip-stmt", variable_table, constructor_param_list_counter]
        return [f"Constant(String-constant({stmt}))", variable_table, constructor_param_list_counter]

    binary_expr_map = {
        "Addition": "add",
        "Subtraction": "sub",
        "Multiplication": "mul",
        "Division": "div",
        "Conjection": "and",
        "Disjunction": "or",
        "Equality": "eq",
        "Disquality": "neq",
        "LessThan": "lt",
        "LessThanEqual": "leq",
        "GreaterThan": "gt",
        "GreaterThanEqual": "geq",
    }
    for expr_type, operation in binary_expr_map.items():
        if isinstance(stmt, globals()[expr_type]):
            outcome_1 = create_body(stmt.left_expr, variable_table, constructor_param_list_counter)
            outcome_2 = create_body(stmt.right_expr, outcome_1[1], outcome_1[2])
            outcome_3 = [f"Binary({operation}, {outcome_1[0]}, {outcome_2[0]})", outcome_2[1], outcome_2[2]]
            return outcome_3
        
    if isinstance(stmt, Method_invocation):
        argument_list = []
        if stmt.argument_list.arguments is not None:
            find_indices = lambda strings, substring: next((int(s.split(",")[0].split(" ")[1]) for i, s in enumerate(strings) if substring in s), None)
            for argument in stmt.argument_list.arguments.things:
                variable_value = f", {argument.id},"
                variable_number = find_indices(variable_table.split("\n")[::-1], variable_value)
                if variable_number is not None:
                    argument_list.append(f"Variable({variable_number})")            
        if hasattr(stmt.field_access.primary, "id"):
            result = f"Method-call(Class-reference({stmt.field_access.primary.id}), {stmt.field_access.id}, [{str(argument_list).strip('[]')}])"
        else:
            result = f"Method-call({stmt.field_access.primary}, {stmt.field_access.id}, [{str(argument_list).strip('[]')}])"
        outcome = [result, variable_table, constructor_param_list_counter]
        return outcome
    
    # if isinstance(stmt, Block):
    #     outcome = ['', variable_table, constructor_param_list_counter]
    #     temp_variable_table = ''
    #     previous_variable_table = ''
    #     for element in stmt.stmt_list.things[::-1]:
    #         if isinstance(element, Block):
    #             temp_variable_table = ''
    #         if not isinstance(element, Var_decl) and temp_variable_table == '':
    #             temp_variable_table = outcome[1]
    #         result = create_body(element, temp_variable_table, outcome[2])
    #         outcome[0] += result[0]

    #         if temp_variable_table != result[1]:
    #             outcome[1] += result[1]  # Append the changes to outcome[1]

    #         temp_variable_table = result[1]
    #         outcome[2] = result[2]
    #     outcome[0] = f'Block([\n{outcome[0]}\n])'
    #     return outcome

    if isinstance(stmt, Block):
        outcome = ['', variable_table, constructor_param_list_counter]
        for element in stmt.stmt_list.things[::-1]:
            result = create_body(element, outcome[1], outcome[2])
            outcome[0] += result[0]
            outcome[1] = result[1]
            outcome[2] = result[2]
            
        outcome[0] = f'Block([\n{outcome[0]}\n])'
        return outcome
    outcome = [None, None, None]
    return outcome
    

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
        self.classes.append(create_in_class())
        self.classes.append(create_out_class())

        class_name_list = []
        for class_object in self.classes[::-1]:
            if (class_object.class_name == 'Out' or class_object.class_name == 'In'):
                continue
            elif (class_object.class_name in class_name_list): #If class name is not unique, throw error
                return "Error: Class name not unique"
            class_name_list.append(class_object.class_name) #Add class name to list

            field = ""
            constructor = ""
            method = ""
            field_name_list = []
            method_var_name_list = []

            for line in class_object.class_body_decl.things:
                if isinstance(line, Constructor_decl):
                    constructor = constructor + create_constructor(line)

                if isinstance(line, Field_decl):
                    # field_name_list.append(line.)
                    result, field_names = create_field(line, class_object, field_name_list)
                    field = field + result
                    field_name_list = field_names
                if isinstance(line, Method_decl):
                    result, method_names = create_method(line, class_object, method_var_name_list)
                    method = method + result
                    method_var_name_list = method_names                    

            res = res +f"\nClass Name: {str(class_object.class_name)}"
            res = res + f"\nSuperclass Name: {str(class_object.superclass_name)}"
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
    def __init__(self, type = None, variables = None):
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
    def __init__(self, modifier = None, formals = None, body = None):
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
    def __init__(self, stmt_list = None):
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
    def __init__(self, type = None, component = ''):
        super().__init__()
        self.type = type
        if component == None:
            self.component = ''
        else:
            self.component = component
    def __str__(self):
        pass

class Ifelsewhile_stmt(Node):
    def __init__(self, type = None, cond = None, then = None, els = '', type_2 = ''):
        super().__init__()
        self.type = type
        self.cond = cond
        self.then = then
        self.els = els
        self.type_2 = type_2
    def __str__(self):
        pass

class For_stmt(Node):
    def __init__(self, cond1 = None, cond2 = None, cond3 = None, body = None, type = None):
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
        if self.arguments is None:
            return '[]'
        else:
            return str(self.arguments)
        
class Arguments_cont(Node):
    def __init__(self):
        super().__init__()
        self.things = []
    def __str__(self):
        return str(self.things[::-1])

class Assign(Node):
    def __init__(self, lhs = None, expr = None):
        super().__init__()
        self.lhs = lhs
        self.expr = expr
    def __str__(self):
        pass

class Addition(Node):
    def __init__(self, type, left_expr, right_expr):
        super().__init__()
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.type = type
    def __str__(self):
        return str(self.left_expr)
        pass

class Subtraction(Node):
    def __init__(self, type, left_expr, right_expr):
        super().__init__()
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.type = type
    def __str__(self):
        return "DDDDDDDDDDD"
        pass

class Multiplication(Node):
    def __init__(self, type, left_expr, right_expr):
        super().__init__()
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.type = type
    def __str__(self):
        return "DDDDDDDDDDD"
        pass

class Division(Node):
    def __init__(self, type, left_expr, right_expr):
        super().__init__()
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.type = type
    def __str__(self):
        return "DDDDDDDDDDD"
        pass

class Conjection(Node):
    def __init__(self, type, left_expr, right_expr):
        super().__init__()
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.type = type
    def __str__(self):
        return "DDDDDDDDDDD"
        pass

class Disjunction(Node):
    def __init__(self, type, left_expr, right_expr):
        super().__init__()
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.type = type
    def __str__(self):
        return "DDDDDDDDDDD"
        pass

class Equality(Node):
    def __init__(self, type, left_expr, right_expr):
        super().__init__()
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.type = type
    def __str__(self):
        return "DDDDDDDDDDD"
        pass
    
class Disquality(Node):
    def __init__(self, type, left_expr, right_expr):
        super().__init__()
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.type = type
    def __str__(self):
        return "DDDDDDDDDDD"
        pass
    
class LessThan(Node):
    def __init__(self, type, left_expr, right_expr):
        super().__init__()
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.type = type
    def __str__(self):
        return "DDDDDDDDDDD"
        pass
    
class LessThanEqual(Node):
    def __init__(self, type, left_expr, right_expr):
        super().__init__()
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.type = type
    def __str__(self):
        return "DDDDDDDDDDD"
        pass
    
class GreaterThan(Node):
    def __init__(self, type, left_expr, right_expr):
        super().__init__()
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.type = type
    def __str__(self):
        return "DDDDDDDDDDD"
        pass
    
class GreaterThanEqual(Node):
    def __init__(self, type, left_expr, right_expr):
        super().__init__()
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.type = type
    def __str__(self):
        return "DDDDDDDDDDD"
        pass

class Field_access(Node):
    def __init__(self, primary = None, id = None, type = None):
        super().__init__()
        self.primary = primary
        self.id = id
        self.type = type
    def __str__(self):
        pass

class Uminus(Node):
    def __init__(self, type = None, expr = None):
        super().__init__()
        self.type = type
        self.expr = expr
    def __str__(self):
        pass

class Auto(Node):
    def __init__(self, post = None, pre = None, lhs = None):
        super().__init__()
        self.post = post
        self.pre = pre
        self.lhs = lhs
    def __str__(self):
        pass

class Method_invocation(Node):
    def __init__(self, field_access = None, argument_list = None):
        super().__init__()
        self.field_access = field_access
        self.argument_list = argument_list
    def __str__(self):
        pass

class NewObject(Node):
    def __init__(self, id = None, argument_list = ''):
        super().__init__()
        self.id = id
        self.argument_list = argument_list
    def __str__(self):
        return f"New-Object({self.id}, {str(self.argument_list)})"

class Paren(Node):
    def __init__(self, expr = None):
        super().__init__()
        self.expr = expr
    def __str__(self):
        pass
