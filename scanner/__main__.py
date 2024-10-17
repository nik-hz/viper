from scanner import Scanner


def print_tokens(tokens):
    # Format output with angle brackets <> instead of parentheses
    for token in tokens:
        print(f"<{token[0]}, {token[1]}>")


def run_scanner(code):
    scanner = Scanner()
    scanner.read_code(code)
    tokens = scanner.scan_token()  # Retrieve tokens
    print_tokens(tokens)  # This prints the tokens in the format asked <Token Type, Token Value>


if __name__ == "__main__":
    # List of test cases to run the scanner on
    test_cases = [
        "int :: x_a; list :: y; print(x) { z=42 }",
        "int :: z; int :: x_a; list :: y; print(x) { z=42 }",
        "int :: x_a; list_a :: y;",
        "int :: def func(int :: a, int :: b){ int :: c = a + b; return c;}",
        "str :: def say_hello_world(){ string :: text = 'hello world'; print(text);}",
    ]
    error_cases = [
        "str:: t = 'hello world!';",
        "int :: 123x_a;",
        "int :: a = @;",
    ]

    # Loop through each test case and run the scanner
    for idx, code in enumerate(test_cases):
        print(f"\nRunning test case {idx + 1}:")
        print(f"Code:\n {code}")
        run_scanner(code)
        print("-" * 40)  # Separator between test cases

    print("\n", "#" * 10, " Running error cases ", "#" * 10)

    for idx, code in enumerate(error_cases):
        print(f"\nRunning test case {idx + 1}:")
        print(f"Code:\n {code}")
        run_scanner(code)
        print("-" * 40)  # Separator between test cases
