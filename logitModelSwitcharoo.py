# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:35:04 2016

@author: giraffe
"""

from sklearn import linear_model, metrics
import numpy as np


"""
Takes in two files: one filled with tf-idf representations of random reddit
comments, and the other filled with tf-idf representations of switcharoos.
Trains a basic logistic regression model on this information, and scores it.
"""

def parseCsv(filename):
	f = open(filename, 'r')
	data_matrix = []
	for line in f:
		entries = line.strip().split(',')
		data = [int(i) for i in entries]
		data_matrix.append(data)
	f.close()
	return np.array(data_matrix)

# with open("positive_examples.csv", 'r') as pos,\
#     open("negative_examples.csv", 'r') as neg:
#         pos_raw = np.recfromcsv(pos)
#         neg_raw = np.recfromcsv(neg)
#         pos_raw = parseCsv("positive_examples.csv")
#         neg_raw = parseCsv("negative_examples.csv")
#         pos_labeled = np.append(pos_raw, np.ones([len(pos_raw),1]),1)
#         neg_labeled = np.append(neg_raw, np.zeros([len(neg_raw),1]),1)
#         data = np.vstack(pos_labeled, neg_labeled)

pos_raw = parseCsv("positive_examples.csv")
neg_raw = parseCsv("negative_examples.csv")
pos_labeled = np.append(pos_raw, np.ones([len(pos_raw),1]),1)
neg_labeled = np.append(neg_raw, np.zeros([len(neg_raw),1]),1)
data = np.vstack([pos_labeled, neg_labeled])


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


