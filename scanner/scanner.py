class Scanner:
    """Finite automata for scanning Viper code"""

    def __init__(self) -> None:
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
            "LPAREN",
            "RPAREN",
            "ASSIGN",
            "TYPE_DEC",
            "TYPE",
            "DEF",
            "VAR",
            "PYTHON_CODE",
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
        ]

        # Updated list of reserved single-character tokens
        self.single_char_tokens = [";", "{", "}", ",", "="]

        # operators, not necessaroly single tokens
        self.operators = ["**", "*", "+", "-", "//", "/", "%"]

        # keep track of vars that have been defined already
        # This should be fine even without scope I
        self.defined_vars = []
        self.defined_funcs = []

        self.expect_var = False  # This flag will be set to True after encountering TYPE_DEC
        self.expect_func = False  # This flag will be set to True after encountering DEF
        self.expect_func_delay = False  # TODO to help with managing parens after funcs

    def remove_comments_and_newline(self, input_code):
        cleaned_code = []
        for line in input_code.splitlines():
            if not line.strip().startswith("#"):
                line = line.split("#", 1)[0].rstrip()
            # Add the cleaned line if it's not empty
            if line:
                cleaned_code.append(line)

        return " ".join(cleaned_code)

    def read_code(self, input_code: str) -> None:
        """
        Reads the input code and prepares it for scanning as self.code
        and splits self.code char by char as self.chars.

        Args:
            input_code (str): The code to be scanned
        Returns:
            None
        """
        self.code = self.remove_comments_and_newline(input_code)
        self.chars = list(self.code)
        self.sentinel = len(self.chars)
        # Reset the scanner after each scan
        self.reset_scanner()

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
        self.state = "START"
        self.tokens = []
        self.defined_vars = []
        self.defined_funcs = []
        self.expect_var = False
        self.expect_func = False

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
        elif char == "=":
            self.tokens.append(("ASSIGN", "="))
        elif char == ",":
            self.tokens.append(("PYTHON_CODE", ","))

    def handle_op(self, char):
        next_char = self.next_char()
        if next_char in self.operators:  # double operators
            if char + next_char == "**":
                self.tokens.append(("OP", "**"))
            elif char + next_char == "//":
                self.tokens.append(("OP", "//"))
        else:
            self.tokens.append(("OP", char))
            self.forward -= 1

    def handle_colon(self) -> None:
        """
        Handle type declaration for "::".
        """
        next_char = self.next_char()
        if next_char == ":":
            self.tokens.append(("TYPE_DEC", "::"))
            self.expect_var = True
        elif next_char == " ":
            self.tokens.append(("PYTHON_CODE", ":"))
            self.expect_var = False
        else:
            self.tokens.append(("PYTHON_CODE", ":"))
            self.forward -= 1

    def handle_type_token(self, lexeme: str) -> None:
        """
        Handle reserved type tokens like "Any", "bool", etc.

        Args:
            lexeme (str): The current lexeme being scanned.
        """
        if lexeme in self.type_tokens:
            self.tokens.append(("TYPE", lexeme))

    def handle_variable(self, lexeme: str) -> None:
        """
        Handle variable name token after type declaration.
        """
        self.tokens.append(("VAR", lexeme))
        self.defined_vars.append(lexeme)
        self.expect_var = False

    def handle_python_code(self, lexeme: str) -> None:
        """
        Handle Python code as an unchecked token.
        """
        if lexeme in self.defined_vars:
            self.tokens.append(("VAR", lexeme))
            self.expected_var = False
        elif lexeme in self.defined_funcs:
            self.tokens.append(("FUNC", lexeme))
            self.expected_func = False
        else:
            self.tokens.append(("PYTHON_CODE", lexeme))

    def handle_func_token(self, lexeme) -> None:
        self.defined_funcs.append(lexeme)
        self.tokens.append(("FUNC", lexeme))
        self.expect_func = False
        self.expect_var = False

    def scan_token(self) -> list:
        """
        Scans the input code for specific tokens using finite automata transitions.
        Handles tokens, including collapsing multiple spaces into a single space token.

        Returns:
            list: A list of tokens in the format (Token Type, Token Value).
        """
        lexeme = ""

        while not self.end_of_file():

            char = self.next_char()

            # Handle spaces by tokenizing one space and skipping consecutive spaces
            if char.isspace():
                continue  # Move to the next character after handling spaces

            if self.state == "START":  # TODO check for [a-z](
                if char in self.single_char_tokens:
                    self.handle_single_char(char)
                elif char == ":":
                    self.handle_colon()
                elif char in self.operators:
                    self.handle_op(char)
                elif char.isalnum() or char == "_":  # Collect alphanumeric variables/types
                    expect_number = char.isnumeric()  # true if we are at a number
                    lexeme += char
                    while not self.end_of_file():
                        next_char = self.next_char()

                        if expect_number and (next_char.isalpha() or next_char == "_"):
                            # panic mode, start deleting chars until we reach a space or a number
                            continue

                        if next_char in self.single_char_tokens:
                            self.forward -= 1  # Unread the non-alphanumeric, non-space character
                            break
                        if next_char in self.operators:
                            self.forward -= 1
                            break
                        elif next_char == ":" and lexeme in self.type_tokens:
                            # Case where type:: is misspelt
                            self.forward -= 1
                            break
                        elif next_char.isspace():
                            # Handle space as separator for maximal munch, stop collecting lexeme
                            break
                        else:
                            lexeme += next_char
                    if lexeme in self.type_tokens:  # If it's a type token, handle it as a type
                        self.handle_type_token(lexeme)
                    elif lexeme == "def":  # If it's "def", handle it as DEF
                        self.tokens.append(("DEF", lexeme))
                        self.expect_func = True
                    elif self.expect_func:  # if previous token was def then expect func, FUNC takes precedence than VAR
                        self.handle_func_token(lexeme)
                    elif self.expect_var:  # If previous token was :: then expect var
                        self.handle_variable(lexeme)
                    else:
                        self.handle_python_code(lexeme)  # Treat it as general Python code
                    lexeme = ""
                else:
                    # Unchecked Python code
                    lexeme += char
                    while not self.end_of_file():
                        next_char = self.next_char()
                        if next_char in self.single_char_tokens or next_char.isspace():
                            self.forward -= 1  # Unread the token boundary
                            break
                        lexeme += next_char
                    self.handle_python_code(lexeme)
                    lexeme = ""

        return self.tokens
