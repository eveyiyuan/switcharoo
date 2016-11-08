# Finds 3 comment strings and turns them into a frequency vector represenation.

import numpy as np
import sys, getopt, string
import json

NUM_FREQ_WORDS = 10000

# Stolen from Eve's code.
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

def convertJSON(filename):
	'''
	Converts a file of JSON objects into a Python list of translated JSON
	objects.
	'''
	f = open(filename, 'r')
	objs = []
	for line in f:
		objs.append(json.loads(line))
	f.close()
	return objs

def glueJSON(grandparent_filename, parent_filename, child_filename):
	'''
	Inefficient way to glue together 3 comment chains together into a nested
	JSON object.
	'''
	grandparents = convertJSON(grandparent_filename)
	parents = convertJSON(parent_filename)
	children = convertJSON(child_filename)
	combined = []
	for child in children:
		parent_id1 = child[u'parent_id']
		for parent in parents:
			if parent[u'name'] == parent_id1:
				parent_id2 = parent[u'parent_id']
				for grandparent in grandparents:
					if grandparent[u'name'] == parent_id2:
						new_obj = dict()
						new_obj[u'grandparent'] = grandparent
						new_obj[u'parent'] = parent
						new_obj[u'child'] = child
						combined.append(new_obj)
						break
				break
	return combined

def writeJSON(filename, json_list):
	'''
	Takes a filename and a Python list of Python-translated JSON objects
	(becomes valid JSON after a call to json.dumps()) and (over)writes it
	with each line of the new file being a JSON object in the list.
	'''
	f = open(filename, 'w')
	for obj in json_list:
		f.write(json.dumps(obj) + '\n')
	f.close()

def makeVector(obj):
	'''
	Takes in a nested JSON file in the form of glueJSON() and turns it into
	a Python list which is the concatenation of the word frequencies of the
	individual comments.
	'''
	# We assume the JSON object has been translated into a Python dictionary.
	vector = []
	for key in obj:
		comment = obj[key][u'body']
		try:
			comment = str(comment)
		except UnicodeEncodeError:
			continue
		comment = comment.split()
		words = [0] * NUM_FREQ_WORDS
		for word in comment:
			wordNoPunct = word.translate(string.maketrans("",""), string.punctuation)
			if wordNoPunct.lower() in topWords:
				words[topWords.index(wordNoPunct.lower())] += 1
		vector += words
	return vector

def writeCSV(json_objs, filename):
	buildTop()
	f = open(filename, 'w')
	for obj in json_objs:
		vector = makeVector(obj)
		cs_vector = ','.join(str(x) for x in vector)
		f.write(cs_vector + '\n')
	f.close()

def main():
	grandparent = 'negative_data/P3.json'
	parent = 'negative_data/P2.json'
	children = 'negative_data/P1.json'
	filename = 'negative_examples3.csv'
	combined_json = glueJSON(grandparent, parent, children)
	#writeCSV(combined_json, filename)
	writeJSON('all3negative.json', combined_json)

if __name__ == '__main__':
	main()


