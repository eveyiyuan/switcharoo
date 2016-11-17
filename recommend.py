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
				print vec
				vec = []
				isEnd = False

	return np.array(jokeEmbedding)

def loadJokes(source):
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
	try:
		opts, args = getopt.getopt(argv,"e:j:")
	except getopt.GetoptError:
		print 'Usage: recommend.py -e <joke embedding file> -j <raw jokes file>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-e":
			embeddedData = arg
		elif opt == "-j":
			jokes = arg

	#embedding = loadEmbedding(embeddedData)
	jokesVec = loadJokes(jokes)
	jokesVecRaw = deepcopy(jokesVec)
	#avg = AvgCommentEmbedder()
	response = raw_input("Please enter your sentence: ")
	wm = WordMover(jokes=jokesVec)
	#response = "I saw a cool dog"
	#responseVec = avg.embedComment(response)
	best, idx = wm.findBest(response)
	# print idx
	print jokesVecRaw[idx]
	#print jokesVec[375423]
	#print jokesVec

if __name__ == "__main__":
	main(sys.argv[1:])