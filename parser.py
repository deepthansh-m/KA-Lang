import ply.yacc as yacc
from lexer import tokens, lexer

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def p_program(p):
    '''program : START NEWLINE statements END'''
    p[0] = p[3]

def p_statements(p):
    '''statements : statement
                  | statements statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : print_statement
                 | assignment_statement NEWLINE
                 | input_statement NEWLINE
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
    '''print_statement : PRINT LPAREN expression RPAREN NEWLINE'''
    p[0] = {"type": "print", "value": p[3]}

def p_assignment_statement(p):
    '''assignment_statement : ID ASSIGN expression'''
    p[0] = {"type": "assignment", "target": p[1], "value": p[3]}

def p_input_statement(p):
    '''input_statement : ID ASSIGN INPUT LPAREN RPAREN'''
    p[0] = {"type": "input", "target": p[1]}

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
        elif isinstance(p[1], str) and (p[1].startswith('"') or p[1].startswith("'")):
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

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN COLON statements
                    | IF LPAREN expression RPAREN COLON statements ELSE COLON statements
                    | IF LPAREN expression RPAREN COLON statements ELIF LPAREN expression RPAREN COLON statements'''
    if len(p) == 7:
        p[0] = {"type": "if", "condition": p[3], "body": p[6]}
    elif p[7] == 'ELSE':
        p[0] = {"type": "if", "condition": p[3], "body": p[6], "else_body": p[9]}
    else:
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

parser = yacc.yacc()

def parse(code):
    try:
        lexer.input(code)
        result = parser.parse(code, lexer=lexer, debug=False)
        print("Parsed AST:")
        print(result)
        return result
    except SyntaxError as e:
        print(f"ವಾಕ್ಯ ರಚನಾ ದೋಷ/Syntax error: {e}")
        return None
    except Exception as e:
        print(f"ಅನಿರೀಕ್ಷಿತ ದೋಷ/Unexpected error: {e}")
        return None

class KannadaInterpreter:
    def __init__(self):
        self.variables = {}
        self.functions = {}
        self.call_stack = []

    def evaluate(self, node):
        if isinstance(node, list):
            result = None
            for statement in node:
                result = self.evaluate_statement(statement)
                if result and result.get('type') == 'return':
                    return result
            return result
        else:
            return self.evaluate_statement(node)

    def evaluate_statement(self, node):
        if not node:
            return None

        node_type = node.get('type', '')

        if node_type == 'print':
            value = self.evaluate_expression(node['value'])
            print(value)
            return None

        elif node_type == 'assignment':
            value = self.evaluate_expression(node['value'])
            self.variables[node['target']] = value
            return None

        elif node_type == 'input':
            user_input = input("ಒಡ್ಡಿ/Enter input: ")
            print()  # Newline after input
            self.variables[node['target']] = user_input
            return None

        elif node_type == 'if':
            condition = self.evaluate_expression(node['condition'])
            if condition:
                return self.evaluate(node['body'])
            elif 'else_body' in node:
                return self.evaluate(node['else_body'])

        elif node_type == 'while':
            condition = self.evaluate_expression(node['condition'])
            result = None
            while condition:
                result = self.evaluate(node['body'])
                if result and (result.get('type') == 'return' or
                               result.get('type') == 'break'):
                    break
                condition = self.evaluate_expression(node['condition'])
            return None if result and result.get('type') == 'break' else result

        elif node_type == 'for':
            var_name = node['var']
            start = int(node['start'])
            end = int(node['end'])
            result = None
            for i in range(start, end):
                self.variables[var_name] = i
                result = self.evaluate(node['body'])
                if result and (result.get('type') == 'return' or
                               result.get('type') == 'break'):
                    break
            return None if result and result.get('type') == 'break' else result

        elif node_type == 'function_def':
            self.functions[node['name']] = node
            return None

        elif node_type == 'function_call':
            return self.call_function(node)

        elif node_type == 'return':
            return {'type': 'return', 'value': self.evaluate_expression(node['value'])}

        elif node_type == 'break':
            return {'type': 'break'}

        elif node_type == 'continue':
            return {'type': 'continue'}

        elif node_type == 'pass':
            return None

        elif node_type == 'try_except':
            try:
                return self.evaluate(node['try_body'])
            except Exception as e:
                return self.evaluate(node['except_body'])
            finally:
                if 'finally_body' in node:
                    self.evaluate(node['finally_body'])

        elif node_type == 'import':
            print(f"Imported module: {node['module']}")
            return None

        elif node_type == 'from_import':
            print(f"Imported {node['name']} from {node['module']}")
            return None

        elif node_type == 'class':
            class_name = node['name']
            print(f"Defined class: {class_name}")
            return None

        else:
            return self.evaluate_expression(node)

    def evaluate_expression(self, expr):
        if not expr:
            return None

        if isinstance(expr, (int, float, str, bool)):
            return expr

        expr_type = expr.get('type', '')

        if expr_type == 'number':
            return int(expr['value'])

        elif expr_type == 'string':
            return expr['value']

        elif expr_type == 'identifier':
            name = expr['name']
            if name in self.variables:
                return self.variables[name]
            raise NameError(f"ಅಪರಿಚಿತ ಚರ/Unknown variable: {name}")

        elif expr_type == 'binary_op':
            left = self.evaluate_expression(expr['left'])
            right = self.evaluate_expression(expr['right'])
            op = expr['op']
            if op == '+':
                return left + right
            elif op == '-':
                return left - right
            elif op == '*':
                return left * right
            elif op == '/':
                return left / right

        elif expr_type == 'unary_op':
            operand = self.evaluate_expression(expr['operand'])
            op = expr['op']
            if op == 'NEGATE':
                return -operand

        elif expr_type == 'comparison':
            left = self.evaluate_expression(expr['left'])
            right = self.evaluate_expression(expr['right'])
            op = expr['op']
            if op == 'LESS':
                return left < right
            elif op == 'GREATER':
                return left > right
            elif op == 'EQUAL':
                return left == right
            elif op == 'NOTEQUAL':
                return left != right
            elif op == 'LESSEQUAL':
                return left <= right
            elif op == 'GREATEREQUAL':
                return left >= right

        elif expr_type == 'function_call':
            return self.call_function(expr)

        return None

    def call_function(self, node):
        func_name = node['name']
        if func_name in self.functions:
            func_def = self.functions[func_name]
            args = [self.evaluate_expression(arg) for arg in node['args']]
            old_vars = self.variables.copy()
            for i, param in enumerate(func_def['params']):
                if i < len(args):
                    self.variables[param] = args[i]
                else:
                    self.variables[param] = None
            result = self.evaluate(func_def['body'])
            self.variables = old_vars
            if result and result.get('type') == 'return':
                return result['value']
            return None
        raise NameError(f"ಅಪರಿಚಿತ ಕಾರ್ಯ/Unknown function: {func_name}")

def run_compiler(code):
    try:
        ast = parse(code)
        if ast is None:
            print("ದೋಷ/Error: Parsing failed due to syntax error")
            return
        interpreter = KannadaInterpreter()
        interpreter.evaluate(ast)
        print("ಯಶಸ್ವಿಯಾಗಿ ಕಾರ್ಯಗತಗೊಂಡಿದೆ/Successfully executed")
    except Exception as e:
        print(f"ದೋಷ/Error: {str(e)}")

if __name__ == "__main__":
    test_code = """
    ಪ್ರಾರಂಭಿಸಿ
        ಹೆಸರು = ಆಗು()
        ಮುದ್ರಿಸಿ(ಹೆಸರು)
        a = ಆಗು()
        ಮುದ್ರಿಸಿ(a)
    ಮುಗಿಯಿರಿ
    """
    print(f"Input code:\n{test_code}")
    run_compiler(test_code)