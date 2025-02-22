import ply.lex as lex

# Token list (Fully Kannada-based Programming Language Tokens)
tokens = (
    'NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ID', 'NEWLINE', 'GREATER',
    'LESS', 'EQUAL', 'NOTEQUAL', 'LESSEQUAL', 'GREATEREQUAL',
    'PRINT', 'LPAREN', 'RPAREN', 'ASSIGN', 'COLON', 'COMMA', 'STRING',
    'IF', 'ELSE', 'ELIF', 'WHILE', 'FOR', 'DEF', 'RETURN', 'CLASS', 'TRY',
    'EXCEPT', 'FINALLY', 'BREAK', 'CONTINUE', 'PASS', 'IN', 'RANGE', 'IMPORT',
    'FROM', 'AS', 'GLOBAL', 'NONLOCAL', 'START', 'END'
)

# Operator tokens
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_EQUAL = r'=='
t_NOTEQUAL = r'!='
t_GREATER = r'>'
t_LESS = r'<'
t_LESSEQUAL = r'<='
t_GREATEREQUAL = r'>='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r':'
t_COMMA = r','

# Define NUMBER token and convert to integer
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)  # Convert string to integer
    return t

t_STRING = r'\".*?\"|\'[^\']*\''

# Ignore whitespace and tabs
t_ignore = ' \t'

# Handle newlines
def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

# Error handling
def t_error(t):
    print(f"ಅಮಾನ್ಯ ಅಕ್ಷರ/Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Keywords in Kannada
def t_START(t):
    r'ಪ್ರಾರಂಭಿಸಿ'
    t.type = 'START'
    return t

def t_PRINT(t):
    r'ಮುದ್ರಿಸಿ|ಮುದ್ರಣ'
    t.type = 'PRINT'
    return t

def t_END(t):
    r'ಮುಗಿಯಿರಿ'
    t.type = 'END'
    return t

def t_IF(t):
    r'ನಂತರ'
    t.type = 'IF'
    return t

def t_ELSE(t):
    r'ಇಲ್ಲದಿದ್ದರೆ'
    t.type = 'ELSE'
    return t

def t_ELIF(t):
    r'ಇಲ್ಲದಿದ್ದರೆನಂತರ'
    t.type = 'ELIF'
    return t

def t_WHILE(t):
    r'ಯಾವಾಗ'
    t.type = 'WHILE'
    return t

def t_FOR(t):
    r'ನಿಮಿತ್ತ'
    t.type = 'FOR'
    return t

def t_DEF(t):
    r'ನಿರ್ಧರಿಸು|ಕಾರ್ಯ'
    t.type = 'DEF'
    return t

def t_RETURN(t):
    r'ಹಿಂತಿರುಗಿಸು'
    t.type = 'RETURN'
    return t

def t_CLASS(t):
    r'ವರ್ಗ'
    t.type = 'CLASS'
    return t

def t_TRY(t):
    r'ಪ್ರಯತ್ನಿಸು'
    t.type = 'TRY'
    return t

def t_EXCEPT(t):
    r'ಹೊರಹಾಕು'
    t.type = 'EXCEPT'
    return t

def t_FINALLY(t):
    r'ಕೊನೆಗೂ'
    t.type = 'FINALLY'
    return t

def t_BREAK(t):
    r'ಮುರಿದುಬಿಡು'
    t.type = 'BREAK'
    return t

def t_CONTINUE(t):
    r'ಮುಂದುವರಿಸು'
    t.type = 'CONTINUE'
    return t

def t_PASS(t):
    r'ಹೋದರೂ'
    t.type = 'PASS'
    return t

def t_IN(t):
    r'ಒಳಗೆ'
    t.type = 'IN'
    return t

def t_RANGE(t):
    r'ವ್ಯಾಪ್ತಿ'
    t.type = 'RANGE'
    return t

def t_IMPORT(t):
    r'ಆಮದು'
    t.type = 'IMPORT'
    return t

def t_FROM(t):
    r'ಇಂದ'
    t.type = 'FROM'
    return t

def t_AS(t):
    r'ಆಗಿ'
    t.type = 'AS'
    return t

def t_GLOBAL(t):
    r'ಜಾಗತಿಕ'
    t.type = 'GLOBAL'
    return t

def t_NONLOCAL(t):
    r'ಸ್ಥಳೀಯವಲ್ಲದ'
    t.type = 'NONLOCAL'
    return t

# Identifier pattern - supports Kannada and Latin characters
t_ID = r'[\u0C80-\u0CFFa-zA-Z_][\u0C80-\u0CFFa-zA-Z_0-9]*'

# Create the lexer
lexer = lex.lex()

# Test function
def test_lexer(data):
    lexer.input(data)
    tokens_list = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens_list.append(tok)
        print(tok)  # Debug statement to print tokens
    return tokens_list

if __name__ == "__main__":
    # Test the lexer
    test_data = """
    ಪ್ರಾರಂಭಿಸಿ
        ಮುದ್ರಿಸಿ("ನಮಸ್ಕಾರ ವಿಶ್ವ")
        ಮುದ್ರಿಸಿ(9)
    ಮುಗಿಯಿರಿ
    """
    tokens = test_lexer(test_data)
    for token in tokens:
        print(token)