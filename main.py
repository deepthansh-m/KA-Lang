import tkinter as tk
from tkinter import messagebox, font
from interpreter import run_compiler

def compile_code():
    code = code_text.get("1.0", "end-1c")
    try:
        result = run_compiler(code)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, result)
    except Exception as e:
        messagebox.showerror("ದೋಷ/Error", f"ಸಂಕಲನ ದೋಷ/Compilation Error: {e}")

# Create the main window
root = tk.Tk()
root.title("ಕನ್ನಡ ಪ್ರೋಗ್ರಾಮಿಂಗ್ ಭಾಷೆ ಸಂಪಾದಕ / Kannada Programming Language Editor")

# Set up fonts for Kannada text
kannada_font = font.Font(family="Noto Sans Kannada", size=12)

# Create main frame
main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

# Labels
input_label = tk.Label(main_frame, text="ಕೋಡ್ ಬರೆಯಿರಿ / Write Code:", font=kannada_font)
input_label.pack(anchor='w', pady=(5,0))

# Code Input Area
code_text = tk.Text(main_frame, height=15, width=100, font=kannada_font)
code_text.pack(pady=5)

# Add example placeholder text
placeholder_text = """# ಉದಾಹರಣೆ / Example:
ಕಾರ್ಯ ಸಂಖ್ಯೆಕೂಡಿಸು(ಎ, ಬಿ):
    ಹಿಂತಿರುಗಿಸು ಎ ಕೂಡಿಸು ಬಿ

# You can also write in English:
def add_numbers(a, b):
    return a + b"""
code_text.insert("1.0", placeholder_text)

# Frame for buttons
button_frame = tk.Frame(main_frame)
button_frame.pack(pady=5)

# Compile Button
compile_button = tk.Button(
    button_frame,
    text="ಸಂಕಲನ / Compile",
    command=compile_code,
    font=kannada_font,
    bg="#4CAF50",
    padx=20
)
compile_button.pack(side=tk.LEFT, padx=5)

# Clear Button
def clear_code():
    code_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)

clear_button = tk.Button(
    button_frame,
    text="ತೆರವುಗೊಳಿಸು / Clear",
    command=clear_code,
    font=kannada_font,
    bg="#f44336",
    padx=20
)
clear_button.pack(side=tk.LEFT, padx=5)

# Output Label
output_label = tk.Label(main_frame, text="ಫಲಿತಾಂಶ / Output:", font=kannada_font)
output_label.pack(anchor='w', pady=(10,0))

# Output Area
output_text = tk.Text(main_frame, height=10, width=100, font=kannada_font)
output_text.pack(pady=5)

# Status bar
status_bar = tk.Label(
    main_frame,
    text="ಸಿದ್ಧ / Ready",
    font=kannada_font,
    bd=1,
    relief=tk.SUNKEN,
    anchor=tk.W
)
status_bar.pack(fill=tk.X, pady=(5,0))

# Set minimum window size
root.minsize(800, 600)

# Configure style
root.configure(bg='#334455')
main_frame.configure(bg='#334455')
button_frame.configure(bg='#334455')
input_label.configure(bg='#334455')
output_label.configure(bg='#334455')

# Run the application
root.mainloop()