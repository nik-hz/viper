import os
import sys

# Add scanner and parser paths to sys.path
scanner_path = os.path.abspath("./scanner")
if scanner_path not in sys.path:
    sys.path.insert(0, scanner_path)

parser_path = os.path.abspath("./parser")
if parser_path not in sys.path:
    sys.path.insert(0, parser_path)

from scanner import Scanner
from parser import Parser

class Pipeline:
    def __init__(self, dbg=False):
        self.dbg = dbg

    def tokenize(self, code):
        """Tokenize the input code using the scanner."""
        scanner = Scanner()
        scanner.read_code(code)
        tokens = scanner.scan_token()
        return tokens

    def print_tokens(self, tokens):
        """Format and print tokens."""
        for token in tokens:
            print(f"<{token[0]}, {token[1]}>")

    def parse(self, tokens):
        """Parse tokens using the parser."""
        parser = Parser(tokens, dbg=self.dbg)
        ast = parser.parse()
        return ast

    def run(self, code, expected_tokens=None, expected_ast=None):
        """Run the pipeline: tokenize, optionally assert tokens, and parse."""
        tokens = self.tokenize(code)
        
        print("\nTokens:")
        self.print_tokens(tokens)

        # Compare tokens with expected tokens
        if expected_tokens is not None:
            actual_tokens = [f"<{t[0]}, {t[1]}>" for t in tokens]
            if actual_tokens == expected_tokens:
                print("\nTokens match the expected output.")
            else:
                print("\nTokens do NOT match the expected output!")
                print(f"Expected: {expected_tokens}")
                print(f"Got:      {actual_tokens}")

        ast = self.parse(tokens)

        # Compare AST with expected AST
        if expected_ast is not None:
            if ast == expected_ast:
                print("\nAST matches the expected output.")
            else:
                print("\nAST does NOT match the expected output!")
                print(f"Expected: {expected_ast}")
                print(f"Got:      {ast}")

        return ast
    
    def visualize_ast(self, ast, level=0, is_last=True):
        """Visualize AST as a tree structure matching the requested format."""
        def prefix(level, is_last):
            """Create tree branch prefixes."""
            if level == 0:
                return ""
            return "│   " * (level - 1) + ("└── " if is_last else "├── ")

        if isinstance(ast, tuple):
            print(prefix(level, is_last) + str(ast[0]))  # Print the current node
            for i, child in enumerate(ast[1:]):
                self.visualize_ast(
                    child,
                    level + 1,
                    is_last=(i == len(ast[1:]) - 1)
                )
        elif isinstance(ast, list):
            for i, item in enumerate(ast):
                self.visualize_ast(
                    item,
                    level,
                    is_last=(i == len(ast) - 1)
                )
        else:
            # Leaf node
            print(prefix(level, is_last) + str(ast))

def run_example(pipeline, input_code, expected_tokens=None, expected_ast=None, example_num=1):
    """Run a single example and display the results."""
    print(f"\n######################## VIPER EXAMPLE {example_num} ########################\n")
    print("Input code:")
    print(input_code)
    
    ast = pipeline.run(input_code, expected_tokens, expected_ast)

    print("\nFinal AST:")
    print(ast)

    print("\nAST Tree:")
    pipeline.visualize_ast(ast)

if __name__ == "__main__":
    pipeline = Pipeline(dbg=False)

    # Test cases
    examples = [
        {
            "code": """
            int :: x_a = 10; 
            list :: y = range(0,x_a); 
            for i in y:{ 
                print(i); 
            };
            """,
            "tokens": [
                "<TYPE, int>",
                "<TYPE_DEC, ::>",
                "<VAR, x_a>",
                "<ASSIGN, =>",
                "<PYTHON_CODE, 10>",
                "<SEMICOLON, ;>",
                "<TYPE, list>",
                "<TYPE_DEC, ::>",
                "<VAR, y>",
                "<ASSIGN, =>",
                "<TYPE, range>",
                "<LPAREN, (>",
                "<PYTHON_CODE, 0>",
                "<PYTHON_CODE, ,>",
                "<VAR, x_a>",
                "<RPAREN, )>",
                "<SEMICOLON, ;>",
                "<PYTHON_CODE, for>",
                "<PYTHON_CODE, i>",
                "<PYTHON_CODE, in>",
                "<PYTHON_CODE, y:>",
                "<LBRACE, {>",
                "<PYTHON_CODE, print>",
                "<LPAREN, (>",
                "<PYTHON_CODE, i>",
                "<RPAREN, )>",
                "<SEMICOLON, ;>",
                "<RBRACE, }>",
                "<SEMICOLON, ;>"
            ],
            "ast": None,
        },
        {
            "code": """
            str :: def say_hello_world():{
                string :: text = 'hello world'; 
                print(text);
            };
            """,
            "tokens":[
                "<TYPE, str>",
                "<TYPE_DEC, ::>",
                "<DEF, def>",
                "<FUNC, say_hello_world>",
                "<LPAREN, (>",
                "<RPAREN, )>",
                "<PYTHON_CODE, :>",
                "<LBRACE, {>",
                "<PYTHON_CODE, string>",
                "<TYPE_DEC, ::>",
                "<VAR, text>",
                "<ASSIGN, =>",
                "<PYTHON_CODE, 'hello>",
                "<PYTHON_CODE, world'>",
                "<SEMICOLON, ;>",
                "<PYTHON_CODE, print>",
                "<LPAREN, (>",
                "<VAR, text>",
                "<RPAREN, )>",
                "<SEMICOLON, ;>",
                "<RBRACE, }>",
                "<SEMICOLON, ;>",
            ],
            "ast": None,  # No assertion for this case
        },
        {
            "code": """
            int :: def func(int :: a, int :: b):{
                int :: c = a + b; 
                return c;
            };
            """,
            "tokens": [
                "<TYPE, int>",
                "<TYPE_DEC, ::>",
                "<DEF, def>",
                "<FUNC, func>",
                "<LPAREN, (>",
                "<TYPE, int>",
                "<TYPE_DEC, ::>",
                "<VAR, a>",
                "<PYTHON_CODE, ,>",
                "<TYPE, int>",
                "<TYPE_DEC, ::>",
                "<VAR, b>",
                "<RPAREN, )>",
                "<PYTHON_CODE, :>",
                "<LBRACE, {>",
                "<TYPE, int>",
                "<TYPE_DEC, ::>",
                "<VAR, c>",
                "<ASSIGN, =>",
                "<VAR, a>",
                "<OP, +>",
                "<VAR, b>",
                "<SEMICOLON, ;>",
                "<PYTHON_CODE, return>",
                "<VAR, c>",
                "<SEMICOLON, ;>",
                "<RBRACE, }>",
                "<SEMICOLON, ;>",
            ],
            "ast": None,  # No assertion for this case
        },
        {
            "code": """
            int :: x_a = 10;
            """,
            "tokens": [
                "<TYPE, int>",
                "<TYPE_DEC, ::>",
                "<VAR, x_a>",
                "<ASSIGN, =>",
                "<PYTHON_CODE, 10>",
                "<SEMICOLON, ;>",
            ],
            "ast": None,  # No assertion for this case
        },
        {
            "code": """
            from math import sqrt;
        
            NoneType :: def nthFib(int :: n):{
                int :: res = (((1+sqrt(5))**n)-((1-sqrt(5)))**n)/(2**n*sqrt(5));
                print(res,'is',str(n)+'th fibonacci number');
            }
            nthFib(12);
            """,
            "tokens": None,
            "ast": None,  # No assertion for this case
        }
    ]

    # Run examples
    for i, example in enumerate(examples, start=1):
        run_example(
            pipeline,
            input_code=example["code"],
            expected_tokens=example.get("tokens"),
            expected_ast=example.get("ast"),
            example_num=i,
        )
