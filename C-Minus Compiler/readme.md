# C-Minus One-pass Compiler

## Overview

This project implements the front-end of a compiler, featuring:

1. **Lexical Analyzer (Scanner)**: Tokenizes the input source code, identifying keywords, identifiers, symbols, numbers, and reporting lexical errors.
2. **Syntax Analyzer (LL(1) Parser)**: Parses the tokenized input according to an LL(1) grammar, generating a parse tree and reporting syntax errors.
3. **Semantic Analyzer**: Performs semantic checks, reporting issues like undefined variables, type mismatches, and supports recursive functions.
4. **Code Generator**: Generates intermediate code representation based on the parsed syntax, managing variables, functions, and scopes.
5. **Error Handling**: Captures and reports lexical, syntax, and semantic errors during the analysis phases.

### Key Features

- **Lexical Analysis**: Identifies tokens and handles lexical errors.
- **LL(1) Parsing**: Uses an LL(1) table and grammar rules for parsing.
- **Semantic Analysis**: Supports type checking, undefined variable detection, and recursive functions.
- **Intermediate Code Generation**: Outputs code in an intermediate representation.
- **Error Reporting**: Logs lexical, syntax, and semantic errors into respective files.

## Components

### 1. **Lexical Analyzer (`Scanner` Class)**

The scanner reads the input file and generates tokens such as:

- **Keywords** (`if`, `else`, `int`, etc.)
- **Symbols** (`+`, `-`, `=`, etc.)
- **Identifiers** (user-defined variable/function names)
- **Numbers** (integer literals)
- **Whitespace** (ignored except for newlines)
- **Lexical Errors** (invalid characters or sequences)

#### Files:
- `scanner.py`: Contains the `Scanner` class to process input and generate tokens.
- `input.txt`: The input source code file.
- `models.py`: Contains data models such as `Token` and `SymbolTable`.

### 2. **LL(1) Parser (`Parser` Class)**

The parser validates the tokenized input using an LL(1) parsing algorithm, based on the provided grammar. It constructs a parse tree and reports any syntax errors encountered.

#### Files:
- `parser.py`: Contains the `Parser` class implementing the LL(1) parsing algorithm.
- `grammar.txt`: The grammar file used by the parser.
- `fi_fo.json`: Contains precomputed first and follow sets for the grammar.

### 3. **Semantic Analyzer**

The semantic analyzer checks for errors such as:

- **Undefined variables**
- **Type mismatches**
- **Recursive function calls** (full support for recursion)

Semantic errors are logged in `semantic_errors.txt`.

#### Files:
- `code_gen.py`: Contains the `CodeGen` class responsible for code generation and semantic analysis.
  
### 4. **Code Generator (`CodeGen` Class)**

Generates intermediate code based on the parsed syntax, supporting:

- **Arithmetic operations**
- **Variable declarations**
- **Function definitions and recursive calls**
- **Control flow (`if`, `while`, `return`)**

### 5. **Error Handling**

All errors are logged in separate files:

- **`lexical_errors.txt`**: Logs lexical errors (invalid tokens).
- **`syntax_errors.txt`**: Logs syntax errors (unexpected tokens, missing tokens).
- **`semantic_errors.txt`**: Logs semantic errors (undefined variables, type mismatches).

## How to Run

### Prerequisites

- **Python 3.x**
- **AnyTree library**: Used for constructing the parse tree (`pip install anytree`).

### Running the Project with `Makefile`

1. **Place your source code** in `input.txt`.
2. **Use the Makefile** to run the project with the following command:

   ```bash
   make run
 ```
### Authors
- **Ava Cyrus** [@avacyrus10](https://github.com/avacyrus10)
- **Amirmohammad Eftekhar** [@amirmohammadeftekhar](https://github.com/amirmohammadeftekhar)