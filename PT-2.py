import parser
import re
from grammar import Grammar
import sys

#term -> simbolos terminais
#prods -> produçoes (dic key = nome da produçao | value lista das sua reproduçoes)

term,prods,axioma,act_sem = parser.parser_file("test")

g = Grammar(term,prods,axioma)

#g.print()

if g.is_ll():

	table = g.gen_table()

	imports = "from ply import lex\nimport sys\n\n"

#--------------------------Lexer----------------------------

	token = "tokens = ["

	fun_cap = '''
def t_{0}(t):
	r{1}
	t.value = ({2},t.value)
	return t
'''

	capture = ""

	for i in range(1,len(term)):
		aux = "TERM_" + str(i)
		token += '"' + aux +"\" ,"
		capture += fun_cap.format(aux,term[i],i)

	token = token[:-2] + "]\n\n"

	err = '''
def t_eof(t):
	t.value = (0,t.value)
	return t

def t_error(t):
	t.value = (-1,t.value)
	t.lexer.skip(1)
	return t
'''

	lexer_code = token + capture + err

#--------------------------Açoes_Semanticas-----------------------------------------

	declaration = "def {}_{}(p):"

	default = "return None"

	dic_sem = "{"

	act_sem_t = "\n"

	for i in act_sem:
		dic_sem += "'{}':[".format(i)
		for j in range(len(act_sem[i])):
			act_sem_t += declaration.format(i,j) + "\n\t"
			act_sem_t += (act_sem[i][j] if act_sem[i][j] != "" else default)  + "\n\n"
			dic_sem +=  "{}_{},".format(i,j)
		dic_sem = dic_sem[:-1] + "],"
	dic_sem = dic_sem[:-1] + "}"
		

#--------------------------Codigo--------------------------------------------------

	code = '''
lexer = lex.lex()

for line in sys.stdin:
	line = line[:-1]#tira o \\n para ler do stdin
	lexer.input(line)
'''

	#for i in table:
	#	print(i,":",table[i])

	table = '''
	axioma = "{}"
	prods = {}
	term = {}
	table = {}
	act_sem = {}

	name_p = axioma
	ind_p = 0
	pos_p = 0
	stack = []
	p = prods[name_p][pos_p]
	func = act_sem[name_p][pos_p] 
	arg = [] 

	Erro = False
	Rec = False

	match = lexer.token().value
	token = match[1]
	match = match[0]

	while not(Erro or Rec):
		if ind_p >= len(p) or p[ind_p] == None: # acaba prod
			ret = func(arg)
			if stack:
				p,ind_p,func,arg = stack.pop()
				arg.append(ret)
			else:
				Rec = True

		elif p[ind_p] in term: # detetou terminal
			arg.append(token)
			ind_p += 1
			match = lexer.token()
			if match:
				match = match.value
				token = match[1]
				match = match[0]

		elif match != None and match != -1: #detetou n terminal
			stack.append((p,ind_p + 1,func,arg))
			name_p = p[ind_p]
			aux = table[name_p][match]
			if aux != None:
				p = prods[name_p][aux]
				func = act_sem[name_p][aux] 
				arg = [] 
				ind_p = 0
			else:
				Erro = True
		else:
			Erro = True

	if Erro:
		print("N pertence")
	if Rec:
		print("Pertence")
'''.format(axioma,prods,term,table,dic_sem)

	fd = open("gen.py","w")
	fd.write(imports + lexer_code + act_sem_t + code + table)
	fd.close()

else:
	g.print_errors()
