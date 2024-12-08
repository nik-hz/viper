class ParserError(Exception):
    def __init__(self, message, position, token=None):
        self.message = message
        self.position = position
        self.token = token

    def __str__(self):
        token_info = f" with token '{self.token}'" if self.token else ""
        return f"ParserError at position {self.position}: {self.message}{token_info}"


class Parser:
    def __init__(self, input_string, dbg):
        self.tokens = input_string
        self.position = 0
        self.in_loop = False
        self.at_return = False
        self.dbg = dbg
        self.err = []
        self.error_context_stack = []  # Stack of temporary error lists for backtracking

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
            print("\nParse successful!")
            return parse_tree
        else:
            print("Parse failed...")
            if self.err:
                print(self.err[0])
            return None

    def push_error_context(self):
        # Create a new temporary error context on the stack
        self.error_context_stack.append([])

    def pop_error_context(self, success):
        # Pop the top error context and commit to main error list if unsuccessful
        if self.error_context_stack:
            temp_errors = self.error_context_stack.pop()
            if not success and temp_errors:
                self.err.extend(temp_errors)

    def add_error(self, message):
        # token = self.current_token()
        token = None
        error = ParserError(message, self.position, token)
        if self.error_context_stack:
            self.error_context_stack[-1].append(error)
        else:
            self.err.append(error)

    # Viper -> StatementList
    def parse_viper(self):
        self.push_error_context()
        node = self.parse_statement_list()
        success = node is not None
        self.pop_error_context(success)
        if success:
            return ("Viper", node)
        self.add_error("Expected StatementList in Viper")
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
        self.pop_error_context(bool(statements))
        return ("StatementList", statements) if statements else ("StatementList", [])

    # Statement -> TypeDeclaration StatementPrime | ExpressionStatement
    def parse_statement(self):
        pos = self.position
        self.push_error_context()
        type_decl = self.parse_type_declaration()
        if type_decl is not None:
            stmt_prime = self.parse_statement_prime()
            if stmt_prime is not None:
                self.pop_error_context(True)
                return ("Statement", type_decl, stmt_prime)
            self.add_error("Expected StatementPrime after TypeDeclaration")
            self.position = pos

        expr_stmt = self.parse_expression_statement()
        if expr_stmt is not None:
            self.pop_error_context(True)
            return ("Statement", expr_stmt)

        self.pop_error_context(False)
        self.add_error("Expected a TypeDeclaration or ExpressionStatement")
        return None

    # StatementPrime -> VAR ASSIGN Expression SEMICOLON | DEF FUNC LPAREN ParameterList RPAREN FunctionBody
    def parse_statement_prime(self):
        pos = self.position
        self.push_error_context()
        if (varname := self.match("VAR")) and (ass := self.match("ASSIGN")):
            expr = self.parse_expression()
            if expr is not None and (semi := self.match("SEMICOLON")):
                self.pop_error_context(True)
                return ("StatementPrime", varname, ass, expr, semi)
            self.add_error("Expected SEMICOLON after Expression in StatementPrime")
            self.position = pos
        elif (fdef := self.match("DEF")) and (func := self.match("FUNC")) and (lpar := self.match("LPAREN")):
            params = self.parse_parameter_list()
            if (rpar := self.match("RPAREN")) and (colon := self.match("PYTHON_CODE")) and ":" in colon[1]:
                func_body = self.parse_function_body()
                if func_body is not None:
                    self.pop_error_context(True)
                    return ("StatementPrime", fdef, func, lpar, params, rpar, colon, func_body)
            self.add_error("Incorrectly formatted function body in StatementPrime")
            self.position = pos

        self.pop_error_context(False)
        return None

    # TypeDeclaration -> TYPE TYPE_DEC
    def parse_type_declaration(self):
        pos = self.position
        if (type_tok := self.match("TYPE")) and (type_dec := self.match("TYPE_DEC")):
            self.pop_error_context(True)
            return ("TypeDeclaration", type_tok, type_dec)
        self.add_error("Expected TYPE followed by TYPE_DEC in TypeDeclaration")
        self.position = pos
        return None  # don't return none just error out?

    # ParameterList -> Parameter ParameterListRest | #
    def parse_parameter_list(self):
        self.push_error_context()
        params = []
        param = self.parse_parameter()
        if param is not None:
            params.append(param)
            params += self.parse_parameter_list_rest()
            self.pop_error_context(True)
            return ("ParameterList", params)
        self.pop_error_context(False)
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
            self.pop_error_context(True)
            return ("Parameter", type_decl, var)
        self.add_error("Expected TypeDeclaration followed by VAR in Parameter")
        self.position = pos
        return None

    # FunctionBody -> LBRACE StatementList ReturnStatement RBRACE
    def parse_function_body(self):
        pos = self.position
        self.push_error_context()
        if lbrace := self.match("LBRACE"):
            stmt_list = self.parse_statement_list()  # TODO make sure return doesn't get caught here
            ret_stmt = self.parse_return_statement()
            if ret_stmt is not None and (rbrace := self.match("RBRACE")) and (semi := self.match("SEMICOLON")):
                self.pop_error_context(True)
                return ("FunctionBody", lbrace, stmt_list, ret_stmt, rbrace, semi)
            self.add_error("Expected RBRACE and SEMICOLON to close FunctionBody")
        else:
            self.add_error("Expected LBRACE to start FunctionBody")
        self.pop_error_context(False)
        self.position = pos
        return None

    # ReturnStatement -> RETURN ExpressionStatement SEMICOLON | #
    def parse_return_statement(self):
        pos = self.position
        self.push_error_context()
        if (ret := self.match("PYTHON_CODE")) and "return" in ret[1]:
            expr_stmt = self.parse_expression_statement()
            if expr_stmt is not None:  # and (semi := self.match("SEMICOLON")):
                self.pop_error_context(True)
                return ("ReturnStatement", ret, expr_stmt)
            self.add_error("Expected ExpressionStatement after return in ReturnStatement")
            self.position = pos  # TODO this may be causing some errors, but not sure
        self.pop_error_context(False)
        return ("ReturnStatement", None)  # Epsilon rule allows an empty ReturnStatement

    # ExpressionStatement -> Expression SEMICOLON handle case when loop and no semicolon needed
    def parse_expression_statement(self):
        expr = self.parse_expression()
        if expr is not None and (semi := self.match("SEMICOLON")) or expr is not None and self.in_loop:
            self.in_loop = False
            return ("ExpressionStatement", expr, semi)
        if expr:
            self.add_error("Expected SEMICOLON after Expression in ExpressionStatement")
        return None

    # Expression -> SimpleExpression ExpressionPrime
    # added simple expression for recusrion
    def parse_expression(self):
        self.push_error_context()
        simple_expr = self.parse_simple_expression()
        if simple_expr is not None:
            expr_prime = self.parse_expression_prime()
            self.pop_error_context(True)
            return ("Expression", simple_expr, expr_prime)
        self.pop_error_context(False)
        return None

    # ExpressionPrime -> SimpleExpression ExpressionPrime | #
    def parse_expression_prime(self):
        pos = self.position  # Save the current position for backtracking
        self.push_error_context()  # Start a new error context

        # Attempt to match SimpleExpression and recurse with ExpressionPrime
        simple_expr = self.parse_simple_expression()
        if simple_expr is not None:
            expr_prime = self.parse_expression_prime()
            self.pop_error_context(True)  # Parsing succeeded, clear error context
            return ("ExpressionPrime", simple_expr, expr_prime)

        # Epsilon (ε) rule applies if no SimpleExpression is found
        self.position = pos  # Restore position for epsilon
        self.pop_error_context(True)  # Parsing epsilon (successful, clear context)
        return ("ExpressionPrime", None)

    # SimpleExpression -> PYTHON_CODE | VAR | FunctionCall | Loop | ParenthesizedExpression | RangeExpression
    def parse_simple_expression(self):
        pos = self.position
        if loop := self.parse_loop():
            self.pop_error_context(True)
            return ("SimpleExpression", loop)
        elif code := self.match("PYTHON_CODE"):
            if "return" in code[1]:
                self.at_return = True
            else:
                self.pop_error_context(True)
                return ("SimpleExpression", code)
        elif var := self.match("VAR"):
            self.pop_error_context(True)
            return ("SimpleExpression", "VAR", var)
        elif op := self.match("OP"):
            self.pop_error_context(True)
            return ("SimpleExpression", "OP", op)
        elif func_call := self.parse_function_call():
            self.pop_error_context(True)
            return ("SimpleExpression", func_call)
        elif paren_expr := self.parse_parenthesized_expression():
            self.pop_error_context(True)
            return ("SimpleExpression", paren_expr)
        elif range_expr := self.parse_range():
            self.pop_error_context(True)
            return ("SimpleExpression", range_expr)
        self.pop_error_context(False)
        self.add_error("Expected, code, variables, functions, loops or range.")
        self.position = pos
        return None

    # ParenthesizedExpression -> LPAREN Expression RPAREN
    def parse_parenthesized_expression(self):
        pos = self.position
        self.push_error_context()
        if self.match("LPAREN"):
            expr = self.parse_expression()
            if expr and self.match("RPAREN"):
                self.pop_error_context(True)
                return ("ParenthesizedExpression", expr)
            self.pop_error_context(False)
            self.add_error("Expected RPAREN to close FunctionBody")
        else:
            self.pop_error_context(False)
            self.add_error("Expected LPAREN to start FunctionBody")
        self.position = pos
        return None

    # FunctionCall -> FUNC LPAREN ArgumentList RPAREN
    def parse_function_call(self):
        pos = self.position
        self.push_error_context()
        if self.match("FUNC") and self.match("LPAREN"):
            args = self.parse_argument_list()
            if self.match("RPAREN"):  # TODO match colon
                self.pop_error_context(True)
                return ("FunctionCall", args)
            self.add_error("Expected RPAREN to close FunctionCall arguments")
        self.pop_error_context(False)
        self.position = pos
        return None

    # ArgumentList -> Expression ArgumentListRest | #
    def parse_argument_list(self):
        pos = self.position
        self.push_error_context()
        expr = self.parse_expression()
        if expr is not None:
            arg_rest = self.parse_argument_list_rest()
            self.pop_error_context(True)
            return ("ArgumentList", [expr] + arg_rest)
        self.pop_error_context(True)
        return ("ArgumentList", [])  # Epsilon rule allows an empty ArgumentList

    # ArgumentListRest -> COMMA Expression ArgumentListRest | #
    def parse_argument_list_rest(self):
        args = []
        self.push_error_context()
        while self.match("COMMA"):
            expr = self.parse_expression()
            if expr is not None:
                args.append(expr)
            else:
                self.add_error("Expected expression after COMMA in ArgumentListRest")
                self.pop_error_context(False)
                return args
        self.pop_error_context(True)
        return args

    # Loop -> FOR VAR IN Iterable LBRACE StatementList RBRACE
    def parse_loop(self):
        """checks if we are in a for loop, otherwise back up pointer and return"""
        pos = self.position
        self.push_error_context()
        if (for_kwd := self.match("PYTHON_CODE")) and "for" in for_kwd[1]:
            iterable = self.parse_python()

            if iterable and self.match("LBRACE"):
                self.in_loop = True

                stmt_list = self.parse_statement_list()

                if self.match("RBRACE"):
                    self.in_loop = False
                    self.pop_error_context(True)
                    return ("Loop", for_kwd, iterable, stmt_list)
                self.add_error("Expected RBRACE to close Loop body")
            else:
                self.add_error("Expected LBRACE to start Loop body")
        self.pop_error_context(False)
        self.position = pos
        return None

    # Iterable -> Expression
    def parse_iterable(self):
        return self.parse_expression()

    # RangeExpression -> RANGE LPAREN RangeParameters RPAREN
    def parse_range(self):
        pos = self.position
        self.push_error_context()
        if (range_tok := self.match("TYPE")) and (lpar := self.match("LPAREN")):  # next token is paren
            python1 = self.parse_python()
            var1 = self.parse_var()
            python2 = self.parse_python()
            var2 = self.parse_var()

            # Recursive call for nested ranges edge case
            nested_range = self.parse_range()

            if nested_range:
                if rpar := self.match("RPAREN"):
                    self.pop_error_context(True)
                    return (range_tok, lpar, python1, var1, python2, var2, nested_range, rpar)
            else:
                if rpar := self.match("RPAREN"):
                    self.pop_error_context(True)
                    return (range_tok, lpar, python1, var1, python2, var2, nested_range, rpar)
            self.add_error("Expected RPAREN to close RangeExpression")
            self.pop_error_context(False)
            self.position = pos
        return None  # Epsilon case if Range is empty

    def parse_python(self):
        nodes = []
        self.push_error_context()
        while code := self.match("PYTHON_CODE"):
            nodes.append(("Python", code))
        self.pop_error_context(bool(nodes))
        return nodes if nodes else None

    def parse_var(self):
        nodes = []
        self.push_error_context()
        while var := self.match("VAR"):
            nodes.append(("Var", var))
        self.pop_error_context(bool(nodes))
        return nodes if nodes else None


def convert_tokens(tokens):
    result = []
    for token in tokens:
        token_type, token_value = token.strip("<>").split(", ", 1)
        result.append((token_type, f"<{token_type}, {token_value}>"))
    return result


if __name__ == "__main__":

    # tokens = [
    #     "<TYPE, int>",
    #     "<TYPE_DEC, ::>",
    #     "<VAR, x_a>",
    #     "<ASSIGN, =>",
    #     "<PYTHON_CODE, 10>",
    #     "<SEMICOLON, ;>",
    #     "<TYPE, list>",
    #     "<TYPE_DEC, ::>",
    #     "<VAR, y>",
    #     "<ASSIGN, =>",
    #     "<TYPE, range>",
    #     "<LPAREN, (>",
    #     "<PYTHON_CODE, 0>",
    #     "<PYTHON_CODE, ,>",
    #     "<VAR, x_a>",
    #     "<RPAREN, )>",
    #     "<SEMICOLON, ;>",
    #     "<PYTHON_CODE, for>",
    #     "<PYTHON_CODE, i>",
    #     "<PYTHON_CODE, in>",
    #     "<PYTHON_CODE, y:>",
    #     "<LBRACE, {>",
    #     "<PYTHON_CODE, print>",
    #     "<LPAREN, (>",
    #     "<PYTHON_CODE, i>",
    #     "<RPAREN, )>",
    #     "<SEMICOLON, ;>",
    #     "<RBRACE, }>",
    #     "<SEMICOLON, ;>",
    # ]

    # tokens2 = [
    #     "<TYPE, str>",
    #     "<TYPE_DEC, ::>",
    #     "<DEF, def>",
    #     "<FUNC, say_hello_world>",
    #     "<LPAREN, (>",
    #     "<RPAREN, )>",
    #     "<PYTHON_CODE, :>",
    #     "<LBRACE, {>",
    #     "<PYTHON_CODE, string>",
    #     "<TYPE_DEC, ::>",
    #     "<VAR, text>",
    #     "<ASSIGN, =>",
    #     "<PYTHON_CODE, 'hello>",
    #     "<PYTHON_CODE, world'>",
    #     "<SEMICOLON, ;>",
    #     "<PYTHON_CODE, print>",
    #     "<LPAREN, (>",
    #     "<VAR, text>",
    #     "<RPAREN, )>",
    #     "<SEMICOLON, ;>",
    #     "<RBRACE, }>",
    #     "<SEMICOLON, ;>",
    # ]

    # tokens3 = [
    #     "<TYPE, int>",
    #     "<TYPE_DEC, ::>",
    #     "<DEF, def>",
    #     "<FUNC, func>",
    #     "<LPAREN, (>",
    #     "<TYPE, int>",
    #     "<TYPE_DEC, ::>",
    #     "<VAR, a>",
    #     "<PYTHON_CODE, ,>",
    #     "<TYPE, int>",
    #     "<TYPE_DEC, ::>",
    #     "<VAR, b>",
    #     "<RPAREN, )>",
    #     "<PYTHON_CODE, :>",
    #     "<LBRACE, {>",
    #     "<TYPE, int>",
    #     "<TYPE_DEC, ::>",
    #     "<VAR, c>",
    #     "<ASSIGN, =>",
    #     "<VAR, a>",
    #     "<OP, +>",
    #     "<VAR, b>",
    #     "<SEMICOLON, ;>",
    #     "<PYTHON_CODE, return>",
    #     "<VAR, c>",
    #     "<SEMICOLON, ;>",
    #     "<RBRACE, }>",
    #     "<SEMICOLON, ;>",
    # ]

    tokens4 = [
        "<PYTHON_CODE, from>",
        "<PYTHON_CODE, math>",
        "<PYTHON_CODE, import>",
        "<PYTHON_CODE, sqrt>",
        "<SEMICOLON, ;>,",
    ]

    # tokens5 = [
    #     "<TYPE, int>",
    #     "<TYPE_DEC, ::>",
    #     "<VAR, x_b>",
    #     "<ASSIGN, =>",
    #     "<PYTHON_CODE, 10>",
    #     "<SEMICOLON, ;>",
    # ]

    # sample_input_string = convert_tokens(tokens)
    # sample_input_string_2 = convert_tokens(tokens2)
    # sample_input_string_3 = convert_tokens(tokens3)
    sample_input_string_4 = convert_tokens(tokens4)
    # sample_input_string_5 = convert_tokens(tokens5)

    # print("\n######################## PARSING EXAMPLE 1 ########################\n")
    # parser = Parser(sample_input_string, dbg=False)
    # parse_tree = parser.parse()
    # print(parse_tree)

    # SHOULD FAIL
    # print("\n######################## PARSING EXAMPLE 2 ########################\n")
    # parser = Parser(sample_input_string_2, dbg=False)
    # parse_tree = parser.parse()
    # print(parse_tree)

    # print("\n######################## PARSING EXAMPLE 3 ########################\n")
    # parser = Parser(sample_input_string_3, dbg=True)
    # parse_tree = parser.parse()
    # print(parse_tree)

    print("\n######################## PARSING EXAMPLE 4 ########################\n")
    parser = Parser(sample_input_string_4, dbg=True)
    parse_tree = parser.parse()
    print(parse_tree)

    # SHOULD FAIL
    # print("\n######################## PARSING EXAMPLE 5 ########################\n")
    # parser = Parser(sample_input_string_5, dbg=False)
    # parse_tree = parser.parse()
    # print(parse_tree)
