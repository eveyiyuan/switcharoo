import json
import string
import sys, getopt

def pruneData(source, dest):
	fDest = open(dest+".json", 'a')
	with open(source, 'r') as f:
		for line in f:
			commentObj = json.loads(line)
			try:
				subreddit = commentObj[u'subreddit']
				isNSFW = commentObj[u'over_18']
				isSelf = commentObj[u'is_self']
				joke = commentObj[u'selftext']
			except KeyError:
				continue
			try:
				joke = str(joke)
			except UnicodeEncodeError:
				continue
			subreddit = str(subreddit).lower()
			if "jokes" in subreddit and isNSFW == False:
				fDest.write(line)

	fDest.close()

def main(argv):
	source = ''
	dest = ''
	try:
		opts, args = getopt.getopt(argv,"i:o:")
	except getopt.GetoptError:
		print 'Usage: pruneDataJokes.py -i <input file> -o <output file name (no extension)>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-i":
			source = arg
		elif opt == "-o":
			dest = arg
	pruneData(source,dest)

if __name__ == "__main__":
	main(sys.argv[1:])