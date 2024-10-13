class Scanner:
    """Finite automata for scanning Viper code"""

    def __init__(self):
        """
        Initializes the scanner with the input code. No args, the scanner should be called on an input string.
        """
        # I/O
        self.code # original string of code
        self.chars # list of chars from self.code
        self.tokens # list of final tokens

        # pointers
        self.lexemeBegin
        self.forward
        self.sentinel

        # states
        self.states = None  # TODO
        self.accept_states = None  # TODO

    def read_code(self) -> None:
        """
        Reads the input code and prepares it for scanning as self.code
        and split self.code char by char as self.chars.

        Returns:
            None
        """
        pass

    def parse_code(self) -> list:
        """
        Parses the code and returns a list of chars.

        Returns:
            list: A list of chars parsed from the code.
        """
        pass

    def next_char(self) -> str:
        """
        Retrieves the next char from the code.

        Returns:
            str: The next char as a string of length 1.
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
