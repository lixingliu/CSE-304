class_body = dict()

FIELD_COUNTER = 0
CONSTRUCTOR_COUNTER = 0
METHOD_COUNTER = 6

def create_body(stmt, variable_table, constructor_param_list_counter):
    print(type(stmt))
    if type(stmt) == type(Paren(None)):
        outcome = create_body(stmt.expr, variable_table, constructor_param_list_counter)
        return(outcome)
    if type(stmt) == type(None):
        return ["Skip-stmt, ", variable_table, constructor_param_list_counter]
    if type(stmt) == type(Stmt(None, None)):
        x = create_body(stmt.component, variable_table, constructor_param_list_counter)
        if stmt.type == 'return' and type(stmt.component) == type(Field_access(None, None, None)):
            return [f"{stmt.type}( {x[0]} )", x[1], x[2]]

        outcome = [None, x[1], x[2]]
        outcome[0] = f"{stmt.type}( {x[0]} )"
        return outcome
    if type(stmt) == type(Ifelsewhile_stmt(None, None, None, None)):
        if_body_stuff = ""
        else_body_stuff = ""
        outcome = [None, None, None]
        for if_stuff in stmt.then.stmt_list.things[::-1]:
            outcome = create_body(if_stuff, variable_table, constructor_param_list_counter)
            if_body_stuff = if_body_stuff + outcome[0]
            variable_table = outcome[1]
            constructor_param_list_counter = outcome[2]
        if stmt.els != "":
            for else_stuff in stmt.els.stmt_list.things[::-1]:
                outcome = create_body(else_stuff, variable_table, constructor_param_list_counter)
                variable_table = outcome[1]
                constructor_param_list_counter = outcome[2]
                else_body_stuff = else_body_stuff + outcome[0]
        if_condition = create_body(stmt.cond, variable_table, constructor_param_list_counter)
        variable_table = if_condition[1]
        constructor_param_list_counter = if_condition[2]
        outcome[0] = f"{stmt.type}({if_condition[0]}) Block ([\n{if_body_stuff}]) else"
        if else_body_stuff == '':
            else_body_stuff = "Skip-stmt"
        if else_body_stuff != "":
            outcome[0] = outcome[0] + f" Block ([\n{else_body_stuff} ])"
            variable_table = outcome[1]
            variable_table = outcome[2]
            return outcome
        else:
            return outcome
    if type(stmt) == type(For_stmt(None, None, None, None, None)):
        for_body_stuff = ""
        outcome = [None, None, None]
        for for_stuff in stmt.then.stmt_list.things[::-1]:
            outcome = create_body(for_stuff, variable_table, constructor_param_list_counter)
            if outcome[0] == 'empty( Skip-stmt )':
                for_body_stuff = 'Skip-stmt'
                break;
            for_body_stuff = for_body_stuff + outcome[0]
            variable_table = outcome[1]
            constructor_param_list_counter = outcome[2]
            
        for_cond_1 = create_body(stmt.cond1, variable_table, constructor_param_list_counter)
        variable_table = for_cond_1[1]
        constructor_param_list_counter = for_cond_1[2]

        for_cond_2 = create_body(stmt.cond2, variable_table, constructor_param_list_counter)
        variable_table = for_cond_2[1]
        constructor_param_list_counter = for_cond_2[2]    

        for_cond_3 = create_body(stmt.cond3, variable_table, constructor_param_list_counter)
        variable_table = for_cond_3[1]
        constructor_param_list_counter = for_cond_3[2]

        result = f"{stmt.type}({for_cond_1[0]}{for_cond_2[0]}, {for_cond_3[0]}) Block ([\n{for_body_stuff}])"
        outcome[0] = result
        outcome[1] = variable_table
        outcome[2] = constructor_param_list_counter
        return outcome
    if type(stmt) == type(Auto(None, None, None)):
        find_indices = lambda strings, substring: list(filter(lambda x: substring in strings[x], range(len(strings))))
        variable_value = f", {stmt.lhs.id},"
        variable_number = find_indices(variable_table.split("\n"), variable_value)[0]
        if (stmt.pre != None):
            if (stmt.pre == "++"):
                return [f"Expr(Auto(Variable({variable_number}), inc, pre) ),\n", variable_table, constructor_param_list_counter]
            if (stmt.pre == "--"):
                return [f"Expr(Auto(Variable({variable_number}), dec, pre) ),\n", variable_table, constructor_param_list_counter]
        if (stmt.post != None):
            if (stmt.post == "++"):
                return [f"Expr(Auto(Variable({variable_number}), inc, post) ),\n", variable_table, constructor_param_list_counter]
            if (stmt.post == "--"):
                return [f"expr(Auto(Variable({variable_number}), dec, post) ),\n", variable_table, constructor_param_list_counter]
        return "AAAA"
    if type(stmt) == type(Var_decl(None, None)):
        constructor_param_list_counter = constructor_param_list_counter + 1
        variable_table = variable_table + f"\nVARIABLE {constructor_param_list_counter}, {stmt.variables.variable.things[0].variable_name}, local, {stmt.type.type_value}"
        return ['', variable_table, constructor_param_list_counter]
    if type(stmt) == type(Assign(None, None)):
        left = ""
        right = ""
        if stmt.lhs.type == ".":
            left = f"Field-access({stmt.lhs.primary}, {stmt.lhs.id})"
        if stmt.lhs.type == None:
            find_indices = lambda strings, substring: list(filter(lambda x: substring in strings[x], range(len(strings))))
            variable_value = f", {stmt.lhs.id},"
            variable_number = find_indices(variable_table.split("\n"), variable_value)[0]
            left = f"Variable({variable_number})"
        right = create_body(stmt.expr, variable_table, constructor_param_list_counter)
        variable_table = right[1]
        constructor_param_list_counter = right[2]
        result = f"Expr( Assign({left}, {right[0]}) ), \n"
        outcome = [result, variable_table, constructor_param_list_counter]
        return outcome
    if stmt == "true":
        return [f"Constant({True})", variable_table, constructor_param_list_counter]
    if stmt == "false":
        return [f"Constant({False})", variable_table, constructor_param_list_counter]
    if stmt == "null":
        return [f"Constant(Null)", variable_table, constructor_param_list_counter]
    if type(stmt) == type(Uminus(None, None)):
        outcome = create_body(stmt.expr, variable_table, constructor_param_list_counter)
        outcome[0] = f"Unary-expression(MINUS, {outcome[0]})"
        return outcome
    if type(stmt) == type(Field_access(None, None, None)):
        outcome  = None
        if type(stmt.primary) == type(Field_access(None, None, None)):
            outcome = create_body(stmt.primary, variable_table, constructor_param_list_counter)
            stmt.primary = outcome[0]
            variable_table = outcome[1]
            constructor_param_list_counter = outcome[2]
        if stmt.primary == None:
            find_indices = lambda strings, substring: list(filter(lambda x: substring in strings[x], range(len(strings))))
            variable_value = f", {stmt.id},"
            variable_number = find_indices(variable_table.split("\n"), variable_value)[0]
            return [f"Variable({variable_number})", variable_table, constructor_param_list_counter]
        return[f"Field-access({stmt.primary}, {stmt.id})", variable_table, constructor_param_list_counter]
    if type(stmt) == type(0.0):
        return [f"Constant(Float-constant({stmt}))", variable_table, constructor_param_list_counter]
    if type(stmt) == type(0):
        return [f"Constant(Integer-constant({stmt}))", variable_table, constructor_param_list_counter]
    if type(stmt) == type(""):
        if stmt == 'empty':
            return ["Skip-stmt", variable_table, constructor_param_list_counter]
        return [f"Constant(String-constant({stmt}))", variable_table, constructor_param_list_counter]
    if type(stmt) == type(Addition(None, None, None)):
        outcome_1 = create_body(stmt.left_expr, variable_table, constructor_param_list_counter)
        outcome_2 = create_body(stmt.right_expr, outcome_1[1], outcome_1[2])
        outcome_3 = [f"Binary(add, {outcome_1[0]}, {outcome_2[0]})", outcome_2[1], outcome_2[2]]
        return outcome_3
    if type(stmt) == type(Subtraction(None, None, None)):
        outcome_1 = create_body(stmt.left_expr, variable_table, constructor_param_list_counter)
        outcome_2 = create_body(stmt.right_expr, outcome_1[1], outcome_1[2])
        outcome_3 = [f"Binary(sub, {outcome_1[0]}, {outcome_2[0]})", outcome_2[1], outcome_2[2]]
        return outcome_3
    if type(stmt) == type(Multiplication(None, None, None)):
        outcome_1 = create_body(stmt.left_expr, variable_table, constructor_param_list_counter)
        outcome_2 = create_body(stmt.right_expr, outcome_1[1], outcome_1[2])
        outcome_3 = [f"( Binary(mul, {outcome_1[0]}, {outcome_2[0]}) )", outcome_2[1], outcome_2[2]]
        return outcome_3
    if type(stmt) == type(Division(None, None, None)):
        outcome_1 = create_body(stmt.left_expr, variable_table, constructor_param_list_counter)
        outcome_2 = create_body(stmt.right_expr, outcome_1[1], outcome_1[2])
        outcome_3 = [f"Binary(div, {outcome_1[0]}, {outcome_2[0]})", outcome_2[1], outcome_2[2]]
        return outcome_3
    if type(stmt) == type(Conjection(None, None, None)):
        outcome_1 = create_body(stmt.left_expr, variable_table, constructor_param_list_counter)
        outcome_2 = create_body(stmt.right_expr, outcome_1[1], outcome_1[2])
        outcome_3 = [f"Binary(and, {outcome_1[0]}, {outcome_2[0]})", outcome_2[1], outcome_2[2]]
        return outcome_3
    if type(stmt) == type(Disjunction(None, None, None)):
        outcome_1 = create_body(stmt.left_expr, variable_table, constructor_param_list_counter)
        outcome_2 = create_body(stmt.right_expr, outcome_1[1], outcome_1[2])
        outcome_3 = [f"Binary(or, {outcome_1[0]}, {outcome_2[0]})", outcome_2[1], outcome_2[2]]
        return outcome_3
    if type(stmt) == type(Equality(None, None, None)):
        outcome_1 = create_body(stmt.left_expr, variable_table, constructor_param_list_counter)
        outcome_2 = create_body(stmt.right_expr, outcome_1[1], outcome_1[2])
        outcome_3 = [f"Binary(eq, {outcome_1[0]}, {outcome_2[0]})", outcome_2[1], outcome_2[2]]
        return outcome_3
    if type(stmt) == type(Disquality(None, None, None)):
        outcome_1 = create_body(stmt.left_expr, variable_table, constructor_param_list_counter)
        outcome_2 = create_body(stmt.right_expr, outcome_1[1], outcome_1[2])
        outcome_3 = [f"Binary(neq, {outcome_1[0]}, {outcome_2[0]})", outcome_2[1], outcome_2[2]]
        return outcome_3
    if type(stmt) == type(LessThan(None, None, None)):
        outcome_1 = create_body(stmt.left_expr, variable_table, constructor_param_list_counter)
        outcome_2 = create_body(stmt.right_expr, outcome_1[1], outcome_1[2])
        outcome_3 = [f"Binary(lt, {outcome_1[0]}, {outcome_2[0]})", outcome_2[1], outcome_2[2]]
        return outcome_3
    if type(stmt) == type(LessThanEqual(None, None, None)):
        outcome_1 = create_body(stmt.left_expr, variable_table, constructor_param_list_counter)
        outcome_2 = create_body(stmt.right_expr, outcome_1[1], outcome_1[2])
        outcome_3 = [f"Binary(leq, {outcome_1[0]}, {outcome_2[0]})", outcome_2[1], outcome_2[2]]
        return outcome_3
    if type(stmt) == type(GreaterThan(None, None, None)):
        outcome_1 = create_body(stmt.left_expr, variable_table, constructor_param_list_counter)
        outcome_2 = create_body(stmt.right_expr, outcome_1[1], outcome_1[2])
        outcome_3 = [f"Binary(gt, {outcome_1[0]}, {outcome_2[0]})", outcome_2[1], outcome_2[2]]
        return outcome_3
    if type(stmt) == type(GreaterThanEqual(None, None, None)):
        outcome_1 = create_body(stmt.left_expr, variable_table, constructor_param_list_counter)
        outcome_2 = create_body(stmt.right_expr, outcome_1[1], outcome_1[2])
        outcome_3 = [f"Binary(geq, {outcome_1[0]}, {outcome_2[0]})", outcome_2[1], outcome_2[2]]
        return outcome_3
    if type(stmt) == type(Method_invocation(None, None)):
        argument_list = []
        if (stmt.argument_list.arguments != None):
            find_indices = lambda strings, substring: list(filter(lambda x: substring in strings[x], range(len(strings))))
            for argument in stmt.argument_list.arguments.things:
                variable_value = f", {argument.id},"
                variable_number = find_indices(variable_table.split("\n"), variable_value)[0]
                argument_list.append(f"Variable({variable_number})")
        if hasattr(stmt.field_access.primary, "id"):
            result = f"Method-call(Class-reference({stmt.field_access.primary.id}), {stmt.field_access.id}, [{str(argument_list).strip('[]')}])"
        else:
            result = f"Method-call({stmt.field_access.primary}, {stmt.field_access.id}, [{str(argument_list).strip('[]')}])"
        outcome = [result, variable_table, constructor_param_list_counter]
        return outcome
    if type(stmt) == type(Block(None)):
        outcome = ['', variable_table, constructor_param_list_counter]
        print(variable_table)
        for element in stmt.stmt_list.things[::-1]:
            result = create_body(element, outcome[1], outcome[2])
            outcome[0] = outcome[0] + result[0]
            outcome[1] = result[1]
            outcome[2] = result[2]
        outcome[0] = f'Block([\n{outcome[0]}])'
        return outcome
    print("sadsadsadsadsadsad")
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
        #In class intialization
        pub_sta_mod = Modifier("public", "static")
        scan_int = Method_decl("scan_int", pub_sta_mod, Type("int"), Formals(Formals_cont()), Stmt_list()) #Initializing scan_int
        scan_float = Method_decl("scan_float", pub_sta_mod, Type("float"), Formals(Formals_cont()), Stmt_list()) #Initializing scan_float
        class_in_body_decl = Class_body_decl()
        class_in_body_decl.things.append(scan_int)
        class_in_body_decl.things.append(scan_float)
        class_in = Class_decl("In", "", class_in_body_decl) #Append the two methods to In's class_body_decl

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

        class_name_list = []
        for thing in self.classes[::-1]:
            if (thing.class_name == 'Out' or thing.class_name == 'In'):
                continue
            elif (thing.class_name in class_name_list): #If class name is not unique, throw error
                res = "Error: Class name not unique"
                return res
            class_name_list.append(thing.class_name) #Add class name to list

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
                        constructor_var_name_list = []
                        for constructor_stuff in stuff.formals.formal_param.things[::-1]:
                            if(constructor_stuff.variable.variable_name in constructor_var_name_list): #If var name is not unique, throw error
                                res = "Error: constructor variable name not unique"
                                return res
                            constructor_var_name_list.append(constructor_stuff.variable.variable_name) #Add var name to list
                            constructor_param_list_counter = constructor_param_list_counter + 1
                            constructor_param_list.append(constructor_param_list_counter)
                            variable_table = variable_table + f"\nVARIABLE {constructor_param_list_counter}, {constructor_stuff.variable.variable_name}, formal, {constructor_stuff.type.type_value}"

                    constructor_body_stuff = ""
                    for constructor_stmt in stuff.body.stmt_list.things[::-1]:
                        outcome = create_body(constructor_stmt, variable_table, constructor_param_list_counter)
                        constructor_body_stuff = constructor_body_stuff + outcome[0]
                        variable_table = outcome[1]
                        constructor_param_list_counter = outcome[2]
                    
                    constructor_body = f"\nBlock([\n{constructor_body_stuff}\n])"
                    constructor = constructor + f"\nCONSTRUCTOR: {CONSTRUCTOR_COUNTER}, {str(stuff.modifier.visibility)}"
                    constructor = constructor + f"\nConstructor Parameters: {str(constructor_param_list).strip('[]')}"
                    constructor = constructor + f"\nVariable Table: {variable_table}"
                    constructor = constructor + f"\nConstructor Body: {constructor_body}"

                if type(stuff) == type(Field_decl(None, None)):
                    field_name_list = []
                    for field_stuff in stuff.var_decl.variables.variable.things[::-1]:
                        global FIELD_COUNTER
                        if (field_stuff.variable_name in field_name_list): #If field name is not unique, throw error
                            res = "Error: field name not unique"
                            return res
                        field_name_list.append(field_stuff.variable_name) #Add field name to list
                        FIELD_COUNTER = FIELD_COUNTER + 1
                        field = field + f"\nFIELD {FIELD_COUNTER}, {str(field_stuff.variable_name)}, {str(thing.class_name)}, {str(stuff.modifier.visibility)}, {str(stuff.modifier.applicability)}, {str(stuff.var_decl.type.type_value)}"

                if type(stuff) == type(Method_decl(None, None, None, None, None)):
                    global METHOD_COUNTER
                    METHOD_COUNTER = METHOD_COUNTER + 1
                    method_param_list = []
                    method_param_list_counter = 0
                    variable_table = ""
                    method_body = ""
                    if (hasattr(stuff.formals.formal_param, "things")):
                        method_var_name_list = []
                        for method_stuff in stuff.formals.formal_param.things[::-1]:
                            if(method_stuff.variable.variable_name in method_var_name_list): #If var name is not unique, throw error
                                res = "Error: method variable name not unique"
                                return res
                            method_var_name_list.append(method_stuff.variable.variable_name) #Add var name to list
                            method_param_list_counter = method_param_list_counter + 1
                            method_param_list.append(method_param_list_counter)
                            variable_table = variable_table + f"\nVARIABLE {method_param_list_counter}, {method_stuff.variable.variable_name}, formal, {method_stuff.type.type_value}"
                    
                    method_body_stuff = ""
                    for method_stmt in stuff.body.stmt_list.things[::-1]:
                        outcome = create_body(method_stmt, variable_table, method_param_list_counter)
                        variable_table = outcome[1]
                        method_param_list_counter = outcome[2]
                        method_body_stuff = method_body_stuff + outcome[0]

                    method_body = f"\nBlock([\n{method_body_stuff}\n])"
                    method = method + f"\nMETHOD: {METHOD_COUNTER}, {str(stuff.method_name)}, {str(thing.class_name)}, {str(stuff.modifier.visibility)}, {str(stuff.modifier.applicability)}, {str(stuff.type)}"
                    method = method + f"\nMethod Parameters: {str(method_param_list).strip('[]')}"
                    method = method + f"\nVariable Table:  {variable_table}"
                    method = method + f"\nMethod Body:   {method_body}"
                    

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

class Assign(Node):
    def __init__(self, lhs, expr):
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
        pass

class Subtraction(Node):
    def __init__(self, type, left_expr, right_expr):
        super().__init__()
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.type = type
    def __str__(self):
        pass

class Multiplication(Node):
    def __init__(self, type, left_expr, right_expr):
        super().__init__()
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.type = type
    def __str__(self):
        pass

class Division(Node):
    def __init__(self, type, left_expr, right_expr):
        super().__init__()
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.type = type
    def __str__(self):
        pass

class Conjection(Node):
    def __init__(self, type, left_expr, right_expr):
        super().__init__()
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.type = type
    def __str__(self):
        pass

class Disjunction(Node):
    def __init__(self, type, left_expr, right_expr):
        super().__init__()
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.type = type
    def __str__(self):
        pass

class Equality(Node):
    def __init__(self, type, left_expr, right_expr):
        super().__init__()
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.type = type
    def __str__(self):
        pass

class Disquality(Node):
    def __init__(self, type, left_expr, right_expr):
        super().__init__()
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.type = type
    def __str__(self):
        pass

class LessThan(Node):
    def __init__(self, type, left_expr, right_expr):
        super().__init__()
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.type = type
    def __str__(self):
        pass

class LessThanEqual(Node):
    def __init__(self, type, left_expr, right_expr):
        super().__init__()
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.type = type
    def __str__(self):
        pass

class GreaterThan(Node):
    def __init__(self, type, left_expr, right_expr):
        super().__init__()
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.type = type
    def __str__(self):
        pass

class GreaterThanEqual(Node):
    def __init__(self, type, left_expr, right_expr):
        super().__init__()
        self.left_expr = left_expr
        self.right_expr = right_expr
        self.type = type
    def __str__(self):
        pass


class Field_access(Node):
    def __init__(self, primary, id, type):
        super().__init__()
        self.primary = primary
        self.id = id
        self.type = type
    def __str__(self):
        pass

class Uminus(Node):
    def __init__(self, type, expr):
        super().__init__()
        self.type = type
        self.expr = expr
    def __str__(self):
        pass

class Auto(Node):
    def __init__(self, post, pre, lhs):
        super().__init__()
        self.post = post
        self.pre = pre
        self.lhs = lhs
    def __str__(self):
        pass

class Method_invocation(Node):
    def __init__(self, field_access, argument_list):
        super().__init__()
        self.field_access = field_access
        self.argument_list = argument_list
    def __str__(self):
        pass

class NewObject(Node):
    def __init__(self, id, argument_list):
        super().__init__()
        self.id = id
        self.argument_list = argument_list
    def __str__(self):
        pass

class Paren(Node):
    def __init__(self, expr):
        super().__init__()
        self.expr = expr
    def __str__(self):
        pass