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
		response = getJokeAv(comment, EMBEDDED_JOKES, JOKES_RAW, NUM_JOKES, avg)
		# if similarity(comment, response) > threshold:
		# updateThreshold()
		repliedTo.append(str(submission.id) + ": " + comment)
		print response
		try:
			top_level_comment.reply(commentLead+response)
		except:
			time.sleep(60)
		time.sleep(60)

with open("repliedTo.txt", "w") as f:
	for line in repliedTo:
		f.write(line)

		
"""
The main idea here is to learn a good "relevance threshold" that results in
our bot not posting irrelevant jokes, but also not posting too few jokes.

It does this by gradually decreasing the threshold and increasing it
every time a post gets a negative reaction.
"""

threshold = 1.0 # Start with impossibly high threshold.
slope = 0.25 # The speed at which we decrease the threshold.

def updateThreshold(negativeFeedback):
	"""
	Updates the value of the relevance threshold. Takes in "negativeFeedback",
	a boolean indicating whether or not there has been negative feedback on
	posts since the last time updateThreshold was called.
	This should probably be called every time a new joke is going to be posted.
	"""
	if negativeFeedback:
		# If we got downvoted, bump our threshold up and decrease our slope.
		threshold += slope * 2 # Arbitrary choice for negative feedback bump.
		slope /= 1.5 # Arbitrary choice for deceleration.
        
	else:
		threshold -= slope
