import parser

from grammar import Grammar

term,prods = parser.parser_file("test")

g = Grammar(term,prods)

g.print()		
