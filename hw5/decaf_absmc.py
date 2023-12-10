arg_reg = []
temp_reg = [None] * 99

heap = []
control_stack = []
data_stack = []

cur_reg = 0

def get_next_temp_reg ():
   cur = cur_reg 
   cur_reg = cur_reg + 1
   return cur

def add_temp_reg (value):
    temp_reg.append(value)

def set_temp_reg_i (r1, val):
    temp_reg[r1] = val

def set_temp_reg_r (r1, r2):
    temp_reg[r1] = temp_reg[r2]

def sub (r1, r2, r3):
    temp_reg[r1] = temp_reg[r2] - temp_reg[r3]

def add (r1, r2, r3):
    temp_reg[r1] = temp_reg[r2] + temp_reg[r3]

def mul (r1, r2, r3):
    temp_reg[r1] = temp_reg[r2] * temp_reg[r3]

def div (r1, r2, r3):
    temp_reg[r1] = temp_reg[r2] / temp_reg[r3]

def and_b (r1, r2, r3):
   temp_reg[r1] = temp_reg[r2] and temp_reg[r3]

def or_b (r1, r2, r3):
   temp_reg[r1] = temp_reg[r2] or temp_reg[r3]

def ilt (r1, r2, r3):
   temp_reg[r1] = temp_reg[r2] < temp_reg[r3]

def ileq (r1, r2, r3):
   temp_reg[r1] = temp_reg[r2] <= temp_reg[r3]

def igt (r1, r2, r3):
   temp_reg[r1] = temp_reg[r2] > temp_reg[r3]

def igeq (r1, r2, r3):
   temp_reg[r1] = temp_reg[r2] >= temp_reg[r3]

def ieq (r1, r2, r3):
   temp_reg[r1] = temp_reg[r2] == temp_reg[r3]

def ineq (r1, r2, r3):
   temp_reg[r1] = temp_reg[r2] != temp_reg[r3]
