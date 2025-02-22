from parser import parse

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
            # Prompt user for input and store it in the target variable
            user_input = input("ಒಡ್ಡಿ/Enter input: ")
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
            return "ದೋಷ/Error: Parsing failed due to syntax error"
        interpreter = KannadaInterpreter()
        import io
        from contextlib import redirect_stdout
        output_capture = io.StringIO()
        with redirect_stdout(output_capture):
            interpreter.evaluate(ast)
        program_output = output_capture.getvalue()
        output = program_output.strip()
        output += "\nಯಶಸ್ವಿಯಾಗಿ ಕಾರ್ಯಗತಗೊಂಡಿದೆ/Successfully executed"
        return output
    except Exception as e:
        return f"ದೋಷ/Error: {str(e)}"

if __name__ == "__main__":
    test_code = """
    ಪ್ರಾರಂಭಿಸಿ
        ಹೆಸರು = ಆಗು()
        ಮುದ್ರಿಸಿ(ಹೆಸರು)
    ಮುಗಿಯಿರಿ
    """
    output = run_compiler(test_code)
    print(output)