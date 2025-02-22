import tkinter as tk
from tkinter import filedialog, messagebox, font, scrolledtext
from interpreter import run_compiler
import os


class KannadaProgrammingIDE:
    def __init__(self, root):
        self.root = root
        self.root.title("ಕನ್ನಡ ಪ್ರೋಗ್ರಾಮಿಂಗ್ ಭಾಷೆ ಸಂಪಾದಕ / Kannada Programming Language IDE")
        self.root.geometry("1000x800")

        # Set up fonts for Kannada text
        self.kannada_font = font.Font(family="Noto Sans Kannada", size=12)

        # Current file
        self.current_file = None

        # Create main layout
        self.create_menu()
        self.create_toolbar()
        self.create_editor_area()
        self.create_output_area()
        self.create_status_bar()

        # Set initial example code
        self.load_example_code()

        # Configure styles
        self.configure_styles()

    def create_menu(self):
        menubar = tk.Menu(self.root)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="ಹೊಸ / New", command=self.new_file)
        file_menu.add_command(label="ತೆರೆ / Open", command=self.open_file)
        file_menu.add_command(label="ಉಳಿಸು / Save", command=self.save_file)
        file_menu.add_command(label="ಹೀಗೆ ಉಳಿಸು / Save As", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="ನಿರ್ಗಮಿಸು / Exit", command=self.root.quit)
        menubar.add_cascade(label="ಫೈಲ್ / File", menu=file_menu)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="ಕತ್ತರಿಸು / Cut", command=lambda: self.code_editor.event_generate("<<Cut>>"))
        edit_menu.add_command(label="ನಕಲು / Copy", command=lambda: self.code_editor.event_generate("<<Copy>>"))
        edit_menu.add_command(label="ಅಂಟಿಸು / Paste", command=lambda: self.code_editor.event_generate("<<Paste>>"))
        menubar.add_cascade(label="ಸಂಪಾದನೆ / Edit", menu=edit_menu)

        # Run menu
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
        self.code_editor = scrolledtext.ScrolledText(self.root, font=self.kannada_font, wrap=tk.WORD)
        self.code_editor.pack(expand=True, fill=tk.BOTH)

    def create_output_area(self):
        self.output_area = scrolledtext.ScrolledText(self.root, font=self.kannada_font, wrap=tk.WORD, height=10,
                                                     bg="black", fg="white")
        self.output_area.pack(fill=tk.BOTH)

    def create_status_bar(self):
        self.status_bar = tk.Label(self.root, text="ಸಿದ್ಧ / Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def load_example_code(self):
        example_code = """ಪ್ರಾರಂಭಿಸಿ
    ಮುದ್ರಿಸಿ("ನಮಸ್ಕಾರ ವಿಶ್ವ")
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

    def run_code(self):
        code = self.code_editor.get(1.0, tk.END).strip()
        print(f"Input code:\n{code}")  # Debug statement to print input code

        # Run the compiler and get the output
        output = run_compiler(code)

        # Display the output in the IDE's output area
        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, output)

        # Print the output for debugging
        print(f"Output:\n{output}")


if __name__ == "__main__":
    root = tk.Tk()
    app = KannadaProgrammingIDE(root)
    root.mainloop()