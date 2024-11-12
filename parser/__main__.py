from parser.parser import Parser, convert_tokens
from scanner.scanner import Scanner

if __name__ == "__main__":
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

    tokens5 = [
        "<TYPE, int>",
        "<TYPE_DEC, ::>",
        "<VAR, x_a>",
        "<ASSIGN, =>",
        "<PYTHON_CODE, 10>",
        "<TYPE, int>",
        "<TYPE_DEC, ::>",
        "<VAR, x_b>",
        "<ASSIGN, =>",
        "<PYTHON_CODE, 10>;",
    ]

    sample_input_string = convert_tokens(tokens)
    sample_input_string_2 = convert_tokens(tokens2)
    sample_input_string_3 = convert_tokens(tokens3)
    sample_input_string_4 = convert_tokens(tokens4)
    sample_input_string_5 = convert_tokens(tokens5)

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

    print("\n######################## PARSING EXAMPLE 5 ########################\n")
    parser = Parser(sample_input_string_5, dbg=False)
    parse_tree = parser.parse()
    print(parse_tree)
