class Scanner:
    """Finite automata for scanning Viper code"""

    def __init__(self):
        """
        Initializes the scanner with the input code. No args, the scanner should be called on an input string.
        """
        self.code
        self.tokens

    def read_code(self) -> None:
        """
        Reads the input code and prepares it for scanning.

        Returns:
            None
        """
        pass

    def parse_code(self) -> list:
        """
        Parses the code and returns a list of tokens.

        Returns:
            list: A list of tokens parsed from the code.
        """
        pass

    def next_token(self) -> str:
        """
        Retrieves the next token from the code.

        Returns:
            str: The next token as a string.
        """
        pass

    def has_more_tokens(self) -> bool:
        """
        Checks if there are more tokens to parse.

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        pass

    def reset_scanner(self) -> None:
        """
        Resets the scanner to the beginning of the code.

        Returns:
            None
        """
        pass


if __name__ == "__main__":
    # Angel testing below

    # Nikolaus testing below

    pass
