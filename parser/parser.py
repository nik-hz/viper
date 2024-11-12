class ParserError(Exception):
    def __init__(self, message, position, token):
        super().__init__(message)
        self.position = position
        self.token = token

    def __str__(self):
        return f"ParserError: {self.args[0]} at position {self.position} with token {self.token}"


class Parser:
    def __init__(self, input_string, dbg=True):
        self.tokens = input_string
        self.position = 0
        self.in_loop = False
        self.at_return = False
        self.dbg = dbg
        self.err = []

    def current_token(self):
        # Return the current token or None if at the end of the input
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def match(self, expected_token):
        # Match the current token if it equals the expected token
        if self.current_token() and self.current_token()[0] == expected_token:
            if self.dbg:
                print(self.current_token())
            matched_token = self.current_token()
            self.position += 1
            return matched_token
        return None

    def parse(self):
        # Start parsing from the root rule
        parse_tree = self.parse_viper()
        if parse_tree and self.position == len(self.tokens):
            print("Parse successful!")
            return parse_tree
        else:
            # print("Parse failed. Generating error trace...")
            if self.err:
                for error in self.err:
                    print(error)  # Print error details before raising
                # print("\n")
                # raise self.err[0]
            return None

    # Viper -> StatementList
    def parse_viper(self):
        node = self.parse_statement_list()
        if node is not None:
            return ("Viper", node)
        return None

    # StatementList -> Statement StatementList | #
    def parse_statement_list(self):
        statements = []
        while True:
            statement = self.parse_statement()
            if statement is not None:
                statements.append(statement)
            else:
                break
        return ("StatementList", statements) if statements else ("StatementList", [])

    # Statement -> TypeDeclaration StatementPrime | ExpressionStatement
    def parse_statement(self):
        pos = self.position
        type_decl = self.parse_type_declaration()
        if type_decl is not None:
            stmt_prime = self.parse_statement_prime()
            if stmt_prime is not None:
                return ("Statement", type_decl, stmt_prime)
            self.position = pos

        expr_stmt = self.parse_expression_statement()
        if expr_stmt is not None:
            return ("Statement", expr_stmt)
        return None

    # StatementPrime -> VAR ASSIGN Expression SEMICOLON | DEF FUNC LPAREN ParameterList RPAREN FunctionBody
    def parse_statement_prime(self):
        pos = self.position
        if (varname := self.match("VAR")) and (ass := self.match("ASSIGN")):
            expr = self.parse_expression()
            if expr is not None and (semi := self.match("SEMICOLON")):
                return ("StatementPrime", varname, ass, expr, semi)
            self.position = pos
        elif (fdef := self.match("DEF")) and (func := self.match("FUNC")) and (lpar := self.match("LPAREN")):
            params = self.parse_parameter_list()
            if (rpar := self.match("RPAREN")) and (colon := self.match("PYTHON_CODE")) and ":" in colon[1]:
                func_body = self.parse_function_body()
                if func_body is not None:
                    return ("StatementPrime", fdef, func, lpar, params, rpar, colon, func_body)
            self.position = pos
        return None

    # TypeDeclaration -> TYPE TYPE_DEC
    def parse_type_declaration(self):
        pos = self.position
        if (type_tok := self.match("TYPE")) and (type_dec := self.match("TYPE_DEC")):
            return ("TypeDeclaration", type_tok, type_dec)
        self.position = pos
        self.err.append(ParserError(f"Expected a TYPE but found {type_tok}", self.position, type_tok))
        return None  # don't return none just error out?

    # ParameterList -> Parameter ParameterListRest | #
    def parse_parameter_list(self):
        params = []
        param = self.parse_parameter()
        if param is not None:
            params.append(param)
            params += self.parse_parameter_list_rest()
        return ("ParameterList", params)

    # ParameterListRest -> COMMA Parameter ParameterListRest | #
    def parse_parameter_list_rest(self):
        params = []
        while (comma := self.match("PYTHON_CODE")) and "," in comma[1]:
            param = self.parse_parameter()
            if param is not None:
                params.append(param)
        return params

    # Parameter -> TypeDeclaration VAR
    def parse_parameter(self):
        pos = self.position
        type_decl = self.parse_type_declaration()
        if type_decl is not None and (var := self.match("VAR")):
            return ("Parameter", type_decl, var)
        self.position = pos
        return None

    # FunctionBody -> LBRACE StatementList ReturnStatement RBRACE
    def parse_function_body(self):
        pos = self.position
        if lbrace := self.match("LBRACE"):
            stmt_list = self.parse_statement_list()  # TODO make sure return doesn't get caught here
            ret_stmt = self.parse_return_statement()
            if ret_stmt is not None and (rbrace := self.match("RBRACE")):
                return ("FunctionBody", lbrace, stmt_list, ret_stmt, rbrace)
            self.position = pos
        return None

    # ReturnStatement -> RETURN ExpressionStatement SEMICOLON | #
    def parse_return_statement(self):
        pos = self.position
        if (ret := self.match("PYTHON_CODE")) and "return" in ret[1]:
            expr_stmt = self.parse_expression_statement()
            if expr_stmt is not None:  # and (semi := self.match("SEMICOLON")):
                return ("ReturnStatement", ret, expr_stmt)
            self.position = pos
        return ("ReturnStatement", None)  # Epsilon rule allows an empty ReturnStatement

    # ExpressionStatement -> Expression SEMICOLON handle case when loop and no semicolon needed
    def parse_expression_statement(self):
        expr = self.parse_expression()
        if expr is not None and (semi := self.match("SEMICOLON")) or expr is not None and self.in_loop:
            self.in_loop = False
            return ("ExpressionStatement", expr, semi)
        return None

    # Expression -> SimpleExpression ExpressionPrime
    # added simple expression for recusrion
    def parse_expression(self):
        simple_expr = self.parse_simple_expression()
        if simple_expr is not None:
            expr_prime = self.parse_expression_prime()
            return ("Expression", simple_expr, expr_prime)
        return None

    # ExpressionPrime -> OP SimpleExpression ExpressionPrime | #
    def parse_expression_prime(self):
        terms = []
        while op := self.match("OP"):
            simple_expr = self.parse_simple_expression()
            if simple_expr is not None:
                terms.append((op, simple_expr))
            else:
                break
        return ("ExpressionPrime", terms) if terms else ("ExpressionPrime", None)

    # SimpleExpression -> PYTHON_CODE | VAR | FunctionCall | Loop | ParenthesizedExpression | RangeExpression
    def parse_simple_expression(self):
        pos = self.position
        if loop := self.parse_loop():
            return ("SimpleExpression", loop)
        elif code := self.match("PYTHON_CODE"):
            if "return" in code[1]:
                self.at_return = True
            else:
                return ("SimpleExpression", code)
        elif var := self.match("VAR"):
            return ("SimpleExpression", "VAR", var)
        elif func_call := self.parse_function_call():
            return ("SimpleExpression", func_call)
        elif paren_expr := self.parse_parenthesized_expression():
            return ("SimpleExpression", paren_expr)
        elif range_expr := self.parse_range():
            return ("SimpleExpression", range_expr)
        self.position = pos
        return None

    # ParenthesizedExpression -> LPAREN Expression RPAREN
    def parse_parenthesized_expression(self):
        pos = self.position
        if self.match("LPAREN"):
            expr = self.parse_expression()
            if expr and self.match("RPAREN"):
                return ("ParenthesizedExpression", expr)
            self.position = pos
        return None

    # FunctionCall -> FUNC LPAREN ArgumentList RPAREN
    def parse_function_call(self):
        pos = self.position
        if self.match("FUNC") and self.match("LPAREN"):
            args = self.parse_argument_list()
            if self.match("RPAREN"):  # TODO match colon
                return ("FunctionCall", args)
            self.position = pos
        return None

    # ArgumentList -> Expression ArgumentListRest | #
    def parse_argument_list(self):
        pos = self.position
        expr = self.parse_expression()
        if expr is not None:
            arg_rest = self.parse_argument_list_rest()
            return ("ArgumentList", [expr] + arg_rest)
        return ("ArgumentList", [])  # Epsilon rule allows an empty ArgumentList

    # ArgumentListRest -> COMMA Expression ArgumentListRest | #
    def parse_argument_list_rest(self):
        args = []
        while self.match("COMMA"):
            expr = self.parse_expression()
            if expr is not None:
                args.append(expr)
        return args

    # Loop -> FOR VAR IN Iterable LBRACE StatementList RBRACE
    def parse_loop(self):
        """checks if we are in a for loop, otherwise back up pointer and return"""
        pos = self.position
        if (for_kwd := self.match("PYTHON_CODE")) and "for" in for_kwd[1]:
            iterable = self.parse_python()

            if iterable and self.match("LBRACE"):
                self.in_loop = True

                stmt_list = self.parse_statement_list()

                if self.match("RBRACE"):
                    self.in_loop = False

                    return ("Loop", for_kwd, iterable, stmt_list)

        self.position = pos
        return None

    # Iterable -> Expression
    def parse_iterable(self):
        return self.parse_expression()

    # RangeExpression -> RANGE LPAREN RangeParameters RPAREN
    def parse_range(self):
        pos = self.position
        if (range_tok := self.match("TYPE")) and (lpar := self.match("LPAREN")):  # next token is paren
            python1 = self.parse_python()
            var1 = self.parse_var()
            python2 = self.parse_python()
            var2 = self.parse_var()

            # Recursive call to parse nested Range
            nested_range = self.parse_range()

            if nested_range:
                if rpar := self.match("RPAREN"):
                    # if scol := self.match("SEMICOLON"):
                    #     return (range_tok, lpar, python1, var1, python2, var2, nested_range, rpar, scol)
                    # else:
                    return (range_tok, lpar, python1, var1, python2, var2, nested_range, rpar)
            else:
                if rpar := self.match("RPAREN"):
                    # if scol := self.match("SEMICOLON"):
                    #     return (range_tok, lpar, python1, var1, python2, var2, rpar, scol)
                    # else:
                    return (range_tok, lpar, python1, var1, python2, var2, nested_range, rpar)

            # Backtrack if parsing failed
            self.position = pos
        return None  # Epsilon case if Range is empty

    def parse_python(self):
        nodes = []
        while code := self.match("PYTHON_CODE"):
            nodes.append(("Python", code))
        return nodes if nodes else None

    def parse_var(self):
        nodes = []
        while var := self.match("VAR"):
            nodes.append(("Var", var))
        return nodes if nodes else None


if __name__ == "__main__":

    def convert_tokens(tokens):
        result = []
        for token in tokens:
            token_type, token_value = token.strip("<>").split(", ", 1)
            result.append((token_type, f"<{token_type}, {token_value}>"))
        return result

    tokens = [
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
        "<SEMICOLON, ;>",
    ]

    tokens2 = [
        "<TYPE, str>",
        "<TYPE_DEC, ::>",
        "<DEF, def>",
        "<FUNC, say_hello_world>",
        "<LPAREN, (>",
        "<RPAREN, )>",
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
    ]

    tokens3 = [
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
        "<ASSIGN, =>>",
        "<VAR, a>",
        "<OP, +>",
        "<VAR, b>",
        "<SEMICOLON, ;>",
        "<PYTHON_CODE, return>",
        "<VAR, c>",
        "<SEMICOLON, ;>",
        "<RBRACE, }>",
    ]

    tokens4 = [
        "<TYPE, int>",
        "<TYPE_DEC, ::>",
        "<VAR, x_a>",
        "<ASSIGN, =>",
        "<PYTHON_CODE, 10>",
        "<SEMICOLON, ;>",
    ]
    sample_input_string = convert_tokens(tokens)
    sample_input_string_2 = convert_tokens(tokens2)
    sample_input_string_3 = convert_tokens(tokens3)
    sample_input_string_4 = convert_tokens(tokens4)
    # parser = Parser(sample_input_string)
    # parse_tree = parser.parse()
    # print(parse_tree)

    print("\n######################## PARSING EXAMPLE 1 ########################\n")
    parser = Parser(sample_input_string, dbg=False)
    parse_tree = parser.parse()
    print(parse_tree)

    # TODO catch error and continue
    print("\n######################## PARSING EXAMPLE 2 ########################\n")
    parser = Parser(sample_input_string_2, dbg=False)
    parse_tree = parser.parse()
    print(parse_tree)

    print("\n######################## PARSING EXAMPLE 3 ########################\n")
    parser = Parser(sample_input_string_3, dbg=False)
    parse_tree = parser.parse()
    print(parse_tree)

    print("\n######################## PARSING EXAMPLE 4 ########################\n")
    parser = Parser(sample_input_string_4, dbg=False)
    parse_tree = parser.parse()
    print(parse_tree)
