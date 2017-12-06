#-----------Library Info-----------#
# We use Lex and Yacc which are libraries for parsing
# lex - laxer generator
# yacc - parser generator. token is a string
#-------User Case------#
#   1   +   2
# 1 => Int(1)
# + => Plus
# 2 => Int(2)
# then creates a tree
# we will pass it to a functions
# it will run the tokens that yacc creates

#---------------------CODE EXECUTION BEGINS------------#
import ply.lex as lex
import ply.yacc as yacc
import sys

#-------Tokens and Lax------------#
tokens = [
    'INT',
    'FLOAT',
    'NAME',
    'PLUS',
    'MINUS',
    'DIVIDE',
    'MULTIPLY',
    'EQUALS'
]

t_PLUS = r'\+'
t_MINUS = r'\-'
t_MULTIPLY = r'\*'
t_DIVIDE = r'\/'
t_EQUALS = r'\='
# t_OPEN_PARENTHESIS = r'\('
# t_CLOSE_PARENTHESIS = r'\)'

t_ignore = r' ' #this will ignore spaces, 1+1 is the same as 1 + 1


# t is our token object
# we are getting the value, and turning it into a float
# and returning it
def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# t is our token object
# we are getting the value, and turning it into an integer and returning it
def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Process variables
def t_NAME(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*' #the first character can be a-z, A-Z, or _. NOT A NUMBER,
    # the second character can be a number and any length
    t.type = 'NAME'
    return t

# Handle errors
def t_error(t):
    print("Illegal characters!")
    t.lexer.skip(1) #skip 1 token, the one that was illegal

lexer = lex.lex()

# removes ambiguity
precedence = (

    ('left', 'PLUS', 'MINUS'),
    ('left', 'MULTIPLY', 'DIVIDE')
)

#--------Testing lexer (recognizing input)-------------#
# Testing the lexer
# lexer.input("1+2")
#
# while True:
#     tok = lexer.token()
#     if not tok:
#         break
#     print(tok)

#---------------parser rules------------------#
# p is a tuple
def p_calc(p):
    '''
    calc : expression
         | var_assign
         | empty
    '''
    print(run(p[1]))

def p_var_assign(p):
    '''
    var_assign : NAME EQUALS expression
    '''
    p[0] = ('=', p[1], p[3])

# recursion solution, expression inside an expression
# ex. 10 + 5 * 4, 5*4 has more priority
def p_expression(p):
    '''

    expression : expression MULTIPLY expression
               | expression DIVIDE expression
               | expression PLUS expression
               | expression MINUS expression
    '''
    p[0] = (p[2], p[1], p[3])

def p_expression_int_float(p):
    '''
    expression : INT
               | FLOAT
    '''
    p[0] = p[1]

def p_expression_int_var(p):
    '''
    expression : NAME
    '''
    p[0] = ('var', p[1])

def p_error(p):
    print("Syntax error found!")

def p_empty(p):
    '''
     empty :
    '''

parser = yacc.yacc()

env = {} # an associative array

def run(p):
    global env
    if type(p) == tuple:
        if p[0] == '+':
            return run(p[1]) + run(p[2])
        elif p[0] == '-':
            return run(p[1]) - run(p[2])
        elif p[0] == '*':
            return run(p[1]) * run(p[2])
        elif p[0] == '/':
            return run(p[1]) / run(p[2])
        elif p[0] == '=':
            env[p[1]] = run(p[2])
            # print(env) # just used for debugging
        elif p[0] == 'var':
            if p[1] not in env:
                return 'Undeclared variable found!'
            else:
                return env[p[1]]
    else:
        return p

# Error handling, end of file error
while True:
    try:
        s = input('>> ')
    except EOFError:
        break
    parser.parse(s)
