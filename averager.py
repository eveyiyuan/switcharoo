from abstract import CommentEmbedder
import numpy as np
import gensim

class AvgCommentEmbedder(CommentEmbedder):
    """
    Given a word embedding, implements the comment embedding by averaging
    the embeddings of each word in a word embedding. We're using the word2vec
    embedding trained on the GoogleNews corpus.
    """
    def __init__(self,  filename = 'GoogleNews-vectors-negative300.bin', binary = True):
        self.loadEmbedding(filename = filename, binary = binary)

    def loadEmbedding(self, filename = 'GoogleNews-vectors-negative300.bin', binary = True):
        self.model = gensim.models.Word2Vec.load_word2vec_format(filename, binary = binary)

    def embedComment(self, text):
        """
        Embeds the comment by averaging the word embedding for each word in
        the embedding.
        """
        comment = self.tokenize(text)
        embedding = self.model[comment[0]]
        deleted = 0
        for i in range(1, len(comment)):
            try:
                embedding += self.model[comment[i]]
            except KeyError:
                deleted += 1
                continue
        try:
            embedding = embedding / (len(comment) - deleted)
        except ValueError:
            print "Cannot embed this vector rip"
        return embedding


def test():
    """
    Some quick code which tests the classes.
    """
    # Make a new AvgCommentEmbedder.
    averager = AvgCommentEmbedder()
    #averager.loadEmbedding()
    vec1 = averager.embedComment("cat dog")
    vec2 = averager.embedComment("pizza burger")
    vec3 = averager.embedComment("cat")
    assert((np.linalg.norm(vec1 - vec3)) < (np.linalg.norm(vec2 - vec3)))

if __name__ == '__main__':
    test()