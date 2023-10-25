classes = dict()

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
            res += "\nCLASS NAME: " + str(thing.class_name)
        # for node in self.classes:
        return res

class Class_decl_list(Node):
    def __init__(self):
        self.things = []
    def __str__(self):
        pass

class Class_decl(Node):
    def __init__(self, class_name):
        super().__init__()
        self.class_name = class_name
    def __str__(self):
        return "hi"

            

