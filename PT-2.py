import parser
import re
from grammar import Grammar
import sys

term,prods,axioma = parser.parser_file("test")

g = Grammar(term,prods)


table,reg,num_term = g.gen_table()

print(reg,end = "\n\n")

for i in table:
	print(i,":",table[i])

print()


reg = re.compile(reg)

#g.print()

pode = True

if g.is_ll() and pode:
	line = "[12,2] "
	#nome da regra,numero da regra,onde na regra
	name_p = axioma
	ind_p = 0
	pos_p = 0
	stack = []
	p = prods[name_p][pos_p]

	Erro = False
	Rec = False

	match = reg.match(line)
	line = line[match.end():]
	while not(Erro or Rec):
		if ind_p >= len(p) or p[ind_p] == None:
			if stack:
				p,ind_p = stack.pop()
			else:
				Rec = True

		elif p[ind_p] in term:
			ind_p += 1
			if line:
				match = reg.match(line)
				line = line[match.end():]
			else:
				Erro = True

		else:
			stack.append((p,ind_p + 1))
			name_p = p[ind_p]
			aux = table[name_p][match.lastindex-1]
			if aux != None:
				p = prods[name_p][aux]
				print(name_p,":",p,"|",match.lastindex-1,aux)
				ind_p = 0
			else:
				print(name_p,match.lastindex-1,aux)
				Erro = True

	if Erro:
		print("N pertence")
	if Rec:
		print("Pertence")

else:
	g.print_errors()