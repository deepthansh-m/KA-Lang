from parser import parse  # Ensure this import is at the top of the file

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
            print(value)  # Print the actual program output
            return None

        elif node_type == 'assignment':
            value = self.evaluate_expression(node['value'])
            self.variables[node['target']] = value
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
            # Simplified import handling
            print(f"Imported module: {node['module']}")
            return None

        elif node_type == 'from_import':
            # Simplified from-import handling
            print(f"Imported {node['name']} from {node['module']}")
            return None

        elif node_type == 'class':
            # Simplified class definition handling
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
            return expr['value']

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
            if op == 'ADD':
                return left + right
            elif op == 'SUBTRACT':
                return left - right
            elif op == 'MULTIPLY':
                return left * right
            elif op == 'DIVIDE':
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
            # User-defined function
            func_def = self.functions[func_name]
            args = [self.evaluate_expression(arg) for arg in node['args']]

            # Create new scope with parameters
            old_vars = self.variables.copy()

            # Set parameters in the new scope
            for i, param in enumerate(func_def['params']):
                if i < len(args):
                    self.variables[param] = args[i]
                else:
                    self.variables[param] = None  # Default to None

            # Execute function body
            result = self.evaluate(func_def['body'])

            # Restore old scope
            self.variables = old_vars

            if result and result.get('type') == 'return':
                return result['value']
            return None

        elif func_name == 'ಗುಣಿಸು' or func_name == 'multiply':
            # Built-in multiply function
            args = [self.evaluate_expression(arg) for arg in node['args']]
            if len(args) == 2:
                return args[0] * args[1]
            else:
                raise ValueError("ಗುಣಿಸು ಕ್ರಿಯೆಗೆ ಎರಡು ಮೌಲ್ಯಗಳು ಬೇಕು/multiply needs two arguments")

        elif func_name == 'ಕೂಡಿಸು' or func_name == 'add':
            # Built-in add function
            args = [self.evaluate_expression(arg) for arg in node['args']]
            return sum(args)

        else:
            raise NameError(f"ಅಪರಿಚಿತ ಕಾರ್ಯ/Unknown function: {func_name}")


# Define the run_compiler function outside the class
def run_compiler(code):
    try:
        # Parse code
        ast = parse(code)

        # Execute code
        interpreter = KannadaInterpreter()

        # Redirect standard output to capture program output
        import io
        from contextlib import redirect_stdout

        output_capture = io.StringIO()
        with redirect_stdout(output_capture):
            interpreter.evaluate(ast)  # Execute the program

        # Get the captured program output
        program_output = output_capture.getvalue()

        # Prepare the final output
        output = program_output.strip()  # Remove extra newlines
        output += "\nಯಶಸ್ವಿಯಾಗಿ ಕಾರ್ಯಗತಗೊಂಡಿದೆ/Successfully executed"

        return output
    except Exception as e:
        return f"ದೋಷ/Error: {str(e)}"


# Test the interpreter
if __name__ == "__main__":
    test_code = """
    ಪ್ರಾರಂಭಿಸಿ
        ಮುದ್ರಿಸಿ(9)
    ಮುಗಿಯಿರಿ
    """

    output = run_compiler(test_code)
    print(output)