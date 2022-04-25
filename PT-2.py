import parser
import re
from grammar import Grammar
import sys

term,prods,axioma = parser.parser_file("test_FF")

print("S:",axioma)
g = Grammar(term,prods)


table,reg,num_term = g.gen_table()

reg = re.compile(reg)

g.print()

pode = True

if g.is_ll() and pode:
	for line in sys.stdin:
		#nome da regra,numero da regra,onde na regra
		name_p = axioma
		ind_p = 0
		pos_p = 0
		stack = []

		while line:
			match = reg.match(line)
			p_n = table[name_p][match.lastindex-1]
			if p_n != None:
				line = line[match.end():]
				pos_p += 1
				p = prods[name_p][ind_p]

				while pos_p > len(p) and p[pos_p] in term and line:
						match = reg.match(line)
						if term[match.lastindex - 1] == p[pos_p]:
							pos_p += 1
							line = line[match.end():]

				print(p,pos_p,len(p))
				if pos_p >= len(p):
					if len(stack) <= 1:
						print("frase pertence")
						line = []
					elif stack:
						name_p,ind_p,pos_p = stack.pop()
				else:
					stack.append((name_p,ind_p,pos_p))
					name_p,ind_p,pos_p = (p[pos_p],p_n,0)


			else:
				line = []
				print("frase n pertence")
else:
	g.print_errors()