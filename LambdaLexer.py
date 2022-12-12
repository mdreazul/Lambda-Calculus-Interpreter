import ply.lex as lex

reserved = { 'lambda': 'LAMBDA', 'fv': 'FV', 'alpha': 'ALPHA' }

tokens = ['NUMBER','LPAREN','RPAREN','OP','NAME','LBRACKET','RBRACKET','EQUALS','COMMA','SEMI'] + list(reserved.values())

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_OP = r'\+|\-|\*|/'
t_LAMBDA = r'[Ll][Aa][Mm][Bb][Dd][Aa]'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_EQUALS = r'='
t_FV = r'[Ff][Vv]'
t_ALPHA = r'[Aa][Ll][Pp][Hh][Aa]'
t_COMMA = r','
t_SEMI = r';'

def t_NUMBER(t):
  r'[-+]?[0-9]+(\.([0-9]+)?)?'
  t.value = float(t.value)
  t.type = 'NUMBER'
  return t

def t_NAME(t):
  r'[a-zA-Z][a-zA-Z0-9]*'
  t.type = reserved.get(t.value.lower(),'NAME')
  return t

# Ignored characters
t_ignore = " \r\n\t"
t_ignore_COMMENT = r'\#.*'

def t_error(t):
  print("Illegal character '%s'" % t.value[0])
  raise Exception('LEXER ERROR')

lexer = lex.lex()
