import parser

term,prods = parser.parser_file("test")

for i in prods:
	print(prods[i])

print(term)