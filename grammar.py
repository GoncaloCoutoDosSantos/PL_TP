class Grammar:

	def __init__(self, term, prods,axioma):
		self.term = term
		self.prods = prods
		self.error = set()
		first_p = {} # first de uma produçao(terminal ou n )
		follow_p = {}
		follow_p[axioma] = [""] # "" = simbolo terminal
		appear_p = {} # key = produçoa | value = lista de produeçoes onde a key 
		lookahead_p = {}

		for i in prods:
			appear_p[i] = set()
			first_p[i] = ([],[])
			lookahead_p[i] = []


		# prenche o first_p e o appear_p
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
						if k in prods:
							appear_p[k].add(i)
						else:
							print("Não existe definição para a produção:",k)
							raise Exception("")

		self.first_p = first_p 
		self.follow_p = follow_p
		self.appear_p = appear_p
		self.lookahead_p = lookahead_p

		#calculo do lookahead
		#percorre todas as produçoes (descobre o first terminal)

		for i in prods:
			for j in prods[i]:
				if j[0] in term:
					aux = [j[0]]
					self.join_lookahead(i,aux,"First/First")
				elif j[0]:
					aux = self.first(j[0])
					self.join_lookahead(i,aux,"First/First")
				else:
					aux = self.follow(i)
					self.join_lookahead(i,aux,"First/Follow")

		

	def first(self,p):
		ret = self.first_p[p][0]

		for i in self.first_p[p][1]:
			if i:
				if i == p:
					self.error.add((p,"Recursividade Esquerda"))
				else:
					aux = self.first(i)
					self.join_arr_err(ret,aux,(p,"First/First"))
			else:
				aux = self.follow(p)
				self.join_arr_err(ret,aux,(p,"First/Follow"))

		return ret

	def join_lookahead(self,i,l,e):
		aux = []
		for k in l:
			for j in self.lookahead_p[i]:
				if k in j:
					self.error.add((i,e))
			aux.append(k)
		self.lookahead_p[i].append(aux)

	def join_arr_err(self,a1,a2,e): #funçao auxiliar que junta dois arrais e deteta os erros de tipo First/First Follow/First
		for i in a2:
			if i in a1:
				self.error.add(e)
			a1.append(i)

	def join_arr(self,a1,a2):
		for i in a2:
			if not(i in a1):
				a1.append(i)

	def follow(self,p,v = []):
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
							if i != p and not(i in v):
								v.append(i)
								self.join_arr(ret,self.follow(i,v))
								v.pop()
						else:
							if j[ini] in self.term:
								if not(j[ini] in ret):
									ret.append(j[ini])
							else:
								self.join_arr(ret,self.first(j[ini]))
		if v == []: self.follow_p[p] = ret
		return ret

	def gen_table(self):
		table = {}

		for i in self.prods:
			aux = []
			for t in range(len(self.term)):
				aux.append(None)
				for j in range(len(self.lookahead_p[i])):
					if self.term[t] in self.lookahead_p[i][j]:
						aux[t] = j
				table[i] = aux
		return (table)

	def print(self):
		self.print_errors()
		print("\n",self.term,end = "\n\n")
		for i in self.prods:
			print("Produção ",i,":")
			print("first:",self.first_p[i])
			if i in self.follow_p:
				print("follow:",self.follow_p[i])
			print("lookahead:")
			print(self.lookahead_p[i])
			#for j in self.lookahead_p[i]:
				#print(j)

	def print_errors(self):
		for i in self.error:
			print("Erro encontrado na produção {} do tipo: {}".format(i[0],i[1]))

	def is_ll(self):
		return not(len(self.error))