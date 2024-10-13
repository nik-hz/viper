# viper
Angel Cui: lc3542\
Nikolaus Holzer: nh2677

# Tokenizing

## Lexical grammar
We define six new token classes that the viper tokenizer recognizes.
1) ```<TYPE_DEC>```: type declaration token → ``"::"``
   1) The ```::``` token will be used to declare the type of a variable or return value. It serves as the separator between variable names and their type annotations.
   2) Example: ```int :: x = 1;```
2) ```<TYPE>```: Type tokens → ```“any”, “bool”, “callable”, “complex”, “dict”, “float”, “frozenset”, “int”, “list”, “optional”, “range”, “set”, “str”, “tuple”, “union”, “NoneType”```
   1) Tokens representing data types such as ```str, float, list, tuple``` are recognized and reserved. 
   2) Example ```list :: y = [];```
3) `<SEMICOLON>`: Semicolon → `";"`
   1) The semicolon terminates logical lines, offering an alternative to python's newline delinated logical lines.
   2) Example `print("Hello world!")`
4) `<LBRACE>`: Curly brace left → `"{"`
   1) Curly braces define blocks of code (such as function bodies or control flow syntax) and replaces pythons indentation based syntax.
   2) Example ```if a == True: {print("Hello world!");}```
5) `<RBRACE>`: Curly brace right → `"}"`
   1) Curly braces define blocks of code (such as function bodies or control flow syntax) and replaces pythons indentation based syntax.
   2) Example ```if a == True: {print("Hello world!");}```
6) `<VAR>`: Variable name → `"a"`
   1) Any variable name that come after `<TYPE> <TYPE_DEC>`.
   2) Example ```int :: a;```
7) `<PYTHON_CODE>`: All regular python tokens → special token for unchecked token, viper relies on python interpreter for correctness.

## Tokenizing Examples
