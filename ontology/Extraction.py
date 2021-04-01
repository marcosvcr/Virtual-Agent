class Extraction:	

	def __init__(self):
		self.pronouns = ["PROADJ", "PRO-KS", "PRO-KS-REL", "PROPESS", "PROSUB","ADV"]	
		self.namesClass = ['NPROP', 'N', None]
		self.hotkeys = [("divisão","D"), ("laboratório","D"),("departamento","D"), ("trabalha","D"), ("ramal","R"), ("telefone", "R"), ("e-mail","E")]
		self.errors = [('do','PREP'),('da','PREP'), ('e-mail','N')]

	def namesHotkeys(self, phrase):
		self.tags = {'names': '','D': False, 'R': False, 'E': False}
		self.phrase = phrase
		self.corrections() 
		self.extract_hotkeys()
		self.extract_names()

	def corrections(self):

		for i in self.phrase:
			for j in self.errors:
				if j[0] == i[0]:
					i_pos = self.phrase.index(i)
					self.phrase.remove(i)
					self.phrase.insert(i_pos,j)


	def extract_names(self):		
		for i in self.phrase:			
			for j in self.namesClass:
				if i[1] == j:
					self.tags['names']=self.tags['names'] + i[0] + ' '


		self.tags['names']=str.rstrip(self.tags['names'])


	def extract_hotkeys(self):
		for i in self.phrase:
			for j in self.hotkeys:
				if j[0] in i[0]:
					self.tags[j[1]]=True
					self.phrase.remove(i)

	def getSearch(self):
		return self.tags

					


