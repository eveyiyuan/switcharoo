# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 14:35:04 2016

@author: giraffe
"""

import sklearn
import numpy as np


"""
Takes in two files: one filled with tf-idf representations of random reddit
comments, and the other filled with tf-idf representations of switcharoos.
Trains a basic logistic regression model on this information, and scores it.
"""

with open("positive_examples.csv", 'r') as pos,\
    open("negative_examples.csv", 'r') as neg:
        pos_raw = np.recfromcsv(pos)
        neg_raw = np.recfromcsv(neg)
        pos_labeled = np.append(pos_raw, np.ones([len(pos_raw),1]),1)
        neg_labeled = np.append(neg_raw, np.zeros([len(neg_raw),1]),1)
        data = np.vstack(pos_labeled, neg_labeled)

np.random.seed(2016)
np.random.shuffle(data)
# Split into 90% training and 10% testing data.
test = data[:int(.1*data.shape[0]),:]
train = data[int(.1*data.shape[0]),:]

# Split into X's and Y's.
testX = test[:,:-1]
testY = test[:,-1]
trainX = train[:,:-1]
trainY = train[:,-1]

# Train basic logit model.
basic_model = sklearn.linear_model.LogisticRegressionCV()
basic_model.fit(trainX, trainY)
basic_model.score(testX, testY)

