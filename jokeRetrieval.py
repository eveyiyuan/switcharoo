# -*- coding: utf-8 -*-
"""
Created on Sat Nov 12 09:05:33 2016

@author: giraffe
"""

import numpy as np
from numpy.linalg import norm

# Abstract class for comment embedding.

def embedComment(text):
    """
    Takes in the text of a comment and returns an embedding of the comment
    as an n-dimensional array.
    """
    return [-1, 0, 6, 0]

def embedDatabase(path):
    """
    Takes in a filepath (to the database of jokes Eve constructs), parses
    them, embeds each of them, and writes them as CSV data to 'database.csv'.
    Each line in this file should be the embedding of a comment with a final
    column indicating the id of the comment.
    
    I'm not sure how large this database will be, but if it can fit in memory,
    might as well just construct a big ol' object in memory for it instead.
    """
    pass


# Code for joke retrieval.

def euclideanDistance(x, y):
    """
    Returns the Euclidean distance between the lists of numbers x and y.
    """
    return norm(np.array(x) - np.array(y))

def findSuggestion(post):
    """
    Takes in a post to reply to. Finds the embedding of that post,
    looks for the most similar joke, and returns the text of it.
    """
    embeddedPost = embedComment(post)
    for joke in database:
        joke["distance"] = euclideanDistance(embeddedPost, joke["embedding"])
    bestJoke = min(database, key=lambda c: c['distance'])
    return bestJoke["text"]
    
# Test cases:
test1 = [{"text": "This shouldn't be printed for test 1.",
          "embedding" : [1, 2, 3, 4]},
         {"text": "This should be printed for test 1.",
          "embedding" : [0, -1, 7, 0]}]
          
database = test1
print(findSuggestion("test string"))

test2 = [{"text": "This should be printed for test 2.",
          "embedding" : [0, 0, 6, 0]},
         {"text": "This shouldn't be printed for test 2.",
          "embedding" : [0, 0, 0, 0]}]
          
database = test2
    
print(findSuggestion("test string")) # "This should be printed."
