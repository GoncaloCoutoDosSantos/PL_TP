from ply import lex
import re

tokens = ["VIRGULA","CAMPO","SPACE","BEGINSPECIAL","BEGINMODE"]

states = [("special","inclusive"),("mode","exclusive"),("erro","exclusive")]


reg_palavra = r'(([^",\n]?("")?)*|(".*"))'
reg_num = r'(\+|-)?\d+(\.\d+)?'
reg_bool = r'true|false'

#Token que capta virgulas no modo especial
#Responsavel por contar as virgulas que ja apareceram e que falta e de voltar ao modo normal

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

#Token do estado especial responsavel por identificar que um modo esta a começar

def t_special_BEGINMODE(t):
	r"::"
	t.lexer.begin("mode")

#Token do modo modo responsavel pela identificação do modo e qual  o regex capaz de detetar a informação 

def t_mode_CAMPO(t):
	r"\w+"
	modes = {'sum' : reg_num,'media' : reg_num,"concat":reg_palavra,"str":reg_palavra,"bool":reg_bool}
	if t.value in modes:
		t.lexer.atual = ((t.lexer.atual[0][0] + "_" + t.value,t.value),t.lexer.atual[1],modes[t.value])#TODO proteger caso n exista no dic de modos 
		t.lexer.begin("special")
	else:
		print("Erro modo de agregação não conhecido: {}".format(t.value))
		t.lexer.reg = ""
		t.lexer.begin("erro")

#Error do estado modo que moda para o estado erro uma vez que ja não e possivel processar o cabeçalho 

def t_mode_error(t):
	print("Formato de modo não suportado")
	t.lexer.reg = ""
	t.lexer.begin("erro")

#Token de campo no modo erro, capta tudo e é impossivel sair deste modo uma vez que foi encontrado um erro no cabeçalho 

def t_erro_CAMPO(t):
	r".+"

#Token virgula default responsavel por detetar as virgulas verificar se existiu um campo anteriormente e adicionalo ao regex

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

#Token de campo default reponsavel por apanhar os campos do cabeçalho 

def t_CAMPO(t):
	r"\w+"
	t.lexer.atual += t.value 

#Token de espaços default reponsavel por apanhar os espaços do cabeçalho e substitui los por um _ 

def t_SPACE(t):
	r"[ ]"
	t.lexer.atual += '_' 

#Token responsavel por tratar do inicio de uma lista responsavel pelo o tratamento dos limites da mesma 

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
			
		t.lexer.atual = ((t.lexer.atual,"normal"),reg,reg_num)
	else:
		print("Erro modo de agregação mal formatado: {}".format(t.value))
		t.lexer.reg = ""
		t.lexer.begin("erro")

#Token ignore global ignora tabs e new lines

t_ANY_ignore = "\t\n"

#Token erro global

def t_ANY_error(t):
	print("Erro modo de agregação mal formatado: {}".format(t.value))
	t.lexer.reg = ""
	t.lexer.begin("erro")
	t.lexer.skip(1)

#função que processa as listas apos a sua captação conssoante o seu modo de agrefaçao
#array -> a ser pos processado
#mode -> modo de agregação

def proc_agre(array,mode):
	array = array.split(",")
	array = [i for i in array if i != '']

	if mode == 'normal':
		ret = []
		for i in array:
			i = float(i)
			ret.append(i)
	elif mode == 'str':
		ret = []
		for i in array:
			ret.append(i)
	elif mode == 'bool':
		ret = []
		for i in array:
			ret.append(bool(i))
	elif mode == 'sum':
		ret = 0
		for i in array:
			ret += float(i)
		ret = "{:g}".format(ret)
	elif mode == 'media':
		ret = 0
		for i in array:
			ret += float(i)
		ret = "{:g}".format(ret / lenght)
	elif mode == 'concat':
		ret = "".join(array)
	else:
		print('Modo Desconhecido')
		ret = None
	return ret

#inicio do programa 

file = input("Nome do ficheiro:")

fd = open("file","r")

if(fd):
	write_file = open(file + ".json", "w")

	lexer = lex.lex()
	lexer.reg = r"^"
	lexer.atual = ""
	lexer.pros_proc = []
	lexer.count = 0
	lexer.ids = set()

	lexer.input(fd.readline())

	for token in lexer:
		print(token)

	#verificação do se o lexer acabou graciosamente ou não e se o processamento do ultimo elemento foi feito(caso o cabeçalho não acabe em virgulas)
	if(lexer.reg != "" and lexer.count == 0 and not(lexer.atual in lexer.ids)):

		if(lexer.atual != ""): lexer.reg += (r'(?P<{0}>'+reg_palavra+')').format(lexer.atual)
		else: lexer.reg = lexer.reg[:-1]

		lexer.reg += r"$"
		#print(lexer.reg)

		reg = re.compile(lexer.reg)

		line_count = 0

		write_file.write("[\n")

		virg2 = False
		for line in fd:
			if virg2: write_file.write(",\n")
			else: virg2 = True
			line_count+=1
			proc = reg.match(line)
			if proc:
				dic = proc.groupdict()
				#processa e passa json 
				for group,mode in lexer.pros_proc:
					dic[group] = proc_agre(dic[group],mode)
				#print(dic)

				write_file.write("    {\n")
				virg1 = False
				for gr in dic:
					if virg1: write_file.write(",\n")
					else: virg1 = True

					write_file.write("        \"" + gr + "\" : ")

					if type (dic.get(gr)) == str:
						write_file.write("\"" + dic.get(gr).replace('"','\\"') + "\"")
					elif type (dic.get(gr)) == int:
						write_file.write(str(dic.get(gr)))
					elif type (dic.get(gr)) == list:
						write_file.write("[")

						virg = False
						for i in dic.get(gr):	
							if virg: write_file.write(",")
							else: virg = True
							if type (i) == str:
								write_file.write("\"" + i + "\"")
							else:
								write_file.write("{:g}".format(i))

						write_file.write("]")

				write_file.write("\n    }")

					
			else:
				print('Error in line: {}'.format(line_count))

		write_file.write("\n]")

		fd.close()
		write_file.close()

	else:
		print("ERRO")
else:
	print("Não foi possivel abrir o ficheiro")