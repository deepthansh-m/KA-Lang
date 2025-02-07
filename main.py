import tkinter as tk
from tkinter import messagebox
from interpreter import run_compiler

def compile_code():
    code = code_text.get("1.0", "end-1c")
    try:
        result = run_compiler(code)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, result)
    except Exception as e:
        messagebox.showerror("Error", f"Error during compilation: {e}")

# Create the main window
root = tk.Tk()
root.title("Kannada Programming Language Editor")

# Code Input Area
code_text = tk.Text(root, height=15, width=100)
code_text.pack(pady=10)

# Compile Button
compile_button = tk.Button(root, text="Compile", command=compile_code)
compile_button.pack(pady=5)

# Output Area
output_text = tk.Text(root, height=10, width=100)
output_text.pack(pady=10)

# Run the application
root.mainloop()