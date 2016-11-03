import sys, getopt
import json
import string
import gensim
import * from variables.py

topWords = []
topWordsFile = "google-10000-english.txt"

def buildTop():
	numWords = 1
	with open(topWordsFile, 'r') as f:
		for line in f:
			if numWords > NUM_FREQ_WORDS:
				break
			line = line.strip()
			topWords.append(line)
			numWords += 1

def simpleParse(source, dest):
	fDest = open(dest, 'a')
	with open(source, 'r') as fSource:
		for line in fSource:
			commentObj = json.loads(line)
			comment = commentObj[u'body']
			try:
				comment = str(comment)
			except UnicodeEncodeError:
				continue
			comment = comment.split()
			words = [0]*NUM_FREQ_WORDS
			for word in comment:
				wordNoPunct = word.translate(string.maketrans("",""), string.punctuation)
				if wordNoPunct.lower() in topWords:
					words[topWords.index(wordNoPunct.lower())] += 1
			wordsStr = ','.join(str(x) for x in words)
			fDest.write(wordsStr)
			fDest.write('\n')
	fDest.close()

def word2vecParse(source, dest):
	fDest = open(dest, 'a')
	with open(source, 'r') as fSource:
		for line in fSource:
			commentObj = json.loads(line)
			comment = commentObj[u'body']
			try:
				comment = str(comment)
			except UnicodeEncodeError:
				continue
			comment = comment.split()
			words = [0]*10000
			for word in comment:
				wordNoPunct = word.translate(string.maketrans("",""), string.punctuation)
				if wordNoPunct.lower() in topWords:
					words[topWords.index(wordNoPunct.lower())] += 1
			wordsStr = ','.join(str(x) for x in words)
			fDest.write(wordsStr)
			fDest.write('\n')
	fDest.close()	

def main(argv):
	buildTop()
	source = ''
	dest = ''
	try:
		opts, args = getopt.getopt(argv,"i:o:")
	except getopt.GetoptError:
		print 'Usage: processData.py -i <input file> -o <output file>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-i":
			source = arg
		elif opt == "-o":
			dest = arg
	simpleParse(source, dest)

if __name__ == "__main__":
	main(sys.argv[1:])