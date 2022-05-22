import ply.lex as lex

tokens = ['TERMINAL','PAL','LINHAIDENTADA','NUM','LINHA','EXC','CARD','DOTS','BAR','CODE','AST','NEWLINE']

states = [("comment","exclusive"),("linha","exclusive")]

def t_NEWLINE(t):
	r"\n"
	t.lexer.lineno += 1
	return t

def t_TERMINAL(t):
	r'"(?:(?:(?!(?<!\\)").)*)"'
	return t

def t_NUM(t):
	r"\d+"
	return t

def t_PAL(t):  
	r"\w+" 
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

def t_EXC(t):
	r"\!"
	t.lexer.push_state("linha")
	return t

def t_CARD(t):
	r"\#"
	t.lexer.change = True
	return t

def t_COMMENT(t):
	r"'''"
	t.lexer.push_state("comment")

def t_comment_COMMENT(t):
	r"'''"
	t.lexer.pop_state()

def t_comment_PAL(t):
	r".|\s"
	pass

t_comment_ignore = ""

def t_LINHAIDENTADA(t): 
	r"\t[^\n]*"
	return t

def t_linha_LINHA(t):
	r"[^\n]+"

	i = 0 
	flag = True
	while(flag):
		if i < len(t.value) and t.value[i] == " ":
			i += 1
		else:
			flag = False
	t.value = t.value[i:]  
	t.lexer.pop_state()
	return t

def t_linha_NEWLINE(t):
	r"\n"
	t.lexer.pop_state()
	return t

t_linha_ignore = ""


def t_ANY_error(t):
	print("Erro no caracter: ",t.value[0]," \nLinha: ",t.lineno)

t_ignore = " "

fd = open("test_1")
lexer = lex.lex()
lexer.change = False
lexer.nline = 0

'''
for line in fd:
	lexer.input(line)
	for token in lexer:
		print(token)
'''