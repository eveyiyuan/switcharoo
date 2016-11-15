import json
import string
import sys, getopt

def pruneData(source, dest):
	''' Input: source - a JSON file of reddit submissions following pushshift's submission formulation
		Output: dest - a JSON file of only reddit submissions in joke subreddits that are not 18+
	'''
	fDest = open(dest+".json", 'a')
	with open(source, 'r') as f:
		for line in f:
			commentObj = json.loads(line)
			try:
				subreddit = commentObj[u'subreddit']
				isNSFW = commentObj[u'over_18']
				isSelf = commentObj[u'is_self']
				joke = commentObj[u'selftext']
			except KeyError:
				continue
			try:
				joke = str(joke)
			except UnicodeEncodeError:
				continue
			subreddit = str(subreddit).lower()
			if "jokes" in subreddit and isNSFW == False:
				fDest.write(line)

	fDest.close()

def sortByScore(source, dest):
	''' Input: source - a JSON file of reddit submissions
		Output: dest - Reddit submissions from source sorted by score decreasing
	'''
	fDest = open(dest+".json", 'a')
	submissions = []
	with open(source, 'r') as f:
		for line in f:
			commentObj = json.loads(line)
			submissions.append(commentObj)


	submissions = sorted(submissions, key=lambda comment: comment[u'score'], reverse=True)
	for s in submissions:
		fDest.write(json.dumps(s))
		fDest.write("\n")
	fDest.close()

def main(argv):
	source = ''
	dest = ''
	sort = ''
	try:
		opts, args = getopt.getopt(argv,"i:o:s:")
	except getopt.GetoptError:
		print 'Usage: pruneDataJokes.py -i <input file> -o <output file name (no extension)> -s <sort, 1 for yes, 0 for no>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-i":
			source = arg
		elif opt == "-o":
			dest = arg
		elif opt == "-s":
			sort = arg
	if sort == '0':
		pruneData(source,dest)
	else:
		sortByScore(source, dest)

if __name__ == "__main__":
	main(sys.argv[1:])