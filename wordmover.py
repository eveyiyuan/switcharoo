# Sample Word Mover comment blaster

import numpy as np
import gensim
import nltk

class WordMover:
	"""
	Implements a simple joke recommendation system. Loads in a database of
	jokes and a word2vec word embedding and uses the word mover algorithm to
	find similar jokes.
	"""

	def __init__(self, jokes, filename = 'GoogleNews-vectors-negative300.bin', binary = True):
		"""
		Takes in a trained word2vec embedding from a file and a list of jokes
		and stores them as member variables.
		"""
		self.model = gensim.models.Word2Vec.load_word2vec_format(filename, binary = binary)
		self.jokesRaw = jokes
		self.jokes = self.tokenize(jokes)
		

	@staticmethod
	def tokenize(jokes):
		stopwords = nltk.corpus.stopwords.words('english')
		for i, joke in enumerate(jokes):
			tokens = joke.strip().lower().split()
			jokes[i] = [word for word in tokens if word not in stopwords]
		return jokes

	def findBest(self, comment):
		best = None
		closest = float('inf')
		tokens = comment.strip().lower().split()
		stopwords = nltk.corpus.stopwords.words('english')
		tokens = [token for token in tokens if token not in stopwords]
		#print self.jokes
		bestIdx = -1
		for idx, joke in enumerate(self.jokes):
			distance = self.model.wmdistance(joke, tokens)
			if distance < closest:
				closest = distance
				best = joke
				bestIdx = idx
		return (self.jokesRaw[bestIdx], bestIdx)

def test():
	jokes = ["pizza burgers fries", "cat dog mouse"]
	model = WordMover(jokes)
	best = model.findBest("I like kittens")
	print best

if __name__ == '__main__':
	test()