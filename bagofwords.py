from abstract import CommentEmbedder

import numpy as np

class BoWCommentEmbedder(CommentEmbedder):
    """
    Given a word embedding, implements the bag of words comment embedding,
    turning a comment into a 10000 dim. vector whose ith coordinate is the
    frequency is the ith word.
    """

    @staticmethod
    def buildTopWords(filename = "google-10000-english.txt", num_freq_words = 10000):
        """
        Builds a list of the top X English words.
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
	bow = BoWCommentEmbedder()
	test_bow = np.zeros(10000)
	test_bow[0] = 1
	assert(np.all(np.equal(bow.embedComment("the"), test_bow)))
	print "Done testing!"

if __name__ == '__main__':
	test()