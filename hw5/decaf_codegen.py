import decaf_ast 
import decaf_absmc as absmc
import decaf_typecheck as typechecker
import sys

global print 
print = ""

def assign (lhs, type, rhs, value):
    lhs_start_index = lhs.find("(Variable(") + len("(Variable(")
    lhs_end_index = lhs.find("))", lhs_start_index)
    lhs_number = lhs[lhs_start_index:lhs_end_index]

    if ("Integer-constant" in rhs):
        move_immed_i(int(lhs_number)-1, int(value.literal))

    elif ("Unary-expression" in rhs):
        if("MINUS" in rhs and "Variable" in rhs):
            start_index = rhs.find("Unary-expression(MINUS, Variable(") + len("Unary-expression(MINUS, Variable(")
            end_index = rhs.find("))", start_index)
            number = rhs[start_index:end_index]

            move(int(lhs_number)-1, int(number)-1)
            move_immed_i(98, 0)
            isub(int(lhs_number)-1, 98, int(number)-1)

    elif("True" in rhs):
        move_immed_i(int(lhs_number)-1, 1)
    elif ("False" in rhs):
        move_immed_i(int(lhs_number)-1, 0)

    elif("Variable(" in rhs):
        start_index = rhs.find("Variable(") + len("Variable(")
        end_index = rhs.find("))", start_index)
        number = rhs[start_index:end_index]

        move(int(lhs_number)-1, int(number)-1)
    
def auto (pre, post, lhs):
    lhs_start_index = lhs.find("(Variable(") + len("(Variable(")
    lhs_end_index = lhs.find("))", lhs_start_index)
    lhs_number = lhs[lhs_start_index:lhs_end_index]

    if(post == "++"):
        move_immed_i(98, 1)
        iadd(int(lhs_number)-1, int(lhs_number)-1, 98)

    elif(post == "--"):
        move_immed_i(98, 1)
        isub(int(lhs_number)-1, int(lhs_number)-1, 98)

def method (name, key):
    global print
    print = print + "M_" + name + "_"  + str(key) + ":"

def move_immed_i (reg, value):
    absmc.set_temp_reg_i(reg, value)
    global print
    print = print + "\nmove_immed_i " + "t" + str(reg) + ", " + str(value)

def move (r1, r2):
    absmc.set_temp_reg_r(r1, r2)
    global print
    print = print + "\nmove " + "t" + str(r1) + ", " + "t" + str(r2)

def isub (r1, r2, r3):
    absmc.sub(r1, r2, r3)
    global print
    print = print + "\nisub " + "t" + str(r1) + ", " + "t" + str(r2) + ", " + "t" + str(r3)

def iadd (r1, r2, r3):
    absmc.add(r1, r2, r3)
    global print
    print = print + "\niadd " + "t" + str(r1) + ", " + "t" + str(r2) + ", " + "t" + str(r3)
