import decaf_ast 
import decaf_absmc as absmc
import decaf_typecheck as typechecker
import sys
import re

global print 
print = ""

def assign (lhs, type, rhs, value):
    lhs_start_index = lhs.find("(Variable(") + len("(Variable(")
    lhs_end_index = lhs.find("))", lhs_start_index)
    lhs_number = lhs[lhs_start_index:lhs_end_index]

    if ("Integer-constant" in rhs):
        move_immed_i(int(lhs_number)-1, int(value.literal))
    
    elif("Float-constant" in rhs):
        move_immed_f(int(lhs_number)-1, int(value.literal))

    elif ("Unary-expression" in rhs):
        if("MINUS" in rhs and "Variable" in rhs):
            start_index = rhs.find("Unary-expression(MINUS, Variable(") + len("Unary-expression(MINUS, Variable(")
            end_index = rhs.find("))", start_index)
            number = rhs[start_index:end_index]

            move(int(lhs_number)-1, int(number)-1)
            next = absmc.get_next_temp()
            move_immed_i2(next, -1)
            imul2(int(lhs_number)-1, int(lhs_number)-1, next)
        elif("NEG" in rhs and "Variable" in rhs):
            start_index = rhs.find("Unary-expression(NEG, Variable(") + len("Unary-expression(NEG, Variable(")
            end_index = rhs.find("))", start_index)
            number = rhs[start_index:end_index]

            reg = move(int(lhs_number)-1, int(number)-1)
            next = absmc.get_next_temp()
            move_immed_i2(next, 0)
            next2 = absmc.get_next_temp()
            igeq2(next2, reg, next)
            move2(next2+1, next2)

    elif("True" in rhs):
        move_immed_i(int(lhs_number)-1, 1)
    elif ("False" in rhs):
        move_immed_i(int(lhs_number)-1, 0)

    elif("Binary("in rhs):
        if("Variable(" in rhs):
            regs = re.findall(r'Variable\((\d+)\)', rhs)

            if("add" in rhs):
                if(type == "int"):
                    iadd(int(lhs_number)-1, int(regs[0])-1, int(regs[1])-1)
                elif(type == "float"):
                    fadd(int(lhs_number)-1, int(regs[0])-1, int(regs[1])-1)
            elif("mul" in rhs):
                if(type == "int"):
                    imul(int(lhs_number)-1, int(regs[0])-1, int(regs[1])-1)
                elif(type == "float"):
                    fmul(int(lhs_number)-1, int(regs[0])-1, int(regs[1])-1)
            elif("sub" in rhs):
                if(type == "int"):
                    isub(int(lhs_number)-1, int(regs[0])-1, int(regs[1])-1)
                elif(type == "float"):
                    fsub(int(lhs_number)-1, int(regs[0])-1, int(regs[1])-1)
            elif("div" in rhs):
                if(type == "int"):
                    idiv(int(lhs_number)-1, int(regs[0])-1, int(regs[1])-1)
                elif(type =="float"):
                    fdiv(int(lhs_number)-1, int(regs[0])-1, int(regs[1])-1)
            elif("and," in rhs):
                and_b(int(lhs_number)-1, int(regs[0])-1, int(regs[1])-1)
            elif("or," in rhs):
                or_b(int(lhs_number)-1, int(regs[0])-1, int(regs[1])-1)
            elif("lt," in rhs):
                ilt(int(lhs_number)-1, int(regs[0])-1, int(regs[1])-1)
            elif("leq," in rhs):
                ileq(int(lhs_number)-1, int(regs[0])-1, int(regs[1])-1)
            elif("gt," in rhs):
                igt(int(lhs_number)-1, int(regs[0])-1, int(regs[1])-1)
            elif("geq," in rhs):
                igeq(int(lhs_number)-1, int(regs[0])-1, int(regs[1])-1)
            elif("neq," in rhs):
                ineq(int(lhs_number)-1, int(regs[0])-1, int(regs[1])-1)
            elif("eq," in rhs):
                ieq(int(lhs_number)-1, int(regs[0])-1, int(regs[1])-1)

    elif("Variable(" in rhs):
        start_index = rhs.find("Variable(") + len("Variable(")
        end_index = rhs.find("))", start_index)
        number = rhs[start_index:end_index]

        move(int(lhs_number)-1, int(number)-1)

    
def auto (pre, post, lhs):
    lhs_start_index = lhs.find("(Variable(") + len("(Variable(")
    lhs_end_index = lhs.find("))", lhs_start_index)
    lhs_number = lhs[lhs_start_index:lhs_end_index]

    next = absmc.get_next_temp()
    move_immed_i2(next, 1)

    if(post == "++"):
        iadd2(int(lhs_number)-1, int(lhs_number)-1, next)

    elif(post == "--"):
        isub2(int(lhs_number)-1, int(lhs_number)-1, next)

def method (name, key):
    global print
    print = print + "M_" + name + "_"  + str(key) + ":"

def if_stmt (cond, then_expr, else_expr):
    regs = re.findall(r'Variable\((\d+)\)', cond)

    regs2 = re.findall(r'Variable\(\d+\)', then_expr)
    first_index = then_expr.find("int")  
    second_index = then_expr.find("int", first_index + 1)
    second_int = then_expr[second_index:second_index + 3]

    if("Binary(lt," in cond):
        ilt(int(regs[0])+2 ,int(regs[0])-1, int(regs[1])-1)
    label = absmc.next_label()
    bnz(int(regs[0])+2, str(label))
    jmp(str(label + 1))
    absmc.next_label()

    global print
    print = print + "\nL" + str(label) + ":"

    if("Block([ \nExpr( Assign(" in then_expr):
        assign(regs2[0], second_int, then_expr, then_expr)
        
    print = print + "\nL" + str(label+1) + ":"
     

# Int

def move_immed_i (r1, value):
    r1 = absmc.check_offset(r1, r1)
    global print
    print = print + "\nmove_immed_i " + "t" + str(r1) + ", " + str(value)

def move_immed_i2 (r1, value):
    r1 = absmc.add_temp_reg("offset")
    global print
    print = print + "\nmove_immed_i " + "t" + str(r1) + ", " + str(value)

def move (r1, r2):
    r1 = absmc.check_offset(r1, r1)
    r2 = absmc.check_offset(r2, "None")
    global print
    print = print + "\nmove " + "t" + str(r1) + ", " + "t" + str(r2)
    return r1

def move2 (r1, r2):
    r1 = absmc.add_temp_reg(r1)
    r1 = absmc.add_temp_reg(r1+1)
    global print
    print = print + "\nmove " + "t" + str(r1) + ", " + "t" + str(r2)

def isub (r1, r2, r3):
    r1 = absmc.check_offset(r1, r1)
    r2 = absmc.check_offset(r2, "None")
    r3 = absmc.check_offset(r3, "None")
    global print
    print = print + "\nisub " + "t" + str(r1) + ", " + "t" + str(r2) + ", " + "t" + str(r3)

def isub2 (r1, r2, r3):
    global print
    print = print + "\nisub " + "t" + str(r1) + ", " + "t" + str(r2) + ", " + "t" + str(r3)

def iadd (r1, r2, r3):
    r1 = absmc.check_offset(r1, r1)
    r2 = absmc.check_offset(r2, "None")
    r3 = absmc.check_offset(r3, "None")
    global print
    print = print + "\niadd " + "t" + str(r1) + ", " + "t" + str(r2) + ", " + "t" + str(r3)

def iadd2 (r1, r2, r3):
    global print
    print = print + "\niadd " + "t" + str(r1) + ", " + "t" + str(r2) + ", " + "t" + str(r3)

def imul (r1, r2, r3):
    r1 = absmc.check_offset(r1, r1)
    r2 = absmc.check_offset(r2, "None")
    r3 = absmc.check_offset(r3, "None")
    global print
    print = print + "\nimul " + "t" + str(r1) + ", " + "t" + str(r2) + ", " + "t" + str(r3)

def imul2 (r1, r2, r3):
    global print
    print = print + "\nimul " + "t" + str(r1) + ", " + "t" + str(r2) + ", " + "t" + str(r3)

def idiv (r1, r2, r3):
    r1 = absmc.check_offset(r1, r1)
    r2 = absmc.check_offset(r2, "None")
    r3 = absmc.check_offset(r3, "None")
    global print
    print = print + "\nidiv " + "t" + str(r1) + ", " + "t" + str(r2) + ", " + "t" + str(r3)


#Float

def move_immed_f (reg, value):
    #absmc.set_temp_reg_i(reg, value)
    global print
    if("." in str(value)):
        print = print + "\nmove_immed_f " + "t" + str(reg) + ", " + str(value)
    else:
        print = print + "\nmove_immed_f " + "t" + str(reg) + ", " + str(value) + ".0" 

def fsub (r1, r2, r3):
    #absmc.sub(r1, r2, r3)
    global print
    print = print + "\nfsub " + "t" + str(r1) + ", " + "t" + str(r2) + ", " + "t" + str(r3)

def fadd (r1, r2, r3):
    #absmc.add(r1, r2, r3)
    global print
    print = print + "\nfadd " + "t" + str(r1) + ", " + "t" + str(r2) + ", " + "t" + str(r3)

def fmul (r1, r2, r3):
    #absmc.mul(r1, r2, r3)
    global print
    print = print + "\nfmul " + "t" + str(r1) + ", " + "t" + str(r2) + ", " + "t" + str(r3)

def fdiv (r1, r2, r3):
    #absmc.div(r1, r2, r3)
    global print
    print = print + "\nfdiv " + "t" + str(r1) + ", " + "t" + str(r2) + ", " + "t" + str(r3)

def and_b (r1, r2, r3):
    #absmc.and_b(r1, r2, r3)
    global print
    print = print + "\nand " + "t" + str(r1) + ", " + "t" + str(r2) + ", " + "t" + str(r3)

def or_b (r1, r2, r3):
    #absmc.or_b(r1, r2, r3)
    global print
    print = print + "\nor " + "t" + str(r1) + ", " + "t" + str(r2) + ", " + "t" + str(r3)

def ilt (r1, r2, r3):
    #absmc.ilt(r1, r2, r3)
    global print
    print = print + "\nilt " + "t" + str(r1) + ", " + "t" + str(r2) + ", " + "t" + str(r3) 

def ileq (r1, r2, r3):
    #absmc.ileq(r1, r2, r3)
    global print
    print = print + "\nileq " + "t" + str(r1) + ", " + "t" + str(r2) + ", " + "t" + str(r3)

def igt (r1, r2, r3):
    #absmc.or_b(r1, r2, r3)
    global print
    print = print + "\nigt " + "t" + str(r1) + ", " + "t" + str(r2) + ", " + "t" + str(r3)

def igeq (r1, r2, r3):
    r1 = absmc.check_offset(r1, r1)
    r2 = absmc.check_offset(r2, "None")
    r3 = absmc.check_offset(r3, "None")
    global print
    print = print + "\nigeq " + "t" + str(r1) + ", " + "t" + str(r2) + ", " + "t" + str(r3)

def igeq2 (r1, r2, r3):
    global print
    print = print + "\nigeq " + "t" + str(r1) + ", " + "t" + str(r2) + ", " + "t" + str(r3)

def ieq (r1, r2, r3):
    #absmc.ieq(r1, r2, r3)
    global print
    print = print + "\nieq " + "t" + str(r1) + ", " + "t" + str(r2) + ", " + "t" + str(r3)

def ineq (r1, r2, r3):
    #absmc.ineq(r1, r2, r3)
    global print
    print = print + "\nineq " + "t" + str(r1) + ", " + "t" + str(r2) + ", " + "t" + str(r3)

def bnz (r1, name):
    global print
    print = print + "\nbnz " + "t" + str(r1) + ", " + "L" + str(name)

def jmp (name):
    global print
    print = print + "\njmp " + "L" + str(name)