import tkinter as tk
from tkinter import filedialog, messagebox, font, scrolledtext, simpledialog
from parser import parse

class KannadaProgrammingIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("ಕನ್ನಡ ಪ್ರೋಗ್ರಾಮಿಂಗ್ ಭಾಷೆ ಸಂಪಾದಕ / Kannada Programming Language IDE")
        self.root.geometry("1000x800")
        self.kannada_font = font.Font(family="Noto Sans Kannada", size=12)
        self.current_file = None
        self.variables = {}
        self.functions = {}
        self.call_stack = []
        self.create_menu()
        self.create_toolbar()
        self.create_editor_area()
        self.create_output_area()
        self.create_status_bar()
        self.load_example_code()
        self.configure_styles()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="ಹೊಸ / New", command=self.new_file)
        file_menu.add_command(label="ತೆರೆ / Open", command=self.open_file)
        file_menu.add_command(label="ಉಳಿಸು / Save", command=self.save_file)
        file_menu.add_command(label="ಹೀಗೆ ಉಳಿಸು / Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="ನಿರ್ಗಮಿಸು / Exit", command=self.root.quit)
        menubar.add_cascade(label="ಫೈಲ್ / File", menu=file_menu)
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="ಕತ್ತರಿಸು / Cut", command=lambda: self.code_editor.event_generate("<<Cut>>"))
        edit_menu.add_command(label="ನಕಲು / Copy", command=lambda: self.code_editor.event_generate("<<Copy>>"))
        edit_menu.add_command(label="ಅಂಟಿಸು / Paste", command=lambda: self.code_editor.event_generate("<<Paste>>"))
        menubar.add_cascade(label="ಸಂಪಾದನೆ / Edit", menu=edit_menu)
        run_menu = tk.Menu(menubar, tearoff=0)
        run_menu.add_command(label="ಚಲಾಯಿಸು / Run", command=self.run_code)
        menubar.add_cascade(label="ಚಲಾಯಿಸು / Run", menu=run_menu)
        self.root.config(menu=menubar)

    def create_toolbar(self):
        self.toolbar = tk.Frame(self.root, bd=1, relief=tk.RAISED)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)
        run_button = tk.Button(self.toolbar, text="ಚಲಾಯಿಸು / Run", command=self.run_code)
        run_button.pack(side=tk.LEFT, padx=5, pady=2)

    def create_editor_area(self):
        self.code_editor = scrolledtext.ScrolledText(self.root, font=self.kannada_font, wrap=tk.WORD, height=20)
        self.code_editor.pack(expand=True, fill=tk.BOTH)

    def create_output_area(self):
        self.output_area = scrolledtext.ScrolledText(self.root, font=self.kannada_font, wrap=tk.WORD, height=10,
                                                     bg="black", fg="white", state="disabled")
        self.output_area.pack(fill=tk.BOTH)

    def create_status_bar(self):
        self.status_bar = tk.Label(self.root, text="ಸಿದ್ಧ / Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def load_example_code(self):
        example_code = """ಪ್ರಾರಂಭಿಸಿ
    ಹೆಸರು = ಆಗು()
    ಮುದ್ರಿಸಿ(ಹೆಸರು)
    a = ಆಗು()
    ಮುದ್ರಿಸಿ(a)
ಮುಗಿಯಿರಿ"""
        self.code_editor.insert(tk.END, example_code)

    def configure_styles(self):
        self.code_editor.tag_configure("error", foreground="red")

    def new_file(self):
        self.current_file = None
        self.code_editor.delete(1.0, tk.END)
        self.status_bar.config(text="ಹೊಸ ಫೈಲ್ / New File")

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Kannada Files", "*.kn"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                self.code_editor.delete(1.0, tk.END)
                self.code_editor.insert(tk.END, content)
            self.current_file = file_path
            self.status_bar.config(text=f"ತೆರೆಯಲಾಗಿದೆ: {os.path.basename(file_path)}")

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w", encoding="utf-8") as file:
                file.write(self.code_editor.get(1.0, tk.END))
            self.status_bar.config(text=f"ಉಳಿಸಲಾಗಿದೆ: {os.path.basename(self.current_file)}")
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".kn",
                                                 filetypes=[("Kannada Files", "*.kn"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.code_editor.get(1.0, tk.END))
            self.current_file = file_path
            self.status_bar.config(text=f"ಉಳಿಸಲಾಗಿದೆ: {os.path.basename(file_path)}")

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
            self.output_area.configure(state="normal")
            self.output_area.insert(tk.END, f"{value}\n")
            self.output_area.configure(state="disabled")
            self.output_area.see(tk.END)
            self.root.update()  # Force GUI update to show print immediately
            return None

        elif node_type == 'assignment':
            value = self.evaluate_expression(node['value'])
            self.variables[node['target']] = value
            return None

        elif node_type == 'input':
            user_input = simpledialog.askstring("ಒಡ್ಡಿ/Input", "ಒಡ್ಡಿ/Enter input:", parent=self.root) or ""
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
            self.output_area.configure(state="normal")
            self.output_area.insert(tk.END, f"Imported module: {node['module']}\n")
            self.output_area.configure(state="disabled")
            return None

        elif node_type == 'from_import':
            self.output_area.configure(state="normal")
            self.output_area.insert(tk.END, f"Imported {node['name']} from {node['module']}\n")
            self.output_area.configure(state="disabled")
            return None

        elif node_type == 'class':
            class_name = node['name']
            self.output_area.configure(state="normal")
            self.output_area.insert(tk.END, f"Defined class: {class_name}\n")
            self.output_area.configure(state="disabled")
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

    def run_code(self):
        code = self.code_editor.get(1.0, tk.END).strip()
        print(f"Input code:\n{code}")
        self.output_area.configure(state="normal")
        self.output_area.delete(1.0, tk.END)

        try:
            ast = parse(code)
            if ast is None:
                self.output_area.insert(tk.END, "ದೋಷ/Error: Parsing failed due to syntax error\n")
            else:
                self.evaluate(ast)
                self.output_area.insert(tk.END, "ಯಶಸ್ವಿಯಾಗಿ ಕಾರ್ಯಗತಗೊಂಡಿದೆ/Successfully executed\n")
        except Exception as e:
            self.output_area.insert(tk.END, f"ದೋಷ/Error: {str(e)}\n")

        self.output_area.configure(state="disabled")
        print(f"Output:\n{self.output_area.get(1.0, tk.END).strip()}")

if __name__ == "__main__":
    root = tk.Tk()
    app = KannadaProgrammingIDE(root)
    root.mainloop()