import os
import sys

# Add scanner and parser paths to sys.path
scanner_path = os.path.abspath("./scanner")
if scanner_path not in sys.path:
    sys.path.insert(0, scanner_path)

parser_path = os.path.abspath("./parser")
if parser_path not in sys.path:
    sys.path.insert(0, parser_path)

typechecker_path = os.path.abspath("./typechecker")
if typechecker_path not in sys.path:
    sys.path.insert(0, typechecker_path)

generator_path = os.path.abspath("./generator")
if generator_path not in sys.path:
    sys.path.insert(0, generator_path)

from scanner import Scanner
from parser import Parser
from typechecker import TypeChecker
# from generator import ViperToPythonGenerator


class Pipeline:
    def __init__(self, dbg=False):
        self.dbg = dbg

    def tokenize(self, code):
        """Tokenize the input code using the scanner."""
        scanner = Scanner()
        scanner.read_code(code)
        tokens = scanner.scan_tokens()
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

        tc = TypeChecker(tokens)

        if not tc.check_types:
            print("Error with types!")
            return None
        else:
            print("Types ok!")

        return ast, None

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
                self.visualize_ast(child, level + 1, is_last=(i == len(ast[1:]) - 1))
        elif isinstance(ast, list):
            for i, item in enumerate(ast):
                self.visualize_ast(item, level, is_last=(i == len(ast) - 1))
        else:
            # Leaf node
            print(prefix(level, is_last) + str(ast))


def run_example(pipeline, input_code, expected_tokens=None, expected_ast=None, example_num=1):
    """Run a single example and display the results."""
    print(f"\n######################## VIPER EXAMPLE {example_num} ########################\n")
    print("Input code:")
    print(input_code)

    ast, code = pipeline.run(input_code, expected_tokens, expected_ast)

    print("\nFinal AST:")
    print(ast)

    print("\nAST Tree:")
    pipeline.visualize_ast(ast)

    # print("\n\nFinal Code")
    # print(code)

    # with open(f"examples/{file[:-3]}.py", "w") as f:
    #     f.write(code)


if __name__ == "__main__":
    pipeline = Pipeline(dbg=False)

    # Test cases for pa1 and pa2

    examples = [
        {
            "code": """
            int :: def calculation1():{ 
                float :: num = 1.5; 
                return num;
            };
            """,
        }
    ]

    # Run examples for pa2

    for i, example in enumerate(examples, start=1):
        run_example(
            pipeline,
            input_code=example["code"],
            # expected_tokens=example.get("tokens"),
            # expected_ast=example.get("ast"),
            example_num=i,
        )

    # Run examples through files end with .vp in examples folder
    # for file in os.listdir("./examples"):
    #     if file.endswith(".vp"):
    #         with open(f"examples/{file}", "r") as f:
    #             code = f.read()
    #             run_example(pipeline, input_code=code, example_num=file)
