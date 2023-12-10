arg_reg = []
temp_reg = [None] * 99

heap = []
control_stack = []
data_stack = []

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