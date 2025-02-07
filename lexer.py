import ply.lex as lex

# Token list (Python-related tokens translated to Kannada)
tokens = (
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ID', 'NEWLINE', 'GREATER',
    'INPUT', 'PRINT', 'LPAREN', 'RPAREN', 'ASSIGN', 'EQUAL', 'IF', 'ELSE',
    'WHILE', 'FOR', 'DEF', 'RETURN', 'INDENT', 'STRING', 'COLON', 'AND', 'OR', 'NOT'
)

# Kannada translations (both Kannada script and Romanized Kannada)
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_EQUAL = r'=='
t_GREATER = r'>'
t_INPUT = r'ಆಗು(ಅವನು|ಅವಳು|ನಾನು) | input'
t_PRINT = r'ಮುದ್ರಣ|print'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r':'
t_ID = r'[a-zA-Z_][a-zA-Z_0-9]*'
t_NUMBER = r'\d+'
t_STRING = r'\".*?\"|\'[^\']*\''
t_AND = r'ಹೌದು|and'
t_OR = r'ಅಥವಾ|or'
t_NOT = r'ಹಾಗೆ ಇಲ್ಲ|not'
t_ignore = ' \t'

# Handle newlines for line tracking
def t_NEWLINE(t):
    r'\n'
    t.lexer.lineno += 1

# Error handling for illegal characters
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Create the lexer object
lexer = lex.lex()