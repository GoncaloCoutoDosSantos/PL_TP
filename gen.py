from ply import lex
import sys

tokens = ["TERM_0" ,"TERM_1" ,"TERM_2" ,"TERM_3" ,"TERM_4"]


def t_TERM_0(t):
	r"\d+"
	t.value = 0
	return t

def t_TERM_1(t):
	r"\("
	t.value = 1
	return t

def t_TERM_2(t):
	r"\)"
	t.value = 2
	return t

def t_TERM_3(t):
	r"\+"
	t.value = 3
	return t

def t_TERM_4(t):
	r"\*"
	t.value = 4
	return t

def t_error(t):
	t.lexer.skip(1)

lexer = lex.lex()

for line in sys.stdin:
	lexer.input(line)

	axioma = "S"
	prods = {'S': [['Exp']], 'Exp': [['"\\d+"'], ['"\\("', 'Funcao', '"\\)"']], 'Funcao': [['"\\+"', 'Lista'], ['"\\*"', 'Lista']], 'Lista': [['Exp', 'Lista'], [None]]}
	term = ['"\\d+"', '"\\("', '"\\)"', '"\\+"', '"\\*"']
	table = {'S': [0, 0, None, None, None], 'Exp': [0, 1, None, None, None], 'Funcao': [None, None, None, 0, 1], 'Lista': [0, 0, 1, None, None]}

	name_p = axioma
	ind_p = 0
	pos_p = 0
	stack = []
	p = prods[name_p][pos_p]

	Erro = False
	Rec = False

	match = lexer.token().value

	while not(Erro or Rec):
		if ind_p >= len(p) or p[ind_p] == None: # acaba prod
			if stack:
				p,ind_p = stack.pop()
			else:
				Rec = True

		elif p[ind_p] in term: # detetou terminal
			ind_p += 1
			match = lexer.token()
			if match:
				match = match.value

		elif match != None: #detetou n terminal
			stack.append((p,ind_p + 1))
			name_p = p[ind_p]
			aux = table[name_p][match]
			if aux != None:
				p = prods[name_p][aux]
				#print(name_p,":",p,"|",match,aux)
				ind_p = 0
			else:
				#print(name_p,match,aux)
				Erro = True
		else:
			Erro = True

	if Erro:
		print("N pertence")
	if Rec:
		print("Pertence")
