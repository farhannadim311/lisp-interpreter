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
    build_digit = ""
    build_char = ""
    comment = False
    for idx, char in enumerate(source):
        if(char.isdigit() == False and build_digit):
            res.append(build_digit)
            build_digit = ""
        if(char == ';'):
            comment = True
            continue
        if(char == '\n'):
            comment = False
            continue
        if(comment):
            continue
        if(char == ' '):
            continue
        if((char == '-' and source[idx + 1].isdigit()) or (char == '-' and source[idx + 1] == '.')):
            build_digit = build_digit + char
            continue
        if(char.isdigit() or char == '.'):
            build_digit = build_digit + char
            continue
        if(char.isalpha()):
            build_char += char
            continue
        if(build_char and char.isalpha() == False):
            res.append(build_char)
            build_char = ""
        res.append(char)
    if(build_digit):
        res.append(build_digit)
    
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
    raise NotImplementedError


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
    scheme_code = """
;add the numbers 2 and 3
(+ ; this expression
 2     ; spans multiple
 3  ; lines

)
"""

    print(tokenize(scheme_code))