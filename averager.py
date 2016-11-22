from abstract import CommentEmbedder
import numpy as np
import gensim
import json

class AvgCommentEmbedder(CommentEmbedder):
    """
    Given a word embedding, implements the comment embedding by averaging
    the embeddings of each word in a word embedding. We're using the word2vec
    embedding trained on the GoogleNews corpus.
    """
    def __init__(self,  filename = './GoogleNews-vectors-negative300.bin', binary = True):
        self.loadEmbedding(filename = filename, binary = binary)

    def loadEmbedding(self, filename = './GoogleNews-vectors-negative300.bin', binary = True):
        self.model = gensim.models.Word2Vec.load_word2vec_format(filename, binary = binary)

    def embedComment(self, text):
        """
        Embeds the comment by averaging the word embedding for each word in
        the embedding.
        """
        comment = self.tokenize(text)
        valid_words= []
        for word in comment:
            if word in self.model:
                valid_words.append(self.model[word])
        if  valid_words != []:
            embedding = np.mean(valid_words, axis = 0)
        else:
            embedding = np.zeros(300)
        return embedding

def test(max_count = 100):
    """
    Some quick code which tests the classes.
    """
    # Make a new AvgCommentEmbedder.
    #averager = AvgCommentEmbedder()
    #averager.loadEmbedding()
    #vec1 = averager.embedComment("cat dog")
    #vec2 = averager.embedComment("pizza burger")
    #vec3 = averager.embedComment("cat")
    #assert((np.linalg.norm(vec1 - vec3)) < (np.linalg.norm(vec2 - vec3)))
    count = 0
    averager = AvgCommentEmbedder()
    with open('./jokesSortedDownNoDelete.json') as f:
        for line in f:
            #print "Joke number", count
            # if count > max_count:
            #     break
            joke_obj = json.loads(line.strip())
            try:
                joke = joke_obj[u'title'] + joke_obj[u'selftext']
            except UnicodeEncodeError:
                continue
            try:
                joke_vec = averager.embedComment(joke)
            except IndexError:
                print joke
                print "Index Error"
                break
            if any(np.isinf(x) for x in joke_vec):
                print joke
            count += 1
    #print "Done testing!"

if __name__ == '__main__':
    test()