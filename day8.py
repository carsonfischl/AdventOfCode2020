# This first section of code is a rewrite of Python's eval() function by SO user ubutnu

from __future__ import division
from pyparsing import (Literal, CaselessLiteral, Word, Combine, Group, Optional,
                       ZeroOrMore, Forward, nums, alphas, oneOf)
import math
import operator

__author__ = 'Paul McGuire'
__version__ = '$Revision: 0.0 $'
__date__ = '$Date: 2009-03-20 $'
__source__ = '''http://pyparsing.wikispaces.com/file/view/fourFn.py
http://pyparsing.wikispaces.com/message/view/home/15549426
'''
__note__ = '''
All I've done is rewrap Paul McGuire's fourFn.py as a class, so I can use it
more easily in other places.
'''


class NumericStringParser(object):
    '''
    Most of this code comes from the fourFn.py pyparsing example

    '''

    def pushFirst(self, strg, loc, toks):
        self.exprStack.append(toks[0])

    def pushUMinus(self, strg, loc, toks):
        if toks and toks[0] == '-':
            self.exprStack.append('unary -')

    def __init__(self):
        """
        expop   :: '^'
        multop  :: '*' | '/'
        addop   :: '+' | '-'
        integer :: ['+' | '-'] '0'..'9'+
        atom    :: PI | E | real | fn '(' expr ')' | '(' expr ')'
        factor  :: atom [ expop factor ]*
        term    :: factor [ multop factor ]*
        expr    :: term [ addop term ]*
        """
        point = Literal(".")
        e = CaselessLiteral("E")
        fnumber = Combine(Word("+-" + nums, nums) +
                          Optional(point + Optional(Word(nums))) +
                          Optional(e + Word("+-" + nums, nums)))
        ident = Word(alphas, alphas + nums + "_$")
        plus = Literal("+")
        minus = Literal("-")
        mult = Literal("*")
        div = Literal("/")
        lpar = Literal("(").suppress()
        rpar = Literal(")").suppress()
        addop = plus | minus
        multop = mult | div
        expop = Literal("^")
        pi = CaselessLiteral("PI")
        expr = Forward()
        atom = ((Optional(oneOf("- +")) +
                 (ident + lpar + expr + rpar | pi | e | fnumber).setParseAction(self.pushFirst))
                | Optional(oneOf("- +")) + Group(lpar + expr + rpar)
                ).setParseAction(self.pushUMinus)
        # by defining exponentiation as "atom [ ^ factor ]..." instead of
        # "atom [ ^ atom ]...", we get right-to-left exponents, instead of left-to-right
        # that is, 2^3^2 = 2^(3^2), not (2^3)^2.
        factor = Forward()
        factor << atom + \
            ZeroOrMore((expop + factor).setParseAction(self.pushFirst))
        term = factor + \
            ZeroOrMore((multop + factor).setParseAction(self.pushFirst))
        expr << term + \
            ZeroOrMore((addop + term).setParseAction(self.pushFirst))
        # addop_term = ( addop + term ).setParseAction( self.pushFirst )
        # general_term = term + ZeroOrMore( addop_term ) | OneOrMore( addop_term)
        # expr <<  general_term
        self.bnf = expr
        # map operator symbols to corresponding arithmetic operations
        epsilon = 1e-12
        self.opn = {"+": operator.add,
                    "-": operator.sub,
                    "*": operator.mul,
                    "/": operator.truediv,
                    "^": operator.pow}
        self.fn = {"sin": math.sin,
                   "cos": math.cos,
                   "tan": math.tan,
                   "exp": math.exp,
                   "abs": abs,
                   "trunc": lambda a: int(a),
                   "round": round,
                   "sgn": lambda a: abs(a) > epsilon and cmp(a, 0) or 0}

    def evaluateStack(self, s):
        op = s.pop()
        if op == 'unary -':
            return -self.evaluateStack(s)
        if op in "+-*/^":
            op2 = self.evaluateStack(s)
            op1 = self.evaluateStack(s)
            return self.opn[op](op1, op2)
        elif op == "PI":
            return math.pi  # 3.1415926535
        elif op == "E":
            return math.e  # 2.718281828
        elif op in self.fn:
            return self.fn[op](self.evaluateStack(s))
        elif op[0].isalpha():
            return 0
        else:
            return float(op)

    def eval(self, num_string, parseAll=True):
        self.exprStack = []
        results = self.bnf.parseString(num_string, parseAll)
        val = self.evaluateStack(self.exprStack[:])
        return val

# above is from ubutnu on Stack Overflow, an improved version of eval()

import re
from collections import Counter

nsp = NumericStringParser()
file = open("./day8.txt", mode="r")
lines = file.readlines()

accumulator = 0
j = int(0)
iterCounter = 0
coveredLines = []
totalCount = Counter()

#part 1

# while j <= int(len(lines)):
#     line = lines[int(j)].split()
#     totalCount = Counter(coveredLines)
#     print(totalCount)
#     if totalCount['jmp +102\n'] < 1: # determined the "checkpoint" for each cycle by repeatedly print the Counter object and looking for the smallest line that kept iterating (it was in the loop) but was greater than 1.
#         if lines[int(j)].startswith("nop"):
#             #print("nopped: " + lines[int(j)])
#             j += 1
#             coveredLines.append(lines[int(j)])
#         elif lines[int(j)].startswith("jmp"):
#             #print("jumped: " + line[1])
#             x = re.findall(r'\d+', line[1])
#             k = int(x[0])
#             oper = list(line[1])
#             oper = oper[0]
#             thisStr = str(j) + str(''.join(oper)) + str(x[0])
#             coveredLines.append(lines[int(j)])
#             j = nsp.eval(thisStr)
#         elif lines[int(j)].startswith("acc"):
#             #print("accumulated: " + line[1])
#             x = re.findall(r'\d+', line[1])
#             oper = list(line[1])
#             oper = oper[0]
#             thisStr = str(accumulator) + str(''.join(oper)) + str(x[0])
#             accumulator = nsp.eval(thisStr)
#             coveredLines.append(lines[int(j)])
#             j += 1
#     else:
#         print(lines[int(j)])
#         break
# 
# print(accumulator)

# part 2
badLines = list() # the second last member in this list *should* be the correct value (the index can change depending on the number of repeat values in your loop; jmp -309 for me

while j <= int(len(lines)):
    print(accumulator) # this is still going to give an "index out of bounds" error but the final number printed will be the correct answer once you change the above
    line = lines[int(j)].split()
    if lines[int(j)].startswith("nop"):
        if lines[int(j)] not in badLines:
            print("added new nop")
            badLines.append(lines[int(j)])
        print("nopped: " + lines[int(j)])
        j += 1
        print(badLines)
    elif lines[int(j)].startswith("jmp"):
        if lines[int(j)] not in badLines:
            print("added new jmp")
            badLines.append(lines[int(j)])
        print("jumped: " + line[1])
        x = re.findall(r'\d+', line[1])
        k = int(x[0])
        oper = list(line[1])
        oper = oper[0]
        thisStr = str(j) + str(''.join(oper)) + str(x[0])
        j = nsp.eval(thisStr)
        print(badLines)
    elif lines[int(j)].startswith("acc"):
#         print("accumulated: " + line[1])
        x = re.findall(r'\d+', line[1])
        oper = list(line[1])
        oper = oper[0]
        thisStr = str(accumulator) + str(''.join(oper)) + str(x[0])
        accumulator = nsp.eval(thisStr)
        j += 1
    else:
        print(lines[int(j)])
        break

print(accumulator)
