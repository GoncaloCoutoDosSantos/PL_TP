import ply.lex as lex

tokens = ['TERMINAL','COMMENT','PAL','LINHAIDENTADA','NUM','LINHA','CARDI','CARD','DOTS','BAR','CODE','AST']

states = [("comment","exclusive"),("linha","exclusive")]

def t_TERMINAL(t):
	r'"(?:(?:(?!(?<!\\)").)*)"'
	return t

def t_PAL(t):  
	r"\w+" 
	return t

def t_NUM(t):
	r"\d+"
	return t

def t_AST(t):
	r"\*"
	return t

def t_BAR(t):
	r"(\t|[ ])*\|"
	return t

def t_CODE(t):
	r"\#\#"
	t.lexer.push_state("linha")
	return t

def t_DOTS(t):
	r":"
	if(t.lexer.change):
		t.lexer.change = False
		t.lexer.push_state("linha")
	return t

def t_CARDI(t):
	r"^\#"
	t.lexer.change = True
	return t

def t_CARD(t):
	r"\#"
	t.lexer.push_state("linha")
	return t

def t_LINHAIDENTADA(t): 
	r"^\t.*(\n|$)"
	return t

def t_linha_LINHA(t):
	r"(.+(\n|$))|\n" 
	print(t.value)
	t.lexer.pop_state()
	return t

def t_COMMENT(t):
	r"'''"
	t.lexer.push_state("comment")

def t_comment_COMMENT(t):
	r"'''"
	t.lexer.pop_state()

def t_comment_PAL(t):
	r"."
	pass

def t_ANY_error(t):
	print(t)

t_ignore = " \n"

fd = open("test_1")
lexer = lex.lex()
lexer.change = False

'''
for line in fd:
	lexer.input(line)
	for token in lexer:
		print(token)
'''