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
            str: The next token as a string of length 1.
        """
        pass

    def end_of_file(self) -> bool:
        """
        Checks if the current token is the end of file.

        Returns:
            bool: True if the current token is the end of file, False otherwise.
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
