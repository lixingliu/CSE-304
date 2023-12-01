'''
Name: Li Xing Liu
Netid: lixiliu
Student Id: 113318331

Name: Andy You
Netid: Andyou
Student Id: 113494190
'''

import sys
import re


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
    'STRING_CONST',
    'INCREMENT',
    'DECREMENT',
    'BOOL_AND',
    'BOOL_OR',
    'EQUALITY',
    'DISQUALITY',
    'LEQ',
    'GEQ',
    'ID',
    'PLUS',
    'MINUS',
    'MULTIPLY',
    'DIVIDE',
    'NOT',
    'GREATERTHAN',
    'LESSTHAN',
    'LEFTPAREN',
    'RIGHTPAREN'
] + list(reserved.values())

literals = "[]{};,=."

t_LEFTPAREN = r'\('
t_RIGHTPAREN = r'\)'
t_PLUS = r'\+'
t_MINUS = r'-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'/'
t_NOT = r'!'
t_GREATERTHAN = r'>'
t_LESSTHAN = r'<'


# this is interpreted as /* <stuff> */;
# <stuff> is represetned by .*? : . repesents any character and .* means zero or more any character
t_ignore_MULTI_COMMENT = r'/\*.*?\*/'

# this is interpreted as // <stuff>
# <stuff> is represented by .* measning zero or more any character
t_ignore_SING_COMMENT = r'//.*'

# \d matches any digit; [0-9] and the '+' signifies one or more occurences
# \d+\.\d* is used for at least one number in front [0-9] followed by a . and then zero or more digits
# \d*\.\d+ is used for zero or more numbers in front [0-9] followed by a . and then one ore more digits
# ([eE][+-]?\d+)? is used for the second kind of floating point numbers; starts with a e or E and is followed 
# by an optional + or - and then one or more digits. The ? surrounding the entire thing makes it all optional
def t_FLOAT_CONST(t):
    r'(\d*\.\d+)([eE][+-]?\d+)?'
    t.value = float(t.value)
    return t

def t_INT_CONST(t):
    r'\d+' ## are we acccepting 00000 ?
    t.value = int(t.value)
    return t


# starts with " and ends with "
# " <stuff> "; <stuff> is represented by (?:\\.|[^"\\])*
# ?: means it is a non-capturing group. It's used to group multiple patterns together for the purpose of regex
# \\. means it represents anything like \n, \t, \\, or \"; stuff with special meaning
# [^"\\] means it will ignore all " and \; " and \ are special special characters that strings cannot have
def t_STRING_CONST(t):
    r'\".*\"'
    return t

t_INCREMENT = r'\+\+'
t_DECREMENT = r'--'

t_BOOL_AND = r'&&'
t_BOOL_OR = r'\|\|'

t_EQUALITY = r'=='
t_DISQUALITY = r'!='

t_LEQ = r'<='
t_GEQ = r'>='

# ID must start with a letter and then followed be zero or more letters, numbers, or underscores
# t.type = reserved.get(t.value, 'ID') is used to check for reserved keywords
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# t_ignore is a special name. The regular expression indicates which characters the scanner will skip past
# while tokenizing. Ignore whitespace and tab
t_ignore = ' \t'

# Another special name. Determines what counts as a newline and what gets done when a newline character is read.
# Here the number of seq. newlines is counted, and the count is added to the current lineno, as tracked
# by the lexer. This allows the lexer to detemrine theline on which each token occurs for debugging and error reporting
def t_newline(t):
    r'\n+'
    t.lexer.lineStart = t.lexer.lexpos
    t.lexer.lineno += t.value.count('\n')

# Another special name. The body of this function determines what happens when the lexer encounters an
# illegal character. In this case, we print the character, its line number, adn its column number.
def t_error(t):
    print()
    print("LEXER: SYNTAX ERROR: ", end = '')
    print("Illegal Character '%s', at %d, %d" %
          (t.value[0], t.lineno, t.lexpos))
    print("CONTEXT: " + t.value[0:10])
    print()
    sys.exit()
    #t.lexer.skip(1)