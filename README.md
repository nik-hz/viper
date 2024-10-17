# viper
Angel Cui: lc3542\
Nikolaus Holzer: nh2677

# For TAs: shell script to set up virtual environment and run 5 code examples for the scanner
1) Make sure you are in the viper directory.
2) Run ```chmod +x scanner.sh``` to ensure executable access to the shell script.
3) Run ```source ./scanner.sh```. This will activate a virtual environment called viper and set you up with required dependencies, and run the five code examples and return the outputs.

# Tokenizing

## Lexical grammar
We define six new token classes that the viper tokenizer recognizes.
1) ```<TYPE_DEC>```: type declaration token → ``"::"``
   1) The ```::``` token will be used to declare the type of a variable or return value. It serves as the separator between variable names and their type annotations.
   2) Example: ```int :: x = 1;```
2) ```<TYPE>```: Type tokens → ```“Any”, “bool”, “Callable”, “complex”, “dict”, “float”, “frozenset”, “int”, “list”, “Optional”, “range”, “set”, “str”, “tuple”, “Union”, “NoneType”```
   1) Tokens representing data types such as ```str, float, list, tuple``` are recognized and reserved. 
   2) Example ```list :: y = [];```
3) `<SEMICOLON>`: Semicolon → `";"`
   1) The semicolon terminates logical lines, offering an alternative to python's newline delinated logical lines.
   2) Example `print("Hello world!")`
4) `<LPAREN>`: Paren left → `"("`
   1) Left parenthesis
5) `<RPAREN>`: Paren right → `")"`
   1) Right parenthesis
6) `<LCBRACE>`: Curly brace left → `"{"`
   1) Curly braces define blocks of code (such as function bodies or control flow syntax) and replaces pythons indentation based syntax.
   2) Example ```if a == True: {print("Hello world!");}```
7) `<RCBRACE>`: Curly brace right → `"}"`
   1) Curly braces define blocks of code (such as function bodies or control flow syntax) and replaces pythons indentation based syntax.
   2) Example ```if a == True: {print("Hello world!");}```
8) `<VAR>`: Variable name → `"a"`
   1) Any variable name that come after `<TYPE> <TYPE_DEC>`.
   2) Example ```int :: a;```
9) `<FUNC>`: Function name → `"a"`
   1) Any function name that come after `<DEF>`.
10) `<DEF>`: Function definition → `"def"`
   1) Function definition
11) `<ASSIGN>`: Defines the `=` operator which assigns values to variables.
12) `<PYTHON_CODE>`: All regular python tokens → special token for unchecked token, viper relies on python interpreter for correctness.

## Error handling
Our lexical parser only handles errors directly related to malformed type declarations. 

We implement panic mode for handling malformed lexemes of the types that we are defining in our lexical grammar. The default error handling of our lexer is to pass lexemes through to the python code class, errors will then appear when attempting to run the python program.

## Tokenizing Examples

```Code:
 str :: def say_hello_world(){ string :: text = 'hello world'; print(text);}
[<TYPE, str>, <TYPE_DEC, ::>, <DEF, def>, <FUNC, say_hello_world>, <LPAREN, (>, <RPAREN, )>, <LBRACE, {>, <PYTHON_CODE, string>, <TYPE_DEC, ::>, <VAR, text>, <ASSIGN, =>, <PYTHON_CODE, 'hello>, <PYTHON_CODE, world'>, <SEMICOLON, ;>, <PYTHON_CODE, print>, <LPAREN, (>, <VAR, text>, <RPAREN, )>, <SEMICOLON, ;>, <RBRACE, }>]
```
# Development
For developpers, make sure you are in the viper directory. and run ```source ./setup.sh```. 
This should activate a virtual environment called viper and set you up with required dependencies.