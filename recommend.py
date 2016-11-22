import numpy as np
import gensim
import json
import string
import sys, getopt
from averager import AvgCommentEmbedder
from wordmover import WordMover
from numpy.linalg import norm
from copy import deepcopy

def loadEmbedding(source):
	''' Loads a file of embedded jokes into memory. Joke embedding vectors should
	    be vectors of floats.
	'''
	vec = []
	jokeEmbedding = []
	isEnd = False
	with open(source, 'r') as f:
		for line in f:
			vals = line.split()
			if vals[0] == '[':
				vals = vals[1:]
			if vals[0][0] == '[':
				vals[0] = vals[0][1:]
			if vals[-1] == ']':
				vals = vals[:-1]
				isEnd = True
			elif  vals[-1][-1] == ']':
				vals[-1] = vals[-1][:-1]
				isEnd = True
			for v in vals:
				vec.append(float(v))
			if isEnd == True:
				jokeEmbedding.append(vec)
				vec = []
				isEnd = False

	return np.array(jokeEmbedding)

def loadJokes(source):
	''' Loads jokes from submissions in JSON form into memory. Jokes are comprised of
		the joke title and joke body
	'''
	jokes = []
	with open(source, 'r') as f:
		for line in f:
			commentObj = json.loads(line)
			try:
				joke = str(commentObj[u'title']) + "\n" + str(commentObj[u'selftext'])
			except UnicodeEncodeError:
				continue
			jokes.append(joke)

	return jokes


def euclideanDistance(x, y):
    """
    Returns the Euclidean distance between the lists of numbers x and y.
    """
    return norm(np.array(x) - np.array(y))

def findSuggestion(postVec, embedding, jokes):
    """
    Takes in a post to reply to. Finds the embedding of that post,
    looks for the most similar joke, and returns the text of it.
    """
    minDist = sys.maxint
    minIdx = -1
    for idx, joke in enumerate(embedding):
        dist = euclideanDistance(postVec, joke)
        if dist < minDist:
        	minDist = dist
        	minIdx = idx
    return jokes[minIdx]
    

def main(argv):
	embeddedData = ''
	jokes = ''
	embedType = ''
	numJokes = ''
	try:
		opts, args = getopt.getopt(argv,"e:j:t:n:")
	except getopt.GetoptError:
		print 'Usage: recommend.py -e <joke embedding file> -j <raw jokes file> -t <type: 1 for averager, 0 for wordmover> -n <number of jokes to use in embedding>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-e":
			embeddedData = arg
		elif opt == "-j":
			jokes = arg
		elif opt == "-t":
			embedType = arg
		elif opt == "-n":
			numJokes = arg

	jokesVec = loadJokes(jokes)
	jokesVecSmall = jokesVec[:int(numJokes)]
	jokesVecRaw = deepcopy(jokesVecSmall)
	if embedType == '1':
		embedding = loadEmbedding(embeddedData)[:int(numJokes)]
		avg = AvgCommentEmbedder()
	else:
		wm = WordMover(jokes=jokesVecSmall)

	response = raw_input("Please enter your sentence, type STOP to stop: ")
	while response != "STOP":
		#response = "I saw a cool dog"
		if embedType == '1':
			responseVec = avg.embedComment(response)
			print findSuggestion(responseVec, embedding, jokesVecRaw)

		else:
			best, idx = wm.findBest(response)
			print jokesVecRaw[idx]
		response = raw_input("Please enter your sentence, type STOP to stop: ")

if __name__ == "__main__":
	main(sys.argv[1:])