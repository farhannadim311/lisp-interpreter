"""
6.101 Lab:
LISP Interpreter Part 2
"""

# KEEP THE ABOVE LINES INTACT, BUT REPLACE THIS COMMENT WITH ALL THE CODE IN
# THE lab.py FILE FROM THE lisp_1 LAB, WHICH SHOULD BE THE STARTING POINT FOR
# THIS LAB.
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
    SchemeSyntaxError, # uncomment in LISP part 2!
    SchemeREPL,
)
sys.setrecursionlimit(20_000)
# NO ADDITIONAL IMPORTS!

class EmptyList:
    def __init__(self):
        self.tup = ()

    def __eq__(self, other):
        if(not(isinstance(other, EmptyList))):
            return False
        return self.tup == other.tup
    
class Pair:
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __str__(self):
        return f"{self.car=}, {self.cdr=}"


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
    if len(args) == 1:
        return -args[0]
    return args[0] - sum(args[1:])

def builtin_div(*args):
    if len(args) == 1:
        return args[0]
    result = args[0]
    for x in args[1:]:
        result /= x
    return result

def equal(*args):
    if(len(args) < 2):
        raise SchemeEvaluationError
    else:
        for i in range(len(args) - 1):
            if(args[i] != args[i + 1]):
                return False
        return True

def greaterthan(*args):
    if(len(args) < 2):
        raise SchemeEvaluationError
    else:
        for i in range(len(args) - 1):
            if(args[i] <= args[i + 1]):
                return False
        return True

def greaterthaneq(*args):
    if(len(args) < 2):
        raise SchemeEvaluationError
    else:
        for i in range(len(args) - 1):
            if(args[i] < args[i + 1]):
                return False
        return True

def lessthan(*args):
    if(len(args) < 2):
        raise SchemeEvaluationError
    else:
        for i in range(len(args) - 1):
            if(args[i] >= args[i + 1]):
                return False
        return True


def lessthaneq(*args):
    if(len(args) < 2):
        raise SchemeEvaluationError
    else:
        for i in range(len(args) - 1):
            if(args[i] > args[i + 1]):
                return False
        return True


def scheme_not(*args):
    if(len(args) != 1):
        raise SchemeEvaluationError
    else:
        if(args[0] == False):
            return True
        else:
            return False

def cons(*args):
    if(len(args) != 2):
        raise SchemeEvaluationError
    else:
        return Pair(args[0], args[1])
    
def car(*args):
    if(len(args) != 1):
        raise SchemeEvaluationError
    if(not (isinstance(args[0], Pair))):
        raise SchemeEvaluationError
    else:
        return args[0].car

def cdr(*args):
    if(len(args) != 1):
        raise SchemeEvaluationError
    if(not (isinstance(args[0], Pair))):
        raise SchemeEvaluationError
    else:
        return args[0].cdr
    
def scheme_list(*args):
    if(len(args) == 0):
        return EmptyList()
    elif(len(args) == 1):
        return cons(args[0], EmptyList())
    else:
        return cons(args[0], scheme_list(*args[1:]))
    

def is_list(obj):
    if(not(isinstance(obj, Pair)) and not(isinstance(obj, EmptyList))):
        return False
    else:
        if(isinstance(obj, EmptyList)):
            return True
        is_true = is_list(obj.cdr)
        return is_true

def length_list(list):
    if(is_list(list) == '#f'):
        raise SchemeEvaluationError
    count = 0
    def find_length(list):
        nonlocal count
        if(isinstance(list, EmptyList)):
            return count
        else:
            count += 1
            find_length(list.cdr)
    find_length(list)
    return count


def scheme_list_ref(cons, index):
    if(index == 0):
        try:
            return cons.car
        except:
            raise SchemeEvaluationError
    else:
        return scheme_list_ref(cons.cdr, index - 1)

def append(*args):
    #no args
    if(len(args) == 0):
        return EmptyList()
    elif(len(args) == 1):
        if(isinstance(args[0], EmptyList)):
            return args[0]
        if(is_list(args[0]) == False):
            raise SchemeEvaluationError
        return Pair(args[0].car, append(args[0].cdr))
    else:
        if(isinstance(args[0], EmptyList)):
            return append(*args[1:])
        return Pair(args[0].car, append(args[0].cdr, *args[1:]))
    
def begin(*args):
    return args[-1]
    


        



SCHEME_BUILTINS = {
    "+": builtin_add,
    "*": builtin_mul,
    "-": builtin_sub,
    "/": builtin_div,
    "#t": True,
    "#f": False,
    "equal?": equal,
    ">" : greaterthan,
    ">=" :greaterthaneq,
    "<" : lessthan,
    "<=": lessthaneq,
    "not" : scheme_not,
    "cons": cons,
    "car": car,
    "cdr": cdr,
    "list": scheme_list,
    "list?": is_list,
    "length": length_list,
    "list-ref": scheme_list_ref,
    "append" : append,
    "begin": begin,

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
    "/": builtin_div,
    "#t": True,
    "#f": False,
    "equal?": equal,
    ">" : greaterthan,
    ">=" :greaterthaneq,
    "<" : lessthan,
    "<=": lessthaneq,
    "not" : scheme_not,
    "cons": cons,
    "car": car,
    "cdr": cdr,
    "list": scheme_list,
    "list?": is_list,
    "length": length_list,
    "list-ref": scheme_list_ref,
    "append" : append,
    "begin": begin,

}

    def __getitem__(self,key):
        if (key in self.variables):
            return self.variables[key]
        else:
            raise SchemeNameError

    def __setitem__(self, key, value):
        self.variables[key] = value

    def delete_item(self, item):
        if(item not in self.variables):
            raise SchemeNameError
        else:
            val = self.variables[item]
            del self.variables[item]
            return val



class Frame:
    def __init__(self, parent_frame = None):
        if(parent_frame == None):
            self.parent_frame = parent_frame
        else:
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
        
    
    def bind(self, key, val):
        if(len(key) != len(val)):
            raise SchemeEvaluationError
        else:
            for k in range(len(key)):
                self.variables[key[k]] = val[k]

    def delete_item(self, item):
        if(item not in self.variables):
            raise SchemeNameError
        else:
            val = self.variables[item]
            del self.variables[item]
            return val

    def update(self, key, val):
        if(key in self.variables):
            self.variables[key] = val
        else:
            try:
                self.parent_frame.update(key , val)
            except:
                raise SchemeNameError



        

class Function(Frame):
    def __init__(self, exp, parameter, parent_frame = None):
        self.exp = exp
        if(parent_frame == None):
            self.parent_frame = make_initial_frame()
        else:
            self.parent_frame = parent_frame
        self.parameter = parameter
        self.variables = {}


    def evaluate_func(self,args):
        new_frame = Frame(parent_frame=self.parent_frame)
        new_frame.bind(self.parameter, args)
        return evaluate(self.exp, new_frame)
    def copy(self):
        f = Function(self.exp, self.parameter.copy(), self.parent_frame)
        return f

    def __str__(self):
        return f"{self.parameter=}, {self.parent_frame=}, {self.exp=}, {self.variables=}"

        
        
def make_initial_frame():
    return Frame(InitialFrame())





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

def is_valid_token(tokens):
    stack = []
    in_expression = False
    count = 0
    if(len(tokens) == 1 and (tokens[0] != '(' and tokens[0] != ')') ):
        return True
    for char in tokens:
        if(in_expression == False and char != '('):
            return False
        if(char == '('):
            if(in_expression == False and count != 0):
                return False
            stack.append('(')
            in_expression = True
        elif(char == ')'):
            if(stack):
                stack.pop()
                if(not stack):
                    in_expression = False
            else:
                return False
        count += 1
    return not(stack)





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
    if(not(is_valid_token(tokens))):
        raise SchemeSyntaxError
    def parse_expression(index, list_so_far): #example (['(', '+', '2', '(', '-', '5', '3', ')', '7', '8', ')'])
        parsed = number_or_symbol(tokens[index])
        if(index == len(tokens)):
            return list_so_far, index
        if((index + 1) < len(tokens) and tokens[index] == '(' and tokens[index  + 1] == ')'):
            return [], index + 2
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
                    if(parse is not None):
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
    if frame is None:
        frame = make_initial_frame()
    
    # Case 1: number
    if isinstance(tree, (int, float)):
        return tree
    
    # Case 2: symbol
    if isinstance(tree, str):
        return frame[tree]
    
     #Case 8 : Handling Empty List
    if(tree == []):
        return EmptyList()
    
    if(tree[0] == 'del'):
        var = tree[1]
        if(type(var) != str):
            raise SchemeEvaluationError
        else:
            return frame.delete_item(var)
    
    if(tree[0] == 'let'):
        new_frame = Frame(frame)
        for t in tree[1]:
            val = evaluate(t[1], frame)
            new_frame[t[0]] = val
        return evaluate(tree[2], new_frame)


    if(tree[0] == 'set!'):
        val = evaluate(tree[2],frame)
        frame.update(tree[1], val)
        return val





    # Case 3: define
    if tree[0] == 'define':
        if(type(tree[1]) != list):
            val = evaluate(tree[2], frame)
            frame[tree[1]] = val
            return val
        else:
            name = tree[1][0]
            params = tree[1][1:]
            body = tree[2]
            frame[name] = Function(body, params, frame)
            return frame[name]

    
    # Case 4: lambda
    if tree[0] == 'lambda':
        return Function(tree[2], tree[1], frame)
    
    #Case 5: if
    if(tree[0] == 'if'):
        predicate = evaluate(tree[1], frame)
        if(predicate):
            return evaluate(tree[2], frame)
        else:
            return evaluate(tree[3], frame)

    #Case 6: Handling And
    if(tree[0] == 'and'):
        for predicates in tree[1:]:
            if(evaluate(predicates, frame) == False):
                return False
        return True
    
    #Case 7 : Handling Or
    if(tree[0] == 'or'):
        for predicates in tree[1:]:
            if(evaluate(predicates, frame) == True):
                return True
        return False
    

    
    # Case 9: function call
    func = evaluate(tree[0], frame)
    args = [evaluate(arg, frame) for arg in tree[1:]]
    if isinstance(func, Function):
        return func.evaluate_func(args)
    elif callable(func):
        try:
            return func(*args)
        except:
            raise SchemeEvaluationError
    else:
        raise SchemeEvaluationError
    
def evaluate_file(filename, frame = None):
    if (frame is None):
        frame = make_initial_frame()
    with open(filename, encoding='utf-8') as f:
        read_data = f.read()
        parsed = parse(tokenize(read_data))
        result = evaluate(parsed, frame)
        print("parsed:", parsed)
        print("result:", result)
        return result



# endregion
####################################################################
# region                       REPL
####################################################################

if __name__ == "__main__":
    #run_doctest = True
    run_repl = True

    #if run_doctest:
        #_doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
        #doctest.run_docstring_examples(tokenize, globals(), optionflags=_doctest_flags)
        #doctest.testmod(optionflags=_doctest_flags)  # runs ALL doctests
    frame = make_initial_frame()
    if(len(sys.argv) > 1):
        for files in range(1, len(sys.argv)):
            evaluate_file(sys.argv[files], frame)

    if run_repl:
        sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
        SchemeREPL(sys.modules[__name__], verbose=True, repl_frame=frame).cmdloop()

# endregion
    # 1. Initialize your Global Frame (adjust class name if yours is different)

# 2. Define the 'ham' variable in the global scope
    #evaluate(['define', 'ham', 42])

# 3. Define the 'bacon' function with its 100 nested lambdas
# Note: This is an IIFE (Immediately Invoked Function Expression) pattern
    # 1. Initialize your Global Frame (adjust class name if yours is different)


# 2. Define the 'ham' variable in the global scope
    # Build the nested lambda expression programmatically
    #global_frame = Frame()
    #body = 'ham'
    #for i in range(101):
        #body = [['lambda', [f'var{i}'], body], i]

    #expressions = [
        #['define', 'ham', 42],
        #['define', 'bacon', ['lambda', ['var100'], body]],
        #['bacon', 7],
    #]

#for i, exp in enumerate(expressions):
    #print(f"\n--- Line {i+1} ---")
    #result = evaluate(exp, global_frame)
    #print(f"  RESULT: {result}")
    #print(evaluate(['define', ['call', 'x'], ['x']]))
    #print(evaluate(['call', ['lambda', [], 2]], f))
    #global_frame = Frame()

    #expressions = [
    #['define', 'apply', ['lambda', ['f'], ['lambda', ['x'], ['f', 'x']]]],
    #[['apply', ['lambda', ['n'], ['+', 'n', 'n']]], 5],
#]

    #for i, exp in enumerate(expressions):
        #print(f"\n--- Line {i+1}: {exp} ---")
        #result = evaluate(exp, global_frame)
        #print(f"  RESULT: {result}")
        #print(evaluate(['define', 'x', ['-', ['define', 'y', ['*', 2, ['define', 'z', ['+', ['define', 'a', 3], 1]]]], 1]]))
        #print(evaluate(['if', '#t', 7, 8]))
        #print(evaluate(['if', ['list?', 7], 1, 0]))
        #print(evaluate(['define', 'x', ['list', 7, 9, 3, 2]], frame))
        #print(evaluate(['define', 'minus', ['lambda', ['n'], ['-', 0, 'n']]],frame))
        #print(evaluate(['map', 'minus', 'x'], frame))
        #print(evaluate(['define', 'x', 7], frame))
        #print(evaluate(['define', 'y', 8], frame))
        #print(evaluate(['define', ['square', 'x'], ['*', 'x', 'x']],frame))
        #print(evaluate(['square', ['del', 'x']], frame))
    #print(evaluate(['define', 'z', 5],frame))
    #print(evaluate(['let', [['x', 5], ['y', 3]], ['+', 'x', 'y', 'z']], frame))
    #print(evaluate(['define', 'y', 10], frame))
    #print(evaluate([['lambda', ['z'], ['set!', 'y', ['+', 'z', 'y']]], 9], frame))