import praw
import os
from recommend import *
from botConfig import *
from averager import AvgCommentEmbedder
from praw.models import MoreComments
import time

if not os.path.isfile("botConfig.py"):
	print "You must create a config file with REDDIT_USERNAME, REDDIT_PASS, jokesfile (JOKES_RAW), embedding file (EMBEDDED_JOKES), & numjokes (NUM_JOKES)"
	exit(1)

avg = AvgCommentEmbedder()
user_agent = ("Joke Recommender 1.0")
commentLead = ("Here is an (hopefully) applicable joke to your comment:  \n")
r = praw.Reddit(user_agent=user_agent, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, username=REDDIT_USERNAME, password=REDDIT_PASS)

if not os.path.isfile("repliedTo.txt"):
	repliedTo = []
else:
	repliedTo = []
	with open("repliedTo.txt", "r") as f:
		for line in f:
			repliedTo.append(line)

submissions = r.front.hot(limit=5)
maxComments = 2
maxPosts = 10
currPosts = 0
currComments = 0
for submission in submissions:
	if currPosts > maxPosts:
		break
	currPosts += 1
	for top_level_comment in submission.comments.list():
		if currComments > maxComments:
			break
		currComments += 1
		if isinstance(top_level_comment, MoreComments):
			continue
		comment = top_level_comment.body.lower()
		if str(submission.id) + ": "+ comment in repliedTo:
			continue
		print comment
		repliedTo.append(str(submission.id) + ": " + comment)
		response = getJokeAv(comment, EMBEDDED_JOKES, JOKES_RAW, NUM_JOKES, avg)
		print response
		try:
			top_level_comment.reply(commentLead+response)
		except:
			time.sleep(60)
		time.sleep(60)

with open("repliedTo.txt", "w") as f:
	for line in repliedTo:
		f.write(line)