from scanner import Scanner


def print_list(tokens):
    t = []
    for token in tokens:
        t.append(f"<{token[0]}, {token[1]}>")
        if len(t) == 3:
            print(t)
            t = []


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
        "int :: x_a = 10; list :: y = range(0,x_a); for i in y: { print(i); }",
        "str :: def say_hello_world(){ string :: text = 'hello world'; print(text);}",
        "int :: def func(int :: a, int :: b):{ int :: c = a + b; return c;}",
        """
        from math import sqrt;
        
        NoneType :: def nthFib(int :: n):{
            int :: res = (((1+ sqrt (5))**n)-((1-sqrt(5)))**n)/(2**n*sqrt(5));
            print(res,'is',str(n)+'th fibonacci number');
        }
        nthFib(12);
        """,
        """
        # Function for nth Fibonacci number
        int :: def Fibonacci(int :: n):{
            if n<= 0:
                print("Incorrect input")
            # First Fibonacci number is 0
            elif n == 1:
                return 0
            # Second Fibonacci number is 1
            elif n == 2:{
                return 1;
            }
            else:{
                return Fibonacci(n-1)+Fibonacci(n-2);
            }
        }

        print(Fibonacci(10)) # our code even handles inline comments!
        """,
    ]

    error_cases = [
        "str:: t = 'hello world!';",
        "int :: 123x_a;",
        "int :: a = 123abc456;",
        "int :: a = @;",
    ]

    test = """
        from math import sqrt;
        
        NoneType :: def nthFib(int :: n):{
            int :: res = (((1+sqrt(5))**n)-((1-sqrt(5)))**n)/(2**n*sqrt(5));
            print(res,'is',str(n)+'th fibonacci number');
        }
        nthFib(12);
        """

    #run_scanner(test)
    #exit()

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
