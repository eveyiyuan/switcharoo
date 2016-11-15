# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 09:05:33 2016

@author: giraffe
"""

import numpy as np
import string
import gensim

# Abstract class for comment embedding.

class CommentEmbedder:
    """
    Abstract base class from which all comment embedders inherit. Provides an
    interface for which each child class implements a different comment
    embedding algorithm.
    """

    @staticmethod
    def tokenize(text):
        """
        Splits up a Python string into a list of strings which is the
        space-separated tokens of the original string. Strips off any
        punctuation in each token, and removes any capitalization.
        """
        comment = text.strip().split()
        # Remove punctuation.
        for i, token in enumerate(comment):
            # Map every character to itself, except delete all punctuation.
            no_punct = token.lower().translate(string.maketrans("",""), string.punctuation)
            comment[i] = no_punct
        return comment

    def embedComment(self, text):
        """
        Takes in the text of a comment and returns an embedding of the comment
        as an n-dimensional array.
        """
        pass

    def embedDatabase(self, path):
        """
        Takes in a filepath (to the database of jokes Eve constructs), parses
        them, embeds each of them, and writes them as CSV data to 'database.csv'.
        Each line in this file should be the embedding of a comment with a final
        column indicating the id of the comment.
        
        I'm not sure how large this database will be, but if it can fit in memory,
        might as well just construct a big ol' object in memory for it instead.
        """
        pass


class AvgCommentEmbedder(CommentEmbedder):
    """
    Given a word embedding, implements the comment embedding by averaging the
    """

    def embedComment(self, text, filename = 'GoogleNews-vectors-negative300.bin'):
        """
        Embeds the comment by averaging the word embedding for each word in
        the embedding.
        """
        # Load in the pretrained model.
        model = gensim.models.Word2Vec.load_word2vec_format(filename, binary = True)
        comment = self.tokenize(text)
        embedding = model[comment[0]]
        for i in range(1, len(comment)):
            try:
                embedding += model[comment[i]]
            except KeyError:
                continue
        embedding = embedding / len(comment)
        return embedding


class BoWCommentEmbedder(CommentEmbedder):
    """
    Given a word embedding, implements the bag of words comment embedding,
    turning a comment into a 10000 dim. vector whose ith coordinate is the
    frequency is the ith word.
    """

    @staticmethod
    def buildTopWords(filename = "google-10000-english.txt", num_freq_words = 10000):
        """
        Builds a list ot the top X English words.
        """
        numWords = 1
        topWords = []
        with open(filename, 'r') as f:
            for line in f:
                if numWords > num_freq_words:
                    break
                line = line.strip()
                topWords.append(line)
                numWords += 1
        return topWords

    def embedComment(self, text, filename = "google-10000-english.txt", num_freq_words = 10000):
        """
        Implements the bag-of-words embedding.
        """
        comment = self.tokenize(text)
        top_words = self.buildTopWords(filename, num_freq_words)
        bag = [0] * num_freq_words
        for word in comment:
            if word in top_words:
                bag[top_words.index(word)] += 1
        return bag

def test():
    """
    Some quick code which tests the classes.
    """
    # Make a new AvgCommentEmbedder.
    averager = AvgCommentEmbedder()
    averager.embedComment("the dog went to the park")
    bow = BoWCommentEmbedder()
    assert()
    test_bow = np.zeros(10000)
    test_bow[0] = 1
    assert(np.all(np.equal(bow.embedComment("the"), test_bow)))

if __name__ == '__main__':
    test()