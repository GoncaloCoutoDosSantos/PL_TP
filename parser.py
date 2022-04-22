from ply import lex

tokens = ["TERM","NORMAL","PROD","FUNC","CODE","COMMENT","END"]

states = [("prod","exclusive"),("prodfunc","exclusive"),("func","exclusive"),("code","exclusive"),("comment","exclusive")]

#-------------------DEFAULT---------------------------

def t_NORMAL(t):
	r"\w+"
	#print("default normal")
	t.lexer.prod_name = t.value;

def t_PROD(t):
	r":|\|"
	#print("begin prod")
	t.lexer.begin("prod")

def t_CODE(t):
	r"\#\#"
	#print("begin code")
	t.lexer.begin("code")

def t_FUNC(t):
	r"\#"
	#print("begin func")
	t.lexer.begin("func")

def t_COMMENT(t):
	r"'''"
	#print("begin comment")
	t.lexer.begin("comment")

t_ignore = " \n\t"

#---------------------PROD-------------------------------

def t_prod_TERM(t):
	r'"[^"]*"'
	if(t.value != '""'):t.lexer.prod_atual.append(t.value)
	else: t.lexer.prod_atual.append(None)
	if(not(t.value in t.lexer.term) and t.value != '""'):
		t.lexer.term.append(t.value)
	#print("prod term")

def t_prod_FUNC(t):
	r"\#"
	save_prod(t)
	#print("begin func_prod")
	t.lexer.begin("prodfunc")

def t_prod_PROD(t):
	r"\|"
	save_prod(t)
	#print("begin prod")
	t.lexer.begin("prod")

def t_prod_NORMAL(t):
	r"\w+"
	t.lexer.prod_atual.append(t.value)
	#print("prod normal")

def t_prod_END(t):
	r"\n"
	#print("begin defualt")
	save_prod(t)
	t.lexer.begin("INITIAL")

def save_prod(t):
	name = t.lexer.prod_name
	if(name in t.lexer.prods): t.lexer.prods[name].append(t.lexer.prod_atual)
	else: t.lexer.prods[name] = [t.lexer.prod_atual]
	t.lexer.prod_atual = []

t_prod_ignore = " "

#--------------------PRODFUNC---------------------------

def t_prodfunc_NORMAL(t):
	r".+\n"
	#print("begin default")
	t.lexer.begin("INITIAL")

t_prodfunc_ignore = " "

#---------------------FUNC-------------------------------

##precisa de ser melhorado para aceitar funçoes sem espaços entre elas

def t_func_NORMAL(t):
	r".+\n"
	#print("func normal")
	#print(t.value)

def t_func_END(t):
	r"^[^\t]"
	#print("begin default")
	t.lexer.begin("INITIAL")


t_func_ignore = " "

#----------------------CODE------------------------------

def t_code_NORMAL(t):
	r".+\n"
	#print("code normal")

def t_code_END(t):
	r"^[^\t]"
	#print("begin default")
	t.lexer.begin("INITIAL")

t_code_ignore = " "

#-----------------------COMMENT--------------------------

t_comment_NORMAL = r"\S+"

def t_comment_END(t):
	r"'''"
	#print("begin default")
	t.lexer.begin("INITIAL")

t_comment_ignore = " \n\t"

#--------------------------------------------------------

def t_ANY_error(t):
	#print("Erro:",t)
	t.lexer.skip(1)

def parser_file(file):

	fd = open(file,"r")

	lexer = lex.lex()
	lexer.prod_name = ""
	lexer.prod_atual = []
	lexer.prods = {}
	lexer.term = []

	for line in fd:
		lexer.input(line)
		for token in lexer:
			pass
			#print(token)

	return (lexer.term,lexer.prods)