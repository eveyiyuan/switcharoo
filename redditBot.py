import praw
import os
from recommend import *
from botConfig import *
from averager import AvgCommentEmbedder
from praw.models import MoreComments
import time
from thresholds import *
from datetime import datetime

commentLead = ("  \n*****  \nHi I am a bot! Here is an (hopefully) applicable joke to your comment. [About](http://matt.morgan.team/joke-recommender-reddit-bot.html)")
doNotPost = ["aww", "diy", "twoxchromosomes", "writingprompts", "futurology", "science"]

def init():
	if not os.path.isfile("botConfig.py"):
		print "You must create a config file with REDDIT_USERNAME, REDDIT_PASS, jokesfile (JOKES_RAW), embedding file (EMBEDDED_JOKES), & numjokes (NUM_JOKES)"
		exit(1)

	avg = AvgCommentEmbedder()
	user_agent = ("Joke Recommender 1.0")

	r = praw.Reddit(user_agent=user_agent, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, username=REDDIT_USERNAME, password=REDDIT_PASS)

	if not os.path.isfile("repliedTo.txt"):
		repliedTo = []
	else:
		repliedTo = []
		with open("repliedTo.txt", "r") as f:
			for line in f:
				repliedTo.append(line.strip())

	if not os.path.isfile("simDistances.txt"):
		dists = {}
	else:
		dists = {}
		with open("simDistances.txt", "r") as f:
			for line in f:
				vals = line.split()
				dists[vals[0]] = float(vals[1])

	if not os.path.isfile("thresholds.txt"):
		thresholds = []
	else:
		thresholds = []
		with open("thresholds.txt", "r") as f:
			for line in f:
				thresholds.append(float(line.strip()))

	mainLoop(r, dists, repliedTo, avg, thresholds)

def mainLoop(r, dists, repliedTo, avg, thresholds):
	submissions = list(r.front.hot(limit=50))
	numPosts = 0
	threshold = update(r, dists)
	try:
		while len(submissions) != 0:
			submission = submissions.pop()
			print datetime.now()
			if submission.subreddit.display_name.lower() in doNotPost:
				continue

			for top_level_comment in submission.comments.list():

				if isinstance(top_level_comment, MoreComments):
					continue
				comment = top_level_comment.body.lower()
				if str(submission.id) in repliedTo:
					continue
				print comment

				if numPosts % 6 == 0:
					threshold = update(r, dists)
					recordData(repliedTo, thresholds, dists)
				
				response, dist = getJokeAv(comment, EMBEDDED_JOKES, JOKES_RAW, NUM_JOKES, avg)
				if dist < threshold:
					print response
					try:
						top_level_comment.reply(response+commentLead)
						repliedTo.append(str(submission.id))
						dists[top_level_comment.id] = dist
						threshold = max(threshold - 0.1, 0.0)
					except Exception, e:
						#submissions.insert(0, submission)
						print e
						print "Failed to post :("
				else:
					submissions.insert(0, submission)

				thresholds.append(threshold)
				numPosts += 1
				time.sleep(600)
				break

	except KeyboardInterrupt:
		recordData(repliedTo, thresholds, dists)
		exit(1)

	recordData(repliedTo, thresholds, dists)

def recordData(repliedTo, thresholds, dists):
	with open("repliedTo.txt", "w") as f:
		for line in repliedTo:
			f.write(line + "\n")

	with open("simDistances.txt", "w") as f:
		for k in dists.keys():
			f.write(k + " " + str(dists[k]) + "\n")

	with open("thresholds.txt", "w") as f:
		for t in thresholds:
			f.write(str(t) + "\n")
		
def update(reddit, dists):
	karma =  []
	distVals = []
	for c in reddit.user.me().comments.new(limit=100):
		try:
			val = dists[c.id]
			karma.append(c.score)
			distVals.append(val)
		except:
			continue

	return getThreshold(distVals, karma)

def main():
	init()

if __name__ == "__main__":
	main()
