import numpy as np
import gensim
import json
import string
import sys, getopt
import nmslib_vector
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
				print vec
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
    

def findSuggestionApproximate(postVec, embedding, jokes):
    
    def readData(embeddedJokes):
        """
        Not actually currently used in order to be compatible with our
        (weird) format for storing files, but can be used to avoid storing the
        entire array of embedded jokes in memory once we get to a reasonable
        format of storing files.
        """
        with open(embeddedJokes) as f:
            for line in f:
                yield [float(v) for v in line.strip().split()]
                
    space_type = 'l2' # i.e. Euclidian distance metric.
    space_param = [] # Just sticking with the defaults because they are fine.
    method_name = 'sw-graph' # Approximate search method.
    index_name  = 'smallJokeSet.index' # Name of index file to be created.
    index = nmslib_vector.init(
                             space_type,
                             space_param,
                             method_name,
                             nmslib_vector.DataType.VECTOR,
                             nmslib_vector.DistType.FLOAT)

    # Add each embedded joke to our index.
    idNum = 0
    for embeddedJoke in embedding:
        nmslib_vector.addDataPoint(index, idNum, embeddedJoke)
        idNum += 1

    # Some parameters. Change indexThreadQty as necessary on your machine.
    # NN can be increased to increase recall but decrease speed.
    index_param = ['NN=17', 'initIndexAttempts=3', 'indexThreadQty=4']
    query_time_param = ['initSearchAttempts=3']
    
    nmslib_vector.createIndex(index, index_param)
    nmslib_vector.setQueryTimeParams(index,query_time_param)
    nmslib_vector.saveIndex(index, index_name)

    k = 1 # i.e. find the k nearest neighbors.
    nearestNeighborIDX = nmslib_vector.knnQuery(index, k, postVec)[0]
    # Another option is to have e.g. k = 5 and return the result with
    # the lowest index, i.e. highest rating.
    nmslib_vector.freeIndex(index)
    return jokes[nearestNeighborIDX]

def main(argv):
	embeddedData = ''
	jokes = ''
	embedType = ''
	numJokes = ''
	try:
		opts, args = getopt.getopt(argv,"ej:t:n:")
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
		embedding = loadEmbedding(embeddedData)
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
