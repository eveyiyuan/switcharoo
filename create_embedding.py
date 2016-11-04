import gensim
import os
import json
import sys, getopt
import string
from variables.py import *


class MySentences(object):
	def	__init__(self, dirname):
		self.dirname = dirname

	def __iter__(self):
	for fname in os.listdir(self.dirname):
		for line in open(os.path.join(self.dirname, fname)):
			commentObj = json.loads(line)
			comment = commentObj[u'body']
			try:
				comment = str(comment)
			except UnicodeEncodeError:
				continue
			yield comment.split()

def main():
	source = ''
	dest = ''
	try:
		opts, args = getopt.getopt(argv,"i:o:")
	except getopt.GetoptError:
		print 'Usage: processData.py -i <input directory> -o <output file>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-i":
			source = arg
		elif opt == "-o":
			dest = arg
	sentences = MySentences(source)
	model = gensim.models.Word2Vec(sentences, min_count=MIN_COUNT, size=NN_LAYER_SIZE)
	model.save(dest)
