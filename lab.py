"""
6.101 Lab:
LISP Interpreter Part 1
"""

#!/usr/bin/env python3

# import typing  # optional import
# import pprint  # optional import
import doctest
import os
import sys

from scheme_utils import (
    number_or_symbol,
    SchemeEvaluationError,
    SchemeNameError,
    # SchemeSyntaxError, # uncomment in LISP part 2!
    SchemeREPL,
)
sys.setrecursionlimit(20_000)
# NO ADDITIONAL IMPORTS!

def builtin_add(*args):
    return sum(args)

def builtin_mul(*args):
    """
    Computes the product of two or more evaluated numeric args.
    >>> builtin_mul(1, 2)
    2
    >>> builtin_mul(1, 2, -3)
    -6
    """
    if len(args) == 2:
        return args[0] * args[1]

    first_num, *rest_nums = args
    return first_num * builtin_mul(*rest_nums)

def builtin_sub(*args):
    if(len(args) == 1):
        return args[0]
    if(len(args) == 2):
        return args[0] - args[1]
    first_num, *rest_nums = args
    return first_num - builtin_sub(*rest_nums)


def builtin_div(*args):
    if(len(args) == 1):
        return args[0]
    if(len(args) == 2):
        return args[0] / args[1]
    first_num, *rest_nums = args
    return first_num / builtin_div(*rest_nums)


SCHEME_BUILTINS = {
    "+": builtin_add,
    "*": builtin_mul,
    "-": builtin_sub,
    "/": builtin_div
}

######################################################################
#region                          Frames
######################################################################

class InitialFrame:
    def __init__(self):
        self.variables = {
    "+": builtin_add,
    "*": builtin_mul,
    "-": builtin_sub,
    "/": builtin_div
}

    def __getitem__(self,key):
        if (key in self.variables):
            return self.variables[key]
        else:
            raise SchemeNameError



class Frame:
    def __init__(self, parent_frame = None):
        if(parent_frame == None):
            self.parent_frame = parent_frame
        self.variables = {}
    
    def __setitem__(self, key, value):
        self.variables[key] = value

    def __getitem__(self, key):
        if(key in self.variables):
            return self.variables[key]
        else:
            return self.parent_frame.__getitem__(key)
        
    def __contains__(self, key):
        try:
            self.__getitem__(key)
        except:
            return False
        else:
            return True

class Function(Frame):
    def __init__(self, exp, parameter, parent_frame = None):
        self.exp = exp
        if(parent_frame == None):
            self.parent_frame = make_initial_frame()
        else:
            self.parent_frame = parent_frame
        self.parameter = parameter
        self.variables = {}

    def bind(self, args):
        for i in range(len(args)):
            self.variables[self.parameter[i]] = args[i]

    def evaluate_func(self):
        return evaluate(self.exp, self)

        
        
def make_initial_frame():
    return Frame()


####################################################################
# region                  Tokenization
####################################################################

def tokenize(source):
    r"""
    Takes source, a string, and returns a list of individual token strings.
    Ignores comments and whitespace.

    >>> tokenize(' + ')
    ['+']
    >>> tokenize('-867.5309')
    ['-867.5309']
    >>> s = "((parse   these \n tokens) ;but ignore comments\n here );)"
    >>> tokenize(s)
    ['(', '(', 'parse', 'these', 'tokens', ')', 'here', ')']
    """
    res = []
    build_char = ""
    comment = False
    for idx, char in enumerate(source):
        #what are the cases
        #could be spaces or newlines
        #could be a string
        #could be a comment thats it
        if(char == ';'):
            comment = True
        if(char == ' ' or char == '\n'):
            if(char == '\n'):
                comment = False
            if(build_char):
                res.append(build_char)
                build_char = ""
            continue
        if(comment):
            continue
        if(char == '('):
            res.append(char)
        elif(char == ')'):
            if(build_char):
                res.append(build_char)
                build_char = ""
            res.append(char)
        else:
            build_char += char
        
    if(build_char):
        res.append(build_char)
    return res



# endregion
####################################################################
# region                  Parsing
####################################################################

def parse(tokens):
    """
    Parses a list of token strings and outputs a tree-like representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Hint: Make use of number_or_symbol imported from scheme_utils

    >>> parse(['+'])
    '+'
    >>> parse(['-867.5309'])
    -867.5309
    >>> parse(['(', '(', 'parse', 'these', 'tokens', ')', 'here', ')'])
    [['parse', 'these', 'tokens'], 'here']
    """
    recursive_call = 0
    def parse_expression(index, list_so_far): #example (['(', '+', '2', '(', '-', '5', '3', ')', '7', '8', ')'])
        nonlocal recursive_call
        parsed = number_or_symbol(tokens[index])
        if(index == len(tokens)):
            return list_so_far, index
        if(parsed != '(' and parsed != ')'):
            return parsed, index + 1
        if(tokens[index] == '(' or tokens[index] == ')'):
            if(tokens[index] == '('):
                list_so_far = []

            i = index + 1
            while(i < len(tokens)):
                char = tokens[i]
                if(char != ')'):
                    parse, idx = parse_expression(i , list_so_far)
                    recursive_call += 1
                    if(parse):
                        list_so_far.append(parse)
                    i = idx
                if(char == ')'):
                    return list_so_far, i + 1
                

    lst, idx = parse_expression(0, [])
    return lst


# endregion
####################################################################
# region                       Evaluation
####################################################################
f = ""
def evaluate(tree, frame = None):
    """
    Given tree, a fully parsed expression, evaluates and outputs the result of
    evaluating expression according to the rules of the Scheme language.

    >>> evaluate(6.101)
    6.101
    >>> evaluate(['+', 3, ['-', 3, 1, 1], 2])
    6
    """
    global f
    if(frame == None):
        frame = make_initial_frame()          
    def eval(index, ans_so_far, t): #example (['+', 3, ['-', 3, 1, 1], 2])
        key = ""
        op = ""
        recursive_call = 0
        op_symbol = ""
        if(type(t) != list):
            if(t in SCHEME_BUILTINS):
                return SCHEME_BUILTINS[t], index + 1
            if(type(t) == int or type(t) == float):
                return t, index + 1
            if(t == 'define'):
                return t, index + 1
            if(t == 'lambda'):
                return t, index + 1
            else:
                if(t in frame):
                    return frame[t], index + 1
                else:
                    raise SchemeNameError
        else:
            idx = 0
            ans_so_far = 0
            recursive_call = 0
            arguments = []
            while(idx < len(t)):
                recurse,idx = eval(idx, ans_so_far, t[idx]) 
                if(recurse == 'define'):
                    key = t[idx]
                    idx = idx + 1
                elif(recurse in SCHEME_BUILTINS.values()):
                    op = recurse
                    op_symbol = t[idx - 1]
                    if(key):
                        frame[key] = recurse
                        return recurse, index
                elif(recurse == 'lambda'):
                    args = t[1]
                    exp = t[2]
                    func = Function(exp, args, parent_frame=frame)
                    return func, idx 
                elif(isinstance(recurse, Function)):
                    op = recurse
                    op_symbol = t[idx - 1]
                    if(key):
                        frame[key] = recurse
                        return recurse, index
                else:
                    if(op_symbol == ""):
                        if(key):
                            frame[key] = recurse
                            return recurse, index
                        raise SchemeEvaluationError
                    if(op):
                        if(op == builtin_add):
                            ans_so_far = op(ans_so_far, recurse)
                        elif(op == builtin_mul):
                            if(recursive_call == 0):
                                ans_so_far = 1
                                ans_so_far = op(ans_so_far, recurse)
                            else:
                                ans_so_far = op(ans_so_far, recurse)
                        elif(op == builtin_sub):
                            if(recursive_call == 0):
                                ans_so_far = op(recurse)
                            else:
                                ans_so_far = op(ans_so_far, recurse)
                        elif(op == builtin_div):
                            if(recursive_call == 0):
                                ans_so_far = op(recurse)
                            else:
                                ans_so_far = op(ans_so_far, recurse)
                        elif(isinstance(op, Function)):
                            arguments.append(recurse)
                        recursive_call += 1
                
            if(arguments):
                op.bind(tuple(arguments))
                return op.evaluate_func(), index


            if(key):
                frame[key] = ans_so_far                 
        return ans_so_far, index + 1
    
    lst, idx = eval(0, 0, tree)
    f = frame
    return lst
    


# endregion
####################################################################
# region                       REPL
####################################################################

if __name__ == "__main__":
    #run_doctest = True
    #run_repl = True

    #if run_doctest:
        #_doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
        #doctest.run_docstring_examples(tokenize, globals(), optionflags=_doctest_flags)
        #doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    #if run_repl:
        #sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
        #SchemeREPL(sys.modules[__name__], verbose=True, repl_frame=make_initial_frame()).cmdloop()

# endregion
    print(evaluate(['define', 'addN', ['lambda', ['n'], ['lambda', ['i'], ['+', 'i', 'n']]]]))
    print(evaluate(['define', 'add7', ['addN', 7]], f))
    print(evaluate(['add7', 2], f))
    print(evaluate(['add7', [['addN', 3], [['addN', 19], 8]]], f))
  
