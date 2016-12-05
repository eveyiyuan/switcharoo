# Implements a (sub)gradient descent optimization of the objective function
#
# \argmin_{p}{\sum_{q}{\max{(sign(p - q)S_q, 0)}}}
#
# which represents the loss function which learns the best separating threshold p
# given comment similarities q and corresponding reddit post scores S_q.

import numpy as np
import random


def evaluateObjective(posts, threshold):
    """
    Evaluates the objective function,
        \sum_{q}{\max{(sign(p - q)S_q, 0)}}
    at the given threshold (p) using posts["similarity"] as q and
    posts["score"] as S_q.
    """
    partialSum = 0
    for post in posts:
        partialSum += max(np.sign(threshold - post["similarity"]) * post["score"], 0)
    return partialSum
    

def getThreshold(similarities, scores):
    """
    Returns the threshold that maximimizes the objective function
        \sum_{q}{\max{(sign(p - q)S_q, 0)}}
    Does this by evaluating the objective function at len(similarities) - 1
    points and return the argmin.
    Takes in a list of the the similarity scores for previous posts made, as well
    as a list of Reddit upvote scores for the same posts.
    """
    if len(similarities) < 3:
        return 0 # Default low threshold so that we start making some posts.
    posts = [{"similarity" : similarities[i], "score" : scores[i]}
              for i in range(len(similarities))]
    # Sort by similarity for convenience.
    posts = sorted(posts, key=lambda k: k["similarity"])
    # Possible thresholds are midpoints between similarity scores.
    possibleThresholds = [(posts[i]["similarity"] + posts[i+1]["similarity"]) / 2.0
                           for i in range(len(posts)-1)]
    # Return the threshold that minimizes the objective function.
    return min(possibleThresholds, key=lambda t: evaluateObjective(posts, t))
    
    

def test():
    '''
    Simple test for the threshold code.
    '''
    similarities = [3, 4, 5, 6]
    scores = [-2, -1, 1, 4]
    thresh = getThreshold(similarities, scores)
    print "The threshold is", thresh

if __name__ == '__main__':
    test()


