import sys



reserved = {
    'boolean' : "BOOLEAN",
    'break' :  'BREAK',
    'continue' : 'CONTINUE',
    'class' : 'CLASS',
    'do' : 'DO',
    'else' : 'ELSE',
    'extends' : 'EXTENDS',
    'false' : 'FALSE',
    'float' : 'FLOAT',
    'for' : 'FOR',
    'if' : 'IF',
    'int' : 'INT',
    'new' : 'NEW',
    'null' : 'NULL',
    'private' : 'PRIVATE',
    'public' : 'PUBLIC',
    'return' : 'RETURN',
    'static' : 'STATIC',
    'super' : 'SUPER',
    'this' : 'THIS',
    'true' : 'TRUE',
    'void' : 'VOID',
    'while' : 'WHILE'
}

tokens = [
    'MULTI_COMMENT',
    'SING_COMMENT',
    'INT_CONST',
    'FLOAT_CONST',
    'STRNG_CONST',
    'INCREMENT',
    'DECREMENT',
    'BOOL_AND',
    'BOOL_OR',
    'EQUALITY',
    'DISQUALITY',
    'LEQ',
    'GEQ',
    'ID'
] + list(reserved.values())

# this is interpreted as /* <stuff> */;
# <stuff> is represetned by .*? : . repesents any character and .* means zero or more any character
t_ignore_MULTI_COMMENT = r'/\*.*?\*/'

# this is interpreted as // <stuff>
# <stuff> is represented by .* measning zero or more any character
t_ignore_SING_COMMENT = r'//.*'

# \d matches any digit; [0-9] and the '+' signifies one or more occurences
def t_INT_CONST(t):
    r'\d+'
    t.value = int(t.value)
    return t

# \d+\.\d* is used for at least one number in front [0-9] followed by a . and then zero or more digits
# \d*\.\d+ is used for zero or more numbers in front [0-9] followed by a . and then one ore more digits
# ([eE][+-]?\d+)? is used for the second kind of floating point numbers; starts with a e or E and is followed 
# by an optional + or - and then one or more digits. The ? surrounding the entire thing makes it all optional
def t_FLOAT_CONST(t):
    r'(\d+\.\d*)|(\d*\.\d+)([eE][+-]?\d+)?'
    t.value = float(t.value)
    return t