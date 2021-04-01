import nltk

class Morphology:
	

	def __init__(self):
		self.tagged_sents = nltk.corpus.mac_morpho.tagged_sents()
		self.unigramTagger = None
		self.check_tagger = False

	def tagger(self):
		 		
		print("Started tagger")
		print("="*40)

		self.tagger = nltk.tag.UnigramTagger(self.tagged_sents)
		self.check_tagger = True
		
		print("="*40)
		print("Completed tagger")
		return True

	def tokenize(self, input):

		if self.check_tagger == True:
			self.token = nltk.word_tokenize(input)
			return True
		else:
			return False 

	def getToken(self):
		return self.tagger.tag(self.token)
		