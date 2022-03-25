from ply import lex
import re

tokens = ["VIRGULA","CAMPO","BEGINSPECIAL"]

states = [("special","inclusive")]


def t_VIRGULA(t):
	r","
	t.lexer.reg += r"(?P<{0}>.+),".format(t.lexer.atual)

def t_special_VIRGULA(t):
	r","
	t.lexer.count -= 1
	if t.lexer.count == 0:
		t.lexer.reg += r"(?P<{0}>".format(t.lexer.atual[0][0])
		t.lexer.reg += t.lexer.atual[1].format(t.lexer.atual[2]) + ')'
		t.lexer.pros_proc.append(t.lexer.atual[0])
		t.lexer.atual = ""
		t.lexer.begin("INITIAL")

def t_CAMPO(t):
	r"\w+"
	t.lexer.atual = t.value 

def t_special_CAMPO(t):
	r"::\w+"
	modes = {'sum' : r'\d','media' : r'\d'}
	aux = t.value[2:]
	t.lexer.atual = ((t.lexer.atual[0][0] + "_" + aux,aux),t.lexer.atual[1],modes[aux])#TODO proteger caso n exista no dic de modos 

def t_BEGINSPECIAL(t):
	r"{.*}"
	t.lexer.begin("special")
	match = re.match(r"{(\d+)(?:,(\d+))?}",t.value)

	if match.group(1): 	
		first = int(match.group(1))

		if match.group(2):
			second = int(match.group(2))
			t.lexer.count = second
			reg = r"{0}+," * first + r"{0}*," * (second - first - 1) + r"{0}*"
		else:
			t.lexer.count = first
			reg = r"{0}+," * (first - 1) + r"{0}+"

		t.lexer.atual = ((t.lexer.atual,"normal"),reg,".")



t_ignore = "\t\n"

def t_error(t):
	print(t)
	t.lexer.skip(1)

def proc_agre(array,mode):
	array = array.split(",")
	array = [i for i in array if i != '']

	if mode == 'normal':
		ret = []
		for i in array:
			i = int(i)
			ret.append(int(i))
	elif mode == 'sum':
		ret = 0
		for i in array:
			ret += int(i)
	elif mode == 'media':
		ret = 0
		for i in array:
			ret += int(i)
		ret = ret / array.lenght()
	else:
		print('Modo Desconhecido')
		ret = None
	return ret


fd = open("test","r")

write_file = open("result.json", "w")

lexer = lex.lex()
lexer.reg = ""
lexer.atual = ""
lexer.pros_proc = []
lexer.count = 0

lexer.input(fd.readline())

for token in lexer:
	print(token)

#print(lexer.reg)

reg = re.compile(lexer.reg)

line_count = 0


write_file.write("[\n")

for line in fd:
	line_count+=1
	proc = reg.match(line)
	dic = []
	dic = proc.groupdict()
	if proc:
		#processa e passa json 
		for group,mode in lexer.pros_proc:
			dic[group] = proc_agre(dic[group],mode)
		#print(dic)

		write_file.write("    {\n")

		for gr in dic:

			write_file.write("        \"" + gr + "\" : ")

#a unica coisa q falta é tratar das vírgulas, no ultimo caso de cada cena tem sempre uma virgula a mais e eu n sei de q maneira fazer sem ser com contadores

			if type (dic.get(gr)) == str:
				write_file.write("\"" + dic.get(gr) + "\",\n")
			elif type (dic.get(gr)) == int:
				write_file.write(str(dic.get(gr)) + ",\n")
			elif type (dic.get(gr)) == list:
				write_file.write("[")
				for i in dic.get(gr):	
					if type (i) == str:
						write_file.write("\"" + i + "\",")
					elif type (i) == int:
						write_file.write( str(i) + ",")
				write_file.write("],\n")

		write_file.write("    },\n")

			
	else:
		print('Error in line: {}'.format(line_count))

write_file.write("]")

fd.close()
write_file.close()