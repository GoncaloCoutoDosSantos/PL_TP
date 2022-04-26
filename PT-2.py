import parser
import re
from grammar import Grammar
import sys

#term -> simbolos terminais
#prods -> produçoes (dic key = nome da produçao | value lista das sua reproduçoes)

term,prods,axioma = parser.parser_file("test")

print(term)

g = Grammar(term,prods,axioma)

g.print()

if g.is_ll() and False:

	table = g.gen_table()

	imports = "from ply import lex\nimport sys\n\n"

	token = "tokens = ["

	fun_cap = '''
def t_{0}(t):
	r{1}
	t.value = {2}
	return t
'''

	capture = ""

	for i in range(1,len(term)):
		aux = "TERM_" + str(i)
		token += '"' + aux +"\" ,"
		capture += fun_cap.format(aux,term[i],i)

	token = token[:-2] + "]\n\n"

	err = '''
def t_error(t):
	t.lexer.skip(1)
'''

	lexer_code = token + capture + err

	code = '''
lexer = lex.lex()

for line in sys.stdin:
	lexer.input(line)
'''

	#for i in table:
	#	print(i,":",table[i])

	table = '''
	axioma = "{}"
	prods = {}
	term = {}
	table = {}

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
'''.format(axioma,prods,term,table)

	fd = open("gen.py","w")
	fd.write(imports + lexer_code + code + table)
	fd.close()

else:
	g.print_errors()