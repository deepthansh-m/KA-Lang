import ply.yacc as yacc
from lexer import tokens

def p_program(p):
    '''program : statement
               | program statement'''
    p[0] = p[1] if len(p) == 2 else p[1] + p[2]

def p_statement_print(p):
    '''statement : PRINT LPAREN expression RPAREN
                 | PRINT LPAREN STRING RPAREN'''
    p[0] = f"Print: {p[3]}\n"

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = p[1]

def p_expression_string(p):
    'expression : STRING'
    p[0] = p[1]

def p_statement_assign(p):
    '''statement : ID ASSIGN expression
                 | ID ASSIGN STRING'''
    p[0] = f"Assign {p[1]} = {p[3]}\n"

def p_expression_binop(p):
    '''expression : expression PLUS expression'''
    # Support string concatenation and number addition
    if isinstance(p[1], str) and isinstance(p[3], str):
        p[0] = p[1] + p[3]
    else:
        p[0] = str(float(p[1]) + float(p[3]))

def p_error(p):
    print(f"Syntax error at '{p.value if p else 'Unknown'}'")

parser = yacc.yacc()
