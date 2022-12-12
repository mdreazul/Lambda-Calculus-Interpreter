import ply.yacc as yacc
from LambdaLexer import tokens

def p_exprStart(p):
  'exprStart : expr SEMI'
  p[0] = p[1]

def p_substitution(p):
  'exprStart : expr LBRACKET NAME EQUALS expr RBRACKET SEMI'
  p[0] = ['subs',p[1],p[3],p[5]]

def p_free(p):
  'exprStart : FV LBRACKET expr RBRACKET SEMI'
  p[0] = ['free',p[3]]

def p_alpha(p):
  'exprStart : ALPHA LBRACKET expr COMMA NAME RBRACKET SEMI'
  p[0] = ['alpha',p[3],p[5]]

def p_lambda_1(p):
  'expr : NUMBER'
  p[0] = ['num',p[1]]

def p_lambda_2(p):
  'expr : NAME'
  p[0] = ['name',p[1]]

def p_lambda_3(p):
  'expr : LPAREN expr expr RPAREN'
  p[0] = ['twoexp',p[2],p[3]]

def p_lambda_4(p):
  'expr : LPAREN LAMBDA NAME expr RPAREN'
  p[0] = ['lambda',p[3],p[4]]

def p_lambda_5(p):
  'expr : LPAREN OP expr expr RPAREN'
  p[0] = ['op',p[2],p[3],p[4]]

def p_error(p):
  #stack_state_str = ' '.join([symbol.type for symbol in parser.symstack][1:])

  #print('Syntax error in input! Parser State:{} {} . {}'
          #.format(parser.state,
           #       stack_state_str,
            #      p))
  if p == None:
    token = "end of file"
  else:
    token = f"{p.type}({p.value}) on line {p.lineno}"

  print(f"Syntax error: Unexpected {token}")

parser = yacc.yacc()
