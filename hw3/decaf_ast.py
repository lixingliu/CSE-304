class_body = dict()

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
        for thing in self.classes:
            field = ""
            constructor = ""
            method = ""
            for stuff in thing.class_body_decl.things:
                if type(stuff) == type(Constructor_decl(None, None)):
                    constructor = constructor + f"\nCONSTRUCTOR {str(stuff.counter)}, {str(stuff.modifier.visibility)}"
                    constructor = constructor + f"\nConstructor Parameters: "
                    constructor = constructor + f"\nVariable Table: "
                    constructor = constructor + f"\nConstructor Body: "
                if type(stuff) == type(Field_decl(None, None, None)):
                    field = field + f"\nFIELD {str(stuff.counter)}, {str(stuff.var_decl.variables.variable.variable_name)}, {str(thing.class_name)}, {str(stuff.modifier.visibility)}, {str(stuff.modifier.applicability)}, {str(stuff.var_decl.type.type_value)}"

                if type(stuff) == type(Method_decl(None, None, None, None)):
                    method = method + f"\nMETHOD: {str(stuff.counter)}, {str(stuff.method_name)}, {str(thing.class_name)}, {str(stuff.modifier.visibility)}, {str(stuff.modifier.applicability)}, {str(stuff.type)}"
                    method = method + f"\nMethod Parameters: "
                    method = method + f"\nVariable Table: "
                    method = method + f"\nVariable "
                    method = method + f"\nMethod Body: "
            res =  "\n--------------------------------------------------------------------------" + res
            res = method + res
            res = f"\nMethods: " + res
            res = constructor + res
            res = f"\nConstructors: " + res
            res = field + res
            res = "\nFields:" + res
            res = f"\nSuperclass Name: {str(thing.superclass_name)}" + res
            res = f"\nClass Name: {str(thing.class_name)}" + res
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
        return "hi"
    
class Class_body_decl(Node):
    def __init__(self):
        super().__init__()
        self.things = []
    def __str__(self):
        pass
    
class Field_decl(Node):
    def __init__(self, modifier, var_decl, counter):
        super().__init__()
        self.modifier = modifier
        self.var_decl = var_decl
        self.counter = counter
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
        if type_value != "int" and type_value != "float" and type_value != "boolean":
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

class Constructor_decl(Node):
    def __init__(self, counter, modifier):
        super().__init__()
        self.counter = counter
        self.modifier = modifier
    def __str__(self):
        pass

class Method_decl(Node):
    def __init__(self, counter, method_name, modifier, type):
        super().__init__()
        self.counter = counter
        self.method_name = method_name
        self.modifier = modifier
        self.type = type
    def __str__(self):
        pass