from ply import lex
import re

tokens = ["VIRGULA","CAMPO","SPACE","BEGINSPECIAL","BEGINMODE"]

states = [("special","inclusive"),("mode","exclusive"),("erro","exclusive")]


reg_palavra = r'(([^",\n]?("")?)*|(".*"))'
reg_num = r'(\+|-)?\d+(\.\d+)?'


def t_VIRGULA(t):
	r","
	if t.lexer.atual != "" and not(t.lexer.atual in t.lexer.ids):
		t.lexer.reg += (r'(?P<{0}>'+reg_palavra+'),').format(t.lexer.atual)
		t.lexer.ids.add(t.lexer.atual)
		t.lexer.atual = ""
	else:
		print("Erro campo sem identificador ou identificador repetido")
		t.lexer.reg = ""
		t.lexer.begin("erro")

def t_special_VIRGULA(t):
	r","
	t.lexer.count -= 1
	if t.lexer.count == 0:
		if not (t.lexer.atual[0][0] in t.lexer.ids) and t.lexer.atual[0][0] != "":
			t.lexer.reg += r"(?P<{0}>".format(t.lexer.atual[0][0])
			t.lexer.ids.add(t.lexer.atual[0][0])
			t.lexer.reg += t.lexer.atual[1].format(t.lexer.atual[2]) + '),'
			t.lexer.pros_proc.append(t.lexer.atual[0])
			t.lexer.atual = ""
			t.lexer.begin("INITIAL")
		else:
			print("Erro campo sem identificador ou identificador repetido")
			t.lexer.reg = ""
			t.lexer.begin("erro")

def t_CAMPO(t):
	r"\w+"
	t.lexer.atual += t.value 

def t_SPACE(t):
	r"[ ]"
	t.lexer.atual += '_' 

def t_special_BEGINMODE(t):
	r"::"
	t.lexer.begin("mode")

def t_mode_CAMPO(t):
	r"\w+"
	modes = {'sum' : reg_num,'media' : reg_num,"concat":reg_palavra}
	if t.value in modes:
		t.lexer.atual = ((t.lexer.atual[0][0] + "_" + t.value,t.value),t.lexer.atual[1],modes[t.value])#TODO proteger caso n exista no dic de modos 
		t.lexer.begin("special")
	else:
		print("Erro modo de agregação não conhecido: {}".format(t.value))
		t.lexer.reg = ""
		t.lexer.begin("erro")

def t_mode_error(t):
	print("Formato de modo não suportado")
	t.lexer.reg = ""
	t.lexer.begin("erro")

def t_BEGINSPECIAL(t):
	r"{.*}"
	t.lexer.begin("special")
	match = re.match(r"{ *(\d+) *(?:, *(\d+) *)?}|{ *, *(\d+) *}",t.value)

	if match:
		if match.group(1): 	
			first = int(match.group(1))

			if match.group(2):
				second = int(match.group(2))
				t.lexer.count = second
				reg = r"({0})," * first + r"({0})?," * (second - first - 1) + r"({0})?"
			else:
				t.lexer.count = first
				reg = r"({0})," * (first - 1) + r"({0})"

		elif match.group(3):
			second = int(match.group(3))
			t.lexer.count = second
			reg = r"({0})?," * (second-1) + r"({0})?"
			
		t.lexer.atual = ((t.lexer.atual,"normal"),reg,".+")
	else:
		print("Erro modo de agregação mal formatado: {}".format(t.value))
		t.lexer.reg = ""
		t.lexer.begin("erro")


def t_erro_CAMPO(t):
	r".+"

t_ANY_ignore = "\t\n"

def t_ANY_error(t):
	print("Erro modo de agregação mal formatado: {}".format(t.value))
	t.lexer.reg = ""
	t.lexer.begin("erro")
	t.lexer.skip(1)

def proc_agre(array,mode):
	array = array.split(",")
	array = [i for i in array if i != '']

	if mode == 'normal':
		ret = '['+','.join(array)+']'
	elif mode == 'sum':
		ret = 0
		for i in array:
			ret += float(i)
		ret = "{:g}".format(ret)
	elif mode == 'media':
		ret = 0
		for i in array:
			ret += float(i)
		ret = "{:g}".format(ret / len(array))
	elif mode == 'concat':
		ret = "".join(array)
	else:
		print('Modo Desconhecido')
		ret = None
	return ret


fd = open("test","r")

lexer = lex.lex()
lexer.reg = r"^"
lexer.atual = ""
lexer.pros_proc = []
lexer.count = 0
lexer.ids = set()

lexer.input(fd.readline())

for token in lexer:
	print(token)

if(lexer.reg != "" and lexer.count == 0 and not(lexer.atual in lexer.ids)):

	if(lexer.atual != ""): lexer.reg += (r'(?P<{0}>'+reg_palavra+')').format(lexer.atual)
	else: lexer.reg = lexer.reg[:-1]

	lexer.reg += r"$"

	print(lexer.reg)

	reg = re.compile(lexer.reg)

	line_count = 0

	for line in fd:
		line_count+=1
		proc = reg.match(line)
		if proc:
			dic = proc.groupdict()
			#processa e passa json 
			for group,mode in lexer.pros_proc:
				dic[group] = proc_agre(dic[group],mode)
			print(dic)
				
		else:
			print('Error in line: {}'.format(line_count))

else:
	print("ERRO")