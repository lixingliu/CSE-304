arg_reg = []
temp_reg = [None] * 99

heap = []
control_stack = []
data_stack = []

global cur_reg
cur_reg = 0
global offset
offset = 0

def get_next_temp():
   global cur_reg
   global offset
   next = cur_reg + offset
   return next

def check_offset(r1):
   global offset
   return r1 + offset

def add_temp_reg (value):
   global offset
   if(value == "offset"):
      offset = offset + 1
   global cur_reg
   cur = cur_reg + offset
   temp_reg[cur] = value
   cur_reg = cur_reg + 1
   return cur 

'''
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
'''