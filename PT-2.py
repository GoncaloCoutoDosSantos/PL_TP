import parser

term,prods = parser.parser_file("test")

for i in prods:
	print(i,":",prods[i])

print(term)
print()
print()
print()

def getfirst(prods,p): #Retorna Term e n Term 
	ret = []
	for i in prods[p]:
		ret.append(i[0])
	return ret

def getfollow(prods,p): #Retorna Term e n Term 
	ret = []
	for i in prods:
		for j in prods[i]:
			if(p in j):
				ini = 0
				while(p in j[ini:]):
					ini = j.index(p) + 1
					#print(ini > len(j),"|ini:",ini,"|j:",len(j))
					if(ini < len(j)):
						ret.append(j[ini])
					else:
						if i == p: ret.append(p)
						else: ret = ret + getfollow(prods,i)
	return ret

def getlookahead(term,prods):
	first_p = {}
	follow_p = {}

	for i in ["Lista2"]:
		if not(i in first_p):
			first_p[i] = []
			first_aux = getfirst(prods,i)
			for f in first_aux:
				print(f," | ",first_aux)
				if f:
					if f in term:
						first_p[i].append(f)
					else:
						if f in first_p:
							first_p[i] = first_p[i] + first_p[f]
						elif f == i: pass
						else:
							first_aux = first_aux + getfirst(prods,f)
				else:
					if f in follow_p:
						first_p[i] = first_p[i] + follow_p[f]
					else:
						first_aux = first_aux + getfollow(prods,f)

	return first_p
				


print(getlookahead(term,prods))