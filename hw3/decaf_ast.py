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
        field = ""
        for thing in self.classes:
            res =  "\n--------------------------------------------------------------------------" + res
            for stuff in thing.class_body_decl.things:
                field = field + f"\nFIELD {str(stuff.counter)}, {str(stuff.var_decl.variables.variable.variable_name)}, {str(thing.class_name)}"
            res = field + res
            res = "\nFields:" + res
            res = "\nSuperclass Name:" + str(thing.superclass_name) + res
            res = "\nClass Name: " + str(thing.class_name) + res
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
    def __init__(self, modifier_value, ):
        super().__init__()
        self.modifier_value = modifier_value
    def __str__(self):
        return str(self.modifier_value)

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
        print(self.variable_name)
    def __str__(self):
        return str(self.variable_name)        

