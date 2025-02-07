from parser import parser

def run_compiler(code):
    try:
        result = parser.parse(code)
        return result
    except Exception as e:
        return f"Compilation Error: {str(e)}"