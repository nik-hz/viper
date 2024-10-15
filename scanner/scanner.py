from dfa import DFA


class Scanner:
    """Finite automata for scanning Viper code"""

    def __init__(self):
        """
        Initializes the scanner with the input code. No args, the scanner should be called on an input string.
        """
        # I/O
        self.code = ""  # original string of code
        self.chars = []  # list of chars from self.code
        self.tokens = []  # list of final tokens

        # pointers
        self.lexemeBegin = 0
        self.forward = 0
        self.sentinel = None

        # states (finite automata states)
        self.state = "START"
        self.accept_states = {
            "SEMICOLON",
            "LBRACE",
            "RBRACE",
            "TYPE_DEC",
            "TYPE",
            "VAR",
            "PYTHON_CODE",
            "LPAREN",
            "RPAREN",
            "DEF",
        }

        # Updated list of reserved type tokens
        self.type_tokens = [
            "Any",
            "bool",
            "Callable",
            "complex",
            "dict",
            "float",
            "frozenset",
            "int",
            "list",
            "Optional",
            "range",
            "set",
            "str",
            "tuple",
            "Union",
            "NoneType",
            "def",
        ]

        # keep track of vars that have been defined already
        # This should be fine even without scope I
        self.defined_vars = []
        self.defined_funcs = []

    def read_code(self, input_code: str) -> None:
        """
        Reads the input code and prepares it for scanning as self.code
        and splits self.code char by char as self.chars.

        Args:
            input_code (str): The code to be scanned
        Returns:
            None
        """
        self.code = input_code
        self.chars = list(self.code)
        self.sentinel = len(self.chars)

    def next_char(self) -> str:
        """
        Retrieves the next char from the code.

        Returns:
            str: The next char as a string of length 1.
        """
        if self.forward < self.sentinel:
            char = self.chars[self.forward]
            self.forward += 1
            return char
        else:
            return ""  # End of file

    def end_of_file(self) -> bool:
        """
        Checks if the current token is the end of file.

        Returns:
            bool: True if the current token is the end of file, False otherwise.
        """
        return self.forward >= self.sentinel

    def reset_scanner(self) -> None:
        """
        Resets the scanner to the beginning of the code.

        Returns:
            None
        """
        self.lexemeBegin = 0
        self.forward = 0

    def handle_single_char(self, char: str) -> None:
        """
        Helper function to handle single-character tokens like ;, {, }.

        Args:
            char (str): The single character to process.

        Returns:
            None
        """
        if char == ";":
            self.tokens.append(("SEMICOLON", ";"))
        elif char == "{":
            self.tokens.append(("LBRACE", "{"))
        elif char == "}":
            self.tokens.append(("RBRACE", "}"))
        elif char == "(":
            self.tokens.append(("LPAREN", "("))
        elif char == ")":
            self.tokens.append(("RPAREN", ")"))
        elif char == ",":
            self.tokens.append(("PYTHON_CODE", ","))

    def handle_type_declaration(self) -> None:
        """
        Handle type declaration for "::".
        """
        next_char = self.next_char()
        if next_char == ":":
            self.tokens.append(("TYPE_DEC", "::"))
        else:
            # TODO: Add error handling for unexpected characters
            raise ValueError(f"Unexpected character '{next_char}' after ':'")

    def handle_type_token(self, lexeme: str) -> None:
        """
        Handle reserved type tokens like "Any", "bool", etc.

        Args:
            lexeme (str): The current lexeme being scanned.
        """
        if lexeme == "def":
            self.tokens.append(("DEF", lexeme))
        elif lexeme in self.type_tokens:
            self.tokens.append(("TYPE", lexeme))

    def handle_variable(self, lexeme: str) -> None:
        """
        Handle variable name token after type declaration.
        """
        self.tokens.append(("VAR", lexeme))
        self.defined_vars.append(lexeme)

    def handle_python_code(self, lexeme: str) -> None:
        """
        Handle Python code as an unchecked token.
        """
        if lexeme in self.defined_vars:
            self.tokens.append(("VAR", lexeme))
        elif lexeme in self.defined_funcs:
            self.tokens.append(("FUNC", lexeme))
        else:
            self.tokens.append(("PYTHON_CODE", lexeme))

    def handle_func_token(self, lexeme):
        self.defined_funcs.append(lexeme)
        self.tokens.append(("FUNC", lexeme))

    def scan_token(self) -> list:
        """
        Scans the input code for specific tokens using finite automata transitions.
        Handles tokens for `;`, `{`, `}`, `::`, type tokens, variable names, and Python code.

        Returns:
            list: A list of tokens in the format <Token Type, Token Value>.
        """
        lexeme = ""
        expect_var = False  # This flag will be set to True after encountering TYPE_DEC
        expect_func = False
        while not self.end_of_file():

            char = self.next_char()

            if char.isspace():
                continue

            if self.state == "START":
                if char in [";", "{", "}", "(", ")", ","]:
                    self.handle_single_char(char)
                elif char == ":":
                    self.handle_type_declaration()
                    expect_var = True  # After TYPE_DEC, the next token is expected to be a variable
                elif char.isalnum() or char == "_":  # Collect alphanumeric variables/types
                    lexeme += char
                    while not self.end_of_file():
                        next_char = self.next_char()
                        if next_char in ["{", "}", ";", "(", ")", ","]:  # TODO: Should we add ::?
                            self.forward -= 1  # Unread the non-alphanumeric, non-space character
                            break
                        elif (
                            next_char.isspace()
                        ):  # Handle space as separator for maximal munch, stop collecting lexeme
                            break
                        else:
                            lexeme += next_char
                    # If the previous token was TYPE_DEC, this must be a VAR unless it's a type keyword
                    if expect_var:
                        if lexeme in self.type_tokens:  # If it's a type token, handle it as a type
                            self.handle_type_token(lexeme)
                        else:
                            self.handle_variable(lexeme)  # Otherwise, it's a variable
                        expect_var = False  # Reset the flag after processing
                    else:
                        if lexeme in self.type_tokens:
                            self.handle_type_token(lexeme)
                        else:
                            self.handle_python_code(lexeme)  # Treat it as general Python code
                    # if previous token was def then expect func
                    if expect_func:
                        self.handle_func_token(lexeme)
                    lexeme = ""
                else:
                    # Unchecked Python code
                    lexeme += char
                    while not self.end_of_file():
                        next_char = self.next_char()
                        if next_char in [";", "{", "}", ":"] or next_char.isspace():
                            self.forward -= 1  # Unread the token boundary
                            break
                        lexeme += next_char
                    self.handle_python_code(lexeme)
                    lexeme = ""
                expect_func = self.tokens[-1][0] == "DEF"

        return self.tokens


if __name__ == "__main__":
    # Angel testing below
    scanner = Scanner()
    # code = "int :: x_a; list :: y; print(x) { z=42 }"
    # [('TYPE', 'int'), ('TYPE_DEC', '::'), ('VAR', 'x_a'), ('SEMICOLON', ';'), ('TYPE', 'list'), ('TYPE_DEC', '::'), ('VAR', 'y'), ('SEMICOLON', ';'), ('PYTHON_CODE', 'print(x)'), ('LBRACE', '{'), ('PYTHON_CODE', 'z=42'), ('RBRACE', '}')]
    # code = "int :: x_a; list_a :: y;"
    # [('TYPE', 'int'), ('TYPE_DEC', '::'), ('VAR', 'x_a'), ('SEMICOLON', ';'), ('PYTHON_CODE', 'list_a'), ('TYPE_DEC', '::'), ('VAR', 'y'), ('SEMICOLON', ';')]
    code = "int :: def func(int :: a, int :: b){ int :: c = a + b; return c;}"
    code2 = "string :: def say_hello_world(){ string :: text = 'hello world'; print(text);}"
    # The above test case needs to be worked on
    scanner.read_code(code)
    tokens = scanner.scan_token()
    print(tokens)
    print("")
    scanner.read_code(code2)
    tokens = scanner.scan_token()
    print(tokens)

    # Nikolaus testing below

    pass
