class Node():   #Node represents the Node in a tree
    def __init__(self): #Default the Node doesnt have a parent
        self.parent = None

    def parentCount(self):  #this returns the amount of parents this node has
        count = 0
        current = self.parent
        while current is not None:
            count += 1
            current = current.parent
        return count
    
class Program(Node):
    def __init__(self, n, b):
        super().__init__()
        self.names = n
        self.body = b
        
    def eval(self):
        results = []
        for node in self.body:
            results.append(node.eval(self.names))
        return results
    def __str__(self):
        res = "NAMES: " + str(self.names)
        res += "\nBODY:" + str(self.body)
        for node in self.body:
            res += "\n" + str(node)
        return res
    
class Stress(Node):
    def __init__(self):
        self.things = []
    
    def __str__(self):
        res = "\t" * self.parentCount() + "Body"
        for node in self.things:
            res += "\n" + str(self.node)
        return res