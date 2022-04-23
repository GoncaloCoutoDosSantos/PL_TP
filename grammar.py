class Grammar:

	def __init__(self, term, prods):
		self.term = term
		self.prods = prods
		self.error = set()
		first_p = {}
		follow_p = {}
		appear_p = {}
		lookahead_p = {}

		for i in prods:
			appear_p[i] = set()
			first_p[i] = ([],[])
			lookahead_p[i] = []

		for i in prods:
			for j in prods[i]:
				if j[0] in term:
					if j[0] in first_p[i][0]:
						self.error.add((i,"First/First"))
					else:
						first_p[i][0].append(j[0])
				else:
					first_p[i][1].append(j[0])
				for k in j:
					if k and not( k in term) and k != "":
						appear_p[k].add(i)

		self.first_p = first_p 
		self.follow_p = follow_p
		self.appear_p = appear_p

		for i in prods:
			for j in prods[i]:
				if j[0] in term:
					lookahead_p[i].append([j[0]])
				elif j[0]:
					lookahead_p[i].append(self.first(j[0]))
				else:
					lookahead_p[i].append(self.follow(i))

		self.lookahead_p = lookahead_p

	def first(self,p):
		ret = self.first_p[p][0]

		for i in self.first_p[p][1]:
			if i:
				if i == p:
					self.error.add((p,"Recursividade Esquerda"))
				else:
					aux = self.first(i)
					self.join_arr(ret,aux,(p,"First/First"))
			else:
				aux = self.follow(p)
				self.join_arr(ret,aux,(p,"First/Follow"))

		return ret

	def join_arr(self,a1,a2,e): #funçao auxiliar que junta dois arrais e deteta os erros de tipo First/First Follow/First
		for i in a2:
			if i in a1:
				self.error.add(e)
			else:
				a1.append(i)

	def follow(self,p):
		ret = []
		if p in self.follow_p:
			ret = self.follow_p[p]
		else:
			for i in self.appear_p[p]:
				for j in self.prods[i]:
					ini = 0
					while p in j[ini:]:
						ini = j.index(p,ini) + 1
						if ini >= len(j):
							if i != p:
								ret = ret + self.follow(i)
						else:
							if j[ini] in self.term:
								ret.append(j[ini])
							else:
								ret = ret + self.first(j[ini])
			self.follow_p[p] = ret
		return ret

	def gen_table(self):
		reg = ""
		dic_term = {}
		table = {}
		for i in range(len(self.term)):
			reg += "(" + self.term[i][1:-1] + ")|"
			dic_term[i] = self.term[i]

		reg = reg[:-1]

		for i in self.prods:
			aux = []
			for t in range(len(self.term)):
				aux.append(None)
				for j in range(len(self.lookahead_p[i])):
					if self.term[t] in self.lookahead_p[i][j]:
						aux[t] = j
				table[i] = aux
		return (table,reg,dic_term)


	def print(self):
		for i in self.error:
			print(i)
		print("\n",self.term,end = "\n\n")
		for i in self.prods:
			print("Produção ",i,":")
			print("first:",self.first_p[i])
			if i in self.follow_p:
				print("follow:",self.follow_p[i])
			print("lookahead:")
			for j in self.lookahead_p[i]:
				print(j)
				