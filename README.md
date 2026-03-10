# LISP Interpreter Part 2

This project is an implementation of a subset of the LISP programming language in Python, created as part of the 6.1010 coursework. It extends the foundational interpreter built in Part 1 by adding support for advanced language features.

## Features Supported
The interpreter is capable of tokenizing, parsing, and evaluating Scheme/LISP code. It includes proper environment (frame) management and the following built-in operations and features:
- **Math Operations**: Addition (`+`), subtraction (`-`), multiplication (`*`), explicit division (`/`)
- **Logical Operations**: Boolean literals (`#t`, `#f`), logical comparisons (`equal?`, `<`, `<=`, `>`, `>=`), and logical evaluations (`and`, `or`, `not`)
- **Variable Definitions**: Global binding and environment frame hierarchy (`define`, `set!`, `del`)
- **Functions**: First-class functions via `lambda` and named functions via `define`, with proper lexical scoping.
- **Lists and Pairs**: Standard LISP primitives `cons`, `car`, `cdr`, `list`, `list?`, `length`, `list-ref`, and `append`.
- **Conditionals**: The `if` special form for branching logic.
- **Local Bindings**: The `let` special form for creating local variable scope.

## Running the Interpreter
To start the read-eval-print loop (REPL):
```bash
python3 lab.py
```

You can also evaluate a given Scheme file directly from the command line:
```bash
python3 lab.py filename.scm
```

## Testing
The project includes several tests via `pytest`. To run tests:
```bash
pytest test.py
```
