from ply import lex
import re

tokens = ["TERM","NORMAL","PROD","FUNC","CODE","COMMENT","END","ERROR"]

states = [("prod","exclusive"),("prodfunc","exclusive"),("func","exclusive"),("funcname","exclusive"),("code","exclusive"),("comment","exclusive")]

#-------------------DEFAULT---------------------------

def t_NORMAL(t):
	r"\w+"
	#print("default normal")
	t.lexer.prod_name = t.value;
	if not(t.lexer.axioma): t.lexer.axioma = t.value #corrigir

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
	t.lexer.aux = ""
	t.lexer.begin("funcname")

def t_COMMENT(t):
	r"'''"
	#print("begin comment")
	t.lexer.push_state("comment")

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
	r"(\n)"
	#print("begin defualt")
	save_prod(t)
	t.lexer.begin("INITIAL")

def t_prod_COMMENT(t):
	r"'''"
	#print("begin comment")
	t.lexer.push_state("comment")

def save_prod(t):
	name = t.lexer.prod_name
	if(name in t.lexer.prods): 
		t.lexer.prods[name].append(t.lexer.prod_atual)
		t.lexer.act_sem[name].append("")
	else: 
		t.lexer.prods[name] = [t.lexer.prod_atual]
		t.lexer.act_sem[name] = [""]
	t.lexer.prod_atual = []


t_prod_ignore = " "

#--------------------PRODFUNC---------------------------

def t_prodfunc_NORMAL(t):
	r".*\n"	
	t.lexer.act_sem[t.lexer.prod_name][-1] = t.value
	t.lexer.begin("INITIAL")

def t_prodfunc_COMMENT(t):
	r"'''"
	#print("begin comment")
	t.lexer.push_state("comment")

t_prodfunc_ignore = " "

#---------------------FUNC-------------------------------

##precisa de ser melhorado para aceitar funçoes sem espaços entre elas
def t_funcname_NORMAL(t):
	r"(.+)(\*(\d+))?:\n"
	t.lexer.aux = re.match(r"(\w+)(?:\*(\d+))?\S*:\S*\n",t.value)
	#print(t.lexer.aux.group(1))
	t.lexer.begin("func")

t_funcname_ignore = " "

def t_func_NORMAL(t):
	r".+(\n|$)"
	if t.lexer.aux.group(1) in t.lexer.act_sem:
		if t.lexer.aux.group(2) == None :
			t.lexer.act_sem[t.lexer.aux.group(1)][0] += t.value.replace("\t","")
		else:
			t.lexer.act_sem[t.lexer.aux.group(1)][int(t.lexer.aux.group(2))] += t.value.replace("\t","")
	else:
		print("Não existe o " + t.lexer.aux.group(1) + " na gramática")
		t.lexer.error = True

def t_func_COMMENT(t):
	r"'''"
	#print("begin comment")
	t.lexer.push_state("comment")

def t_func_END(t):
	r"^[^\t]"
	t.lexer.begin("INITIAL")


t_func_ignore = " "

#----------------------CODE------------------------------

def t_code_NORMAL(t):
	r".+(\n|$)"
	t.lexer.code += t.value
	#print("code normal")


def t_code_END(t):
	r"^[^\t]"
	#print("begin default")
	t.lexer.begin("INITIAL")

def t_code_COMMENT(t):
	r"'''"
	#print("begin comment")
	t.lexer.push_state("comment")

def t_code_ERROR(t):
	r"(\#|''')"
	lexer.error = True
	print("Deixe uma linha vazia entre diferentes entradas")

t_code_ignore = " "

#-----------------------COMMENT--------------------------

#precisa de ser alterado para voltar o modo que estava para permitir fazer comentarios dentro de funçoes

t_comment_NORMAL = r"[^']+"

def t_comment_END(t):
	r"'"
	t.lexer.end_comment += 1
	if(t.lexer.end_comment == 3):
		t.lexer.pop_state()
		t.lexer.end_comment = 0

t_comment_ignore = " \n\t"

#--------------------------------------------------------

def t_ANY_error(t):
	#print("Erro:",t)
	t.lexer.skip(1)

def parser_file(file):

	try:
		fd = open(file,"r")


		lexer = lex.lex()
		lexer.prod_name = ""
		lexer.prod_atual = []
		lexer.prods = {}
		lexer.term = [""]
		lexer.axioma = ""
		lexer.act_sem = {}
		lexer.code = ""
		lexer.end_comment = 0
		lexer.error = False
		for line in fd:
			lexer.input(line)
			for token in lexer:
				pass
				#print(token)
	except:
		print("Ficheiro não foi encontrado")
		lexer.error = True

	return (lexer.term,lexer.prods,lexer.axioma,lexer.act_sem,lexer.code,lexer.error)