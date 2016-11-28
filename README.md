# Overview
The switcharoo repository contains the code for a joke-posting Reddit bot. (The name is due to historical accident.)

The bot looks for a comment to reply to, then embeds the comment into a fixed-dimensional space. It then searches through a database of jokes (constructed from /r/jokes posts) for the joke closest to the comment in the embedding space, and posts it.

# Joke Recommender

Note, please include "google-10000-english.txt" from [here](https://github.com/first20hours/google-10000-english) in this directory.

# Dependencies
gensim word2vec python library [here](https://radimrehurek.com/gensim)

