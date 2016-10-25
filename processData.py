import sys, getopt
import json
import string

topWords = []
topWordsFile = "google-10000-english.txt"
def buildTop():
	with open(topWordsFile, 'r') as f:
		for line in f:
			line = line.strip()
			topWords.append(line)

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