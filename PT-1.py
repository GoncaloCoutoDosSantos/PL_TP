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
	aux = t.value[2:]
	t.lexer.atual = ((t.lexer.atual[0][0] + "_" + aux,aux),t.lexer.atual[1],t.lexer.atual[2])

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

fd = open("test","r")

lexer = lex.lex()
lexer.reg = ""
lexer.atual = ""
lexer.pros_proc = []
lexer.count = 0

lexer.input(fd.readline())

for token in lexer:
	print(token)

print(lexer.reg)

reg = re.compile(lexer.reg)

for line in fd:
	proc = reg.match(line)
	if proc:
		#processa e passa json 
		print(proc.groupdict())
	else:
		#linha deu erro 
		pass

for proc in lexer.pros_proc:
	print(proc)