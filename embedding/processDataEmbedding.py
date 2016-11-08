import gensim
import json
import sys, getopt
import string
import numpy as np
embeddingLoc = '~/Documents/cs101/switcharoo/embedding/GoogleNews-vectors-negative300.bin'
def genVector(source, dest):
	model = gensim.models.Word2Vec.load_word2vec_format(embeddingLoc, binary=True)
	fDest = open(dest, 'a')
	with open(source, 'r') as fSource:
		for line in fSource:
			tempVec = []
			commentObj = json.loads(line)
			comment = commentObj[u'body']
			try:
				comment = str(comment)
			except UnicodeEncodeError:
				continue
			comment = comment.split()
			first = comment[0].translate(string.maketrans("",""), string.punctuation).lower()
			idx = 1
			try:
				tempVec = model[first]
			except KeyError:
				for i in range(1, len(comment)):
					first = comment[i].translate(string.maketrans("",""), string.punctuation).lower()
					try:
						tempVec = model[first]
					except KeyError:
						continue
					idx = i + 1
					break
			
			tempVec = np.array(tempVec)
			for i in range(idx,len(comment)):
				try: 
					tempVec += np.array(model[comment[i].translate(string.maketrans("",""), string.punctuation).lower()])
				except KeyError:
					continue
			print tempVec

	fDest.close()

def genVectorWithDiff(source1, dest):
	model = gensim.models.Word2Vec.load_word2vec_format(embeddingLoc, binary=True)
	fDest = open(dest, 'a')
	child = True
	tempVec = []
	with open(source, 'r') as fSource:
		while True:
			line = fSource.readline()
			if not line:
				break
			commentObj = json.loads(line)
			comment = commentObj[u'body']
			try:
				comment = str(comment)
			except UnicodeEncodeError:
				continue
			comment = comment.split()
			if child == True:
				child = False
				tempVec = model[comment[0]]
				for i in range(1,len(comment)):
					tempVec += model[comment[i]]
			else:
				child = True
				for word in comment:
					tempVec -= model[word]
				fDest.write(tempVec)
				fDest.write("\n")

	fDest.close()

def main(argv):
	source = ''
	dest = ''
	try:
		opts, args = getopt.getopt(argv,"i:o:")
	except getopt.GetoptError:
		print 'Usage: processDataEmbedding.py -i <input file> -o <output file>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-i":
			source = arg
		elif opt == "-o":
			dest = arg
	genVector(source, dest)

if __name__ == "__main__":
	main(sys.argv[1:])