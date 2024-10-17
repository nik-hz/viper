def scan_token(self) -> list:
        """
        Scans the input code for specific tokens using finite automata transitions.
        Handles tokens for `;`, `{`, `}`, `::`, type tokens, variable names, and Python code.

        Returns:
            list: A list of tokens in the format <Token Type, Token Value>.
        """
        lexeme = ""

        while not self.end_of_file():

            char = self.next_char()

            if char.isspace():
                continue

            if self.state == "START":
                if char in [";", "{", "}", "(", ")", ","]:
                    self.handle_single_char(char)
                elif char == ":":
                    self.handle_type_declaration()
                elif char.isalnum() or char == "_":  # Collect alphanumeric variables/types
                    lexeme += char
                    while not self.end_of_file():
                        next_char = self.next_char()
                        if next_char in [";", "{", "}", "(", ")", ","]:  # TODO: Should we add ::?
                            self.forward -= 1  # Unread the non-alphanumeric, non-space character
                            break
                        elif (
                            next_char.isspace()
                        ):  # Handle space as separator for maximal munch, stop collecting lexeme
                            break
                        else:
                            lexeme += next_char
                    if lexeme in self.type_tokens: # If it's a type token, handle it as a type
                        self.handle_type_token(lexeme)
                    elif lexeme == "def": # If it's "def", handle it as DEF
                        self.tokens.append(("DEF", lexeme))
                        self.expect_func = True
                    elif self.expect_func: # if previous token was def then expect func, FUNC takes precedence than VAR
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
                        if next_char in [";", "{", "}", ":"] or next_char.isspace():
                            self.forward -= 1  # Unread the token boundary
                            break
                        lexeme += next_char
                    self.handle_python_code(lexeme)
                    lexeme = ""
                self.expect_func = self.tokens[-1][0] == "DEF"