# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:35:04 2016

@author: giraffe
"""

import numpy as np
import linecache, json
from sklearn import linear_model, metrics
#from sklearn.model_selection import GridSearchCV

"""
Takes in two files: one filled with tf-idf representations of random reddit
comments, and the other filled with tf-idf representations of switcharoos.
Trains a basic logistic regression model on this information, and scores it.
"""

def parseCsv(filename, limit = 1000):
	f = open(filename, 'r')
	data_matrix = []
	count = 0
	#lengths = dict()
	for line in f:
		if count > limit:
			break
		entries = line.strip().split(',')
		try:
			data = [int(i) for i in entries]
			# if len(data) in lengths:
			# 	lengths[len(data)] += 1
			# else:
			# 	lengths[len(data)] = 1
			# data_matrix.append(data)
			if len(data) == 30000:
				data_matrix.append(data)
				count += 1
		except ValueError:
			continue
	# for key in lengths:
	# 	print key, lengths[key]
	f.close()
	return np.array(data_matrix)

def parseCsv2(filename, limit = 1000):
	'''
	No NumPy array conversion.
	'''
	f = open(filename, 'r')
	data_matrix = []
	count = 0
	for line in f:
		if count > limit:
			break
		entries = line.strip().split(',')
		try:
			data = [int(i) for i in entries]
			data_matrix.append(data)
			count += 1
		except ValueError:
			continue
	f.close()
	return data_matrix

def concatenate(n, nper, vectors):
	concatenated = []
	random_choices = []
	length = len(vectors)
	for i in range(n):
		vector = []
		choices = []
		for i in range(nper):
			rand = np.random.randint(0, length)
			choices.append(rand)
			vector += vectors[rand]
		concatenated.append(vector)
		random_choices.append(choices)
	return (np.array(concatenated), random_choices)



pos_raw = parseCsv("positive_examples3.csv")
#neg_raw = parseCsv("negative_examples3.csv")
temp_neg_raw = parseCsv2("negative_examples.csv")
neg_raw, choices = concatenate(len(pos_raw), 3, temp_neg_raw)
pos_labeled = np.append(pos_raw, np.ones([len(pos_raw),1]),1)
neg_labeled = np.append(neg_raw, np.zeros([len(neg_raw),1]),1)
data = np.vstack([pos_labeled[:1000], neg_labeled[:1000]])


np.random.seed(2016)
np.random.shuffle(data)
# Split into 90% training and 10% testing data.
test = data[:int(.1*data.shape[0]),:]
train = data[int(.1*data.shape[0]):,:]

# Split into X's and Y's.
testX = test[:,:-1]
testY = test[:,-1]
trainX = train[:,:-1]
trainY = train[:,-1]

# Train basic logit model.
basic_model = linear_model.LogisticRegression()
basic_model.fit(trainX, trainY)
score = basic_model.score(testX, testY)
pred = basic_model.predict(testX)
print "The score is", score
print metrics.confusion_matrix(testY, pred)
print metrics.classification_report(testY, pred)

#ind = np.argpartition(basic_model.coef_, -10)[0][-10:]
#for index in ind:
#	print index, basic_model.coef_[0][index]

# Get the log probabilities of each data point in our test set.
log_probs = basic_model.predict_log_proba(testX)
# Get the indices of the top 10 log probabilities. These are already the
# correct shuffled indices in data.
indices = np.argpartition(log_probs[:, 1], -10)[-10:]
# Invert the shuffle.
np.random.seed(2016)
inverse = range(len(data))
np.random.shuffle(inverse)
unshuffled_indices = [inverse[i] for i in indices]
# Get the original lines.
for index in unshuffled_indices:
	if data[index][-1] == 0:
		# Get the blaster from the original json file.
		#line = linecache.getline('all3negative.json', index)
		#obj = json.loads(line)
		#print line.[u'grandparent'][u'body']
		#print line.[u'parent'][u'body']
		#print line.[u'child'][u'body']
		# Look up the random choices we made.
		rand_choices = choices[index]
		for choice in rand_choices:
			line = linecache.getline('negative_examples.json', choice)
			obj = json.loads(line)
			print obj[u'body']
		print 'END OF COMMENT - NEG'
	else:
		# Get the blast from the positive json file.
		line = linecache.getline('all3positive.json', index)
		obj = json.loads(line)
		print obj[u'grandparent'][u'body']
		print obj[u'parent'][u'body']
		print obj[u'child'][u'body']
		print 'END OF COMMENT - POS'

