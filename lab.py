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
    result = []
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

def evaluate(tree):
    """
    Given tree, a fully parsed expression, evaluates and outputs the result of
    evaluating expression according to the rules of the Scheme language.

    >>> evaluate(6.101)
    6.101
    >>> evaluate(['+', 3, ['-', 3, 1, 1], 2])
    6
    """
    raise NotImplementedError


# endregion
####################################################################
# region                      Built-ins
####################################################################

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


SCHEME_BUILTINS = {
    "+": lambda *args: sum(args),
    "*": builtin_mul,
}


# endregion
####################################################################
# region                       REPL
####################################################################

if __name__ == "__main__":
    #run_doctest = True
    #run_repl = False

    #if run_doctest:
        #_doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
        #doctest.run_docstring_examples(tokenize, globals(), optionflags=_doctest_flags)
        #doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests

    #if run_repl:
        #sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
        #SchemeREPL(sys.modules[__name__], verbose=True, repl_frame=None).cmdloop()

# endregion
    print(parse(['(', '+', '2', '(', '-', '5', '3', ')', '7', '8', ')']))