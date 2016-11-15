# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 09:05:33 2016

@author: giraffe
"""

import string

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
