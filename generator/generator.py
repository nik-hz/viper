class ViperToPythonGenerator:
    def __init__(self):
        self.indent_level = 0
        self.indent_str = "    "

    def indent(self):
        return self.indent_str * self.indent_level

    def generate(self, ast):
        # print("DEBUG: Starting generate with ast:", ast[0])
        if ast[0] == "Viper":
            return self.generate_program(ast[1])
        return ""

    def generate_program(self, statement_list):
        # print("DEBUG: Starting generate_program with:", statement_list[0])
        if statement_list[0] == "StatementList":
            statements = [self.generate_statement(stmt) for stmt in statement_list[1]]
            # print("DEBUG: Generated statements:", statements)
            result = "\n".join(stmt for stmt in statements if stmt)
            # print("DEBUG: Final program:", result)
            return result
        return ""

    def generate_statement(self, statement):
        # print("DEBUG: Starting generate_statement with:", statement[0])
        if statement[0] != "Statement":
            return ""

        stmt_content = statement[1]
        if isinstance(stmt_content, tuple):
            if stmt_content[0] == "TypeDeclaration":
                return self.handle_type_declaration(stmt_content, statement[2])
            elif stmt_content[0] == "ExpressionStatement":
                expr = self.generate_expression(stmt_content[1])
                return f"{self.indent()}{expr}"
        return ""

    def handle_type_declaration(self, type_decl, statement_prime):
        # print("DEBUG: Starting handle_type_declaration")
        type_name = type_decl[1][1]
        # print("DEBUG: Type name:", type_name)

        if statement_prime[0] == "StatementPrime":
            # print("DEBUG: Statement prime:", statement_prime[1])
            if isinstance(statement_prime[1], tuple) and statement_prime[1][0] == "DEF":
                return self.generate_function(type_name, statement_prime)
            # Handle variable declaration
            elif isinstance(statement_prime[1], tuple) and statement_prime[1][0] == "VAR":
                var_name = statement_prime[1][1]  # Extract variable name
                expression = statement_prime[3]  # Extract the expression for assignment
                expr_str = self.generate_expression(expression)  # Generate the expression code
                result = f"{self.indent()}{var_name} = {expr_str}"
                if type_name != "NoneType":  # Add type assertion if applicable
                    result += f"\n{self.indent()}assert isinstance({var_name}, {type_name})"
                return result
            elif statement_prime[1] == "VAR":
                # Handle simpler VAR case
                var_name = statement_prime[1]  # Variable name
                expression = statement_prime[2]  # Expression
                expr_str = self.generate_expression(expression)
                result = f"{self.indent()}{var_name} = {expr_str}"
                if type_name != "NoneType":
                    result += f"\n{self.indent()}assert isinstance({var_name}, {type_name})"
                return result
        return ""

    def generate_function(self, return_type, statement_prime):
        # print("DEBUG: Starting generate_function")
        # Extract function name from FUNC tuple
        func_name = None
        for item in statement_prime:
            if isinstance(item, tuple) and item[0] == "FUNC":
                func_name = item[1]
                # print("DEBUG: Found function name:", func_name)
                break

        # Find function body
        body = None
        for item in statement_prime:
            if isinstance(item, tuple) and item[0] == "FunctionBody":
                body = item
                # print("DEBUG: Found function body")
                break

        if not func_name or not body:
            return ""

        result = f"def {func_name}():"

        # Generate function body
        self.indent_level += 1
        body_statements = body[2][1]  # StatementList within FunctionBody
        statements = [self.generate_statement(stmt) for stmt in body_statements]
        body_code = "\n".join(stmt for stmt in statements if stmt)
        # print("DEBUG: Generated body code:", body_code)
        self.indent_level -= 1

        if body_code:
            result += f"\n{body_code}"

        return result

    def generate_expression(self, expression):
        # print("DEBUG: Starting generate_expression with:", expression if isinstance(expression, tuple) else expression)
        st = ""
        st = self._generate_expression(expression, st)
        return st

    def _generate_expression(self, expression, builder):

        if len(expression) == 2:
            cfg, next_expr = expression
        elif len(expression) == 3:
            cfg, middle_expr, next_expr = expression

        # base case next_expr is a string and not tuple
        if isinstance(next_expr, str):
            builder += next_expr
            return builder
        elif next_expr == None:
            return builder

        if cfg == "ParenthesizedExpression":
            builder += "("
            builder = self._generate_expression(next_expr, builder)
            builder += ")"
            return builder
        elif cfg == "Expression":
            # builder += middle_expr[-1][1]
            builder = self._generate_expression(middle_expr, builder)
            builder = self._generate_expression(next_expr, builder)
            return builder
        elif cfg == "ExpressionPrime":
            builder = self._generate_expression(middle_expr, builder)
            builder = self._generate_expression(next_expr, builder)
            return builder
        elif cfg == "SimpleExpression":
            builder = self._generate_expression(next_expr, builder)
            return builder
        elif cfg == "FunctionCall":
            builder = self._generate_expression(middle_expr, builder)
            builder += "("
            temp = self._generate_expression(next_expr, builder)
            if temp:
                builder = temp
            builder += ")"
            return builder
        elif cfg == "ArgumentList":
            if next_expr:
                builder = self._generate_expression(next_expr[0], builder)
            return builder


def convert_viper_to_python(ast):
    generator = ViperToPythonGenerator()
    result = generator.generate(ast)
    # print("DEBUG: Final generated code:", result)
    return result


# Test with the provided AST
ast1 = (
    "Viper",
    (
        "StatementList",
        [
            (
                "Statement",
                ("TypeDeclaration", ("TYPE", "NoneType"), ("TYPE_DEC", "::")),
                (
                    "StatementPrime",
                    ("DEF", "def"),
                    ("FUNC", "print_one"),
                    ("LPAREN", "("),
                    ("ParameterList", []),
                    ("RPAREN", ")"),
                    ("PYTHON_CODE", ":"),
                    (
                        "FunctionBody",
                        ("LBRACE", "{"),
                        (
                            "StatementList",
                            [
                                (
                                    "Statement",
                                    ("TypeDeclaration", ("TYPE", "int"), ("TYPE_DEC", "::")),
                                    (
                                        "StatementPrime",
                                        ("VAR", "num"),
                                        ("ASSIGN", "="),
                                        (
                                            "Expression",
                                            ("SimpleExpression", ("PYTHON_CODE", "1")),
                                            ("ExpressionPrime", None),
                                        ),
                                        ("SEMICOLON", ";"),
                                    ),
                                ),
                                (
                                    "Statement",
                                    (
                                        "ExpressionStatement",
                                        (
                                            "Expression",
                                            ("SimpleExpression", ("PYTHON_CODE", "print")),
                                            (
                                                "ExpressionPrime",
                                                (
                                                    "SimpleExpression",
                                                    (
                                                        "ParenthesizedExpression",
                                                        (
                                                            "Expression",
                                                            ("SimpleExpression", "VAR", ("VAR", "num")),
                                                            ("ExpressionPrime", None),
                                                        ),
                                                    ),
                                                ),
                                                ("ExpressionPrime", None),
                                            ),
                                        ),
                                        ("SEMICOLON", ";"),
                                    ),
                                ),
                            ],
                        ),
                        ("ReturnStatement", None),
                        ("RBRACE", "}"),
                        ("SEMICOLON", ";"),
                    ),
                ),
            ),
            (
                "Statement",
                (
                    "ExpressionStatement",
                    (
                        "Expression",
                        (
                            "SimpleExpression",
                            (
                                "FunctionCall",
                                ("FUNC", "print_one"),
                                (
                                    "ArgumentList",
                                    [
                                        (
                                            "Expression",
                                            ("SimpleExpression", ("PYTHON_CODE", "1")),
                                            ("ExpressionPrime", None),
                                        )
                                    ],
                                ),
                            ),
                        ),
                        ("ExpressionPrime", None),
                    ),
                    ("SEMICOLON", ";"),
                ),
            ),
        ],
    ),
)


python_code = convert_viper_to_python(ast1)
print(python_code)
