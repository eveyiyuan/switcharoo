import numpy as np
import gensim
import json
import string
import sys, getopt
from averager import AvgCommentEmbedder

def embedData(source):
	avg = AvgCommentEmbedder()
	with open(source, 'r') as f:
		for line in f:
			commentObj = json.loads(line)
			try:
				joke = str(commentObj[u'title']) + " " + str(commentObj[u'selftext'])
			except UnicodeEncodeError:
				continue
			print avg.embedComment(joke)

def main(argv):
	source = ''
	dest = ''
	try:
		opts, args = getopt.getopt(argv,"i:o:s:")
	except getopt.GetoptError:
		print 'Usage: embedData.py -i <input file> Note you must pipe the output to a file'
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-i":
			source = arg
		elif opt == "-o":
			dest = arg
	embedData(source)

if __name__ == "__main__":
	main(sys.argv[1:])