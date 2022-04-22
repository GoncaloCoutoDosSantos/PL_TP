class Grammar:

	def __init__(self, term, prods):
		self.term = term
		self.prods = prods
		first_p = {}
		follow_p = {}
		lookahead_p = {}

		for i in prods:
			follow_p[i] = []
			first_p[i] = []
			lookahead_p[i] = []

		for i in prods:
			for j in prods[i]:
				first_p[i].append(j[0])

		self.first_p = first_p 
		self.follow_p = follow_p
		self.lookahead_p = lookahead_p


	def print(self):
		for i in self.prods:
			print("Produção ",i,":")
			print("first:",self.first_p[i])
			print("follow:",self.follow_p[i])
			print("lookahead:",self.lookahead_p[i],end = "\n\n")
				