#-----------Library Info-----------#
# We use Lex and Yacc which are libraries for parsing
# lex - laxer generator
# yacc - parser generator. tokenises a string
#-------User Case------#
#   1   +   2
# 1 => Int(1)
# + => Plus
# 2 => Int(2)
# then creates a tree
# we will pass it to a functions
# it will run the tokens that yacc creates

#----------Code Begins------------#
import ply.lex as lex
import ply.yacc as yacc
import sys

# Tell Lax what tokens are valid
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
