import parser
import re
from grammar import Grammar
import sys

#term -> simbolos terminais
#prods -> produçoes (dic key = nome da produçao | value lista das sua reproduçoes)

error = False

if(len(sys.argv) == 2):

	input_file = sys.argv[1]
else:
	error = True
	print("Intruduza nome do ficheiro")

if not(error):
	term,prods,axioma,act_sem,codex,error = parser.parser_file(input_file)

'''
print(term,end="\n\n")
for i in prods:
	print(i,prods[i])
'''


#print(error)
try:
	if not(error):g = Grammar(term,prods,axioma)
except:
	error = True
#g.print()

if not(error) and g.is_ll():

	table = g.gen_table()

	imports = "from ply import lex\nimport sys\nfrom copy import deepcopy\n\n"

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

	declaration = "def {}_{}(p,t):"

	default = "return None"

	dic_sem = "{"

	act_sem_t = "\n"

	for i in act_sem:
		dic_sem += "'{}':[".format(i)
		for j in range(len(act_sem[i])):
			act_sem_t += declaration.format(i,j) + "\n"
			act_sem_t += (act_sem[i][j] if act_sem[i][j] != "" else default)  + "\n\n"
			dic_sem +=  "{}_{},".format(i,j)
		dic_sem = dic_sem[:-1] + "],"
	dic_sem = dic_sem[:-1] + "}"
		

#--------------------------Codigo--------------------------------------------------

	class_aux = '''
class Auxiliar:
	pass

t = Auxiliar()

'''

	code = '''

lexer = lex.lex()

input = sys.stdin

error = False

mode_file = False

antigo_aux = deepcopy(t)

if len(sys.argv) >=2:
	if len(sys.argv) == 3 and sys.argv[1] == "-f":
		try:
			file = open(sys.argv[2],"r")
			input = [file.read()]
			mode_file = True
		except:
			print("File not found") 
	else:
		print("Argumentos não reconhecidos") 

if not(error):
	for line in input:
		if not(mode_file):
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
				ret = func(arg,t)
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
			if token == "":token = "Terminal"
			print("Erro na posição:",lexer.lexpos,"no grupo (",token,")")
		t = deepcopy(antigo_aux)

	if mode_file:
		file.close()
'''.format(axioma,prods,term,table,dic_sem)

	fd = open(input_file + "_parser.py","w")
	fd.write(imports + lexer_code + act_sem_t + class_aux + codex + code + table)
	fd.close()

else:
	if not(error):g.print_errors()
