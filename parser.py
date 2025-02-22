import ply.yacc as yacc
from lexer import tokens, lexer

# Define operator precedence
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)


# Kannada-based parser rules
def p_program(p):
    '''program : START NEWLINE statements END'''
    p[0] = p[3]  # The statements are the body of the program


def p_statements(p):
    '''statements : statement
                  | statements statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_statement(p):
    '''statement : print_statement
                 | assignment_statement
                 | if_statement
                 | while_statement
                 | for_statement
                 | function_def
                 | function_call
                 | return_statement
                 | break_statement
                 | continue_statement
                 | pass_statement
                 | try_except_statement
                 | import_statement
                 | class_definition'''
    p[0] = p[1]


def p_print_statement(p):
    '''print_statement : PRINT LPAREN expression RPAREN NEWLINE
                       | PRINT LPAREN STRING RPAREN NEWLINE'''
    if p[3].startswith('"') or p[3].startswith("'"):
        value = {"type": "string", "value": p[3][1:-1]}
    else:
        value = p[3]
    p[0] = {"type": "print", "value": value}


def p_expression(p):
    '''expression : expression PLUS term
                 | expression MINUS term
                 | term'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {"type": "binary_op", "op": p[2], "left": p[1], "right": p[3]}


def p_term(p):
    '''term : term TIMES factor
            | term DIVIDE factor
            | factor'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {"type": "binary_op", "op": p[2], "left": p[1], "right": p[3]}


def p_factor(p):
    '''factor : NUMBER
              | STRING
              | ID
              | LPAREN expression RPAREN
              | MINUS factor'''
    if len(p) == 2:
        if isinstance(p[1], int):
            p[0] = {"type": "number", "value": p[1]}
        elif p[1].startswith('"') or p[1].startswith("'"):
            p[0] = {"type": "string", "value": p[1][1:-1]}
        else:
            p[0] = {"type": "identifier", "name": p[1]}
    else:
        p[0] = {"type": "unary_op", "op": "NEGATE", "operand": p[2]}


def p_comparison(p):
    '''comparison : expression LESS expression
                  | expression GREATER expression
                  | expression EQUAL expression
                  | expression NOTEQUAL expression
                  | expression LESSEQUAL expression
                  | expression GREATEREQUAL expression'''
    op_map = {
        '<': 'LESS',
        '>': 'GREATER',
        '==': 'EQUAL',
        '!=': 'NOTEQUAL',
        '<=': 'LESSEQUAL',
        '>=': 'GREATEREQUAL'
    }
    p[0] = {"type": "comparison", "op": op_map[p[2]], "left": p[1], "right": p[3]}


def p_assignment_statement(p):
    '''assignment_statement : ID ASSIGN expression'''
    p[0] = {"type": "assignment", "target": p[1], "value": p[3]}


def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN COLON statements
                    | IF LPAREN expression RPAREN COLON statements ELSE COLON statements
                    | IF LPAREN expression RPAREN COLON statements ELIF LPAREN expression RPAREN COLON statements'''
    if len(p) == 7:
        p[0] = {"type": "if", "condition": p[3], "body": p[6]}
    elif p[7] == 'ELSE':
        p[0] = {"type": "if", "condition": p[3], "body": p[6], "else_body": p[9]}
    else:  # ELIF
        elif_clause = {"type": "if", "condition": p[9], "body": p[12]}
        p[0] = {"type": "if", "condition": p[3], "body": p[6], "else_body": [elif_clause]}


def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN COLON statements'''
    p[0] = {"type": "while", "condition": p[3], "body": p[6]}


def p_for_statement(p):
    '''for_statement : FOR LPAREN ID IN RANGE LPAREN NUMBER COMMA NUMBER RPAREN RPAREN COLON statements'''
    p[0] = {"type": "for", "var": p[3], "start": p[7], "end": p[9], "body": p[13]}


def p_function_def(p):
    '''function_def : DEF ID LPAREN parameter_list RPAREN COLON statements'''
    p[0] = {"type": "function_def", "name": p[2], "params": p[4], "body": p[7]}


def p_parameter_list(p):
    '''parameter_list : empty
                      | ID
                      | parameter_list COMMA ID'''
    if len(p) == 1 or p[1] is None:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]


def p_function_call(p):
    '''function_call : ID LPAREN argument_list RPAREN'''
    p[0] = {"type": "function_call", "name": p[1], "args": p[3]}


def p_argument_list(p):
    '''argument_list : empty
                     | expression
                     | argument_list COMMA expression'''
    if len(p) == 1 or p[1] is None:
        p[0] = []
    elif len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]


def p_return_statement(p):
    '''return_statement : RETURN expression'''
    p[0] = {"type": "return", "value": p[2]}


def p_break_statement(p):
    '''break_statement : BREAK'''
    p[0] = {"type": "break"}


def p_continue_statement(p):
    '''continue_statement : CONTINUE'''
    p[0] = {"type": "continue"}


def p_pass_statement(p):
    '''pass_statement : PASS'''
    p[0] = {"type": "pass"}


def p_try_except_statement(p):
    '''try_except_statement : TRY COLON statements EXCEPT COLON statements
                            | TRY COLON statements EXCEPT COLON statements FINALLY COLON statements'''
    if len(p) == 7:
        p[0] = {"type": "try_except", "try_body": p[3], "except_body": p[6]}
    else:
        p[0] = {"type": "try_except", "try_body": p[3], "except_body": p[6], "finally_body": p[10]}


def p_import_statement(p):
    '''import_statement : IMPORT ID
                        | FROM ID IMPORT ID'''
    if len(p) == 3:
        p[0] = {"type": "import", "module": p[2]}
    else:
        p[0] = {"type": "from_import", "module": p[2], "name": p[4]}


def p_class_definition(p):
    '''class_definition : CLASS ID COLON statements
                        | CLASS ID LPAREN ID RPAREN COLON statements'''
    if len(p) == 5:
        p[0] = {"type": "class", "name": p[2], "body": p[4]}
    else:
        p[0] = {"type": "class", "name": p[2], "parent": p[4], "body": p[7]}


def p_empty(p):
    'empty :'
    pass


def p_error(p):
    if p:
        print(f"ವಾಕ್ಯ ರಚನಾ ದೋಷ/Syntax error at '{p.value}'")
    else:
        print("ವಾಕ್ಯ ರಚನಾ ದೋಷ/Syntax error at EOF")


# Create the parser
parser = yacc.yacc()


def parse(code):
    try:
        # Input the code into the lexer
        lexer.input(code)

        # Parse the code and generate the AST
        result = parser.parse(code, lexer=lexer, debug=False)  # Set debug=True for detailed parsing logs

        # Print the parsed AST for debugging
        print("Parsed AST:")
        print(result)

        return result
    except SyntaxError as e:
        # Handle syntax errors
        print(f"ವಾಕ್ಯ ರಚನಾ ದೋಷ/Syntax error: {e}")
        return None
    except Exception as e:
        # Handle other unexpected errors
        print(f"ಅನಿರೀಕ್ಷಿತ ದೋಷ/Unexpected error: {e}")
        return None


if __name__ == "__main__":
    # Test the parser
    test_code = """
    ಪ್ರಾರಂಭಿಸಿ
        ಮುದ್ರಿಸಿ("ನಮಸ್ಕಾರ ವಿಶ್ವ")
    ಮುಗಿಯಿರಿ
    """

    result = parse(test_code)
    print(result)