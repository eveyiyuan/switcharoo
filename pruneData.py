import pandas as pd
import sys, getopt
import numpy as np
import json
import re

def processData(source, dest):
	fDest = open(dest+".json", 'a')
	fPID = open(dest+"_pid.json", 'a')
	with open(source, 'r') as f:
		for line in f:
			commentObj = json.loads(line)
			comment = commentObj[u'body']
			try:
				comment = str(comment)
			except UnicodeEncodeError:
				continue
			p = re.compile("[Tt]he ol['ed] [Rr]eddit [a-zA-Z ]+-?[AEae]-?roo+")
			if len(p.findall(comment)) != 0:
				fDest.write(line)
				fPID.write(commentObj[u'parent_id']+"\n")
	fDest.close()

	# 	data = f.readlines()
	# data = map(lambda x: x.rstrip(), data)
	# data_json_str = "[" + ','.join(data) + "]"
	# data_df = pd.read_json(data_json_str)
	# query = data_df[data_df.body.str.contains("[Tt]he ol['ed] [Rr]eddit [a-zA-Z ]+-?[AEae]-?roo+")]
	# queryD = query.to_dict('records')
	# queryD = [json.dumps(record)+"\n" for record in queryD]
	# with open(dest+".json", 'a') as d:
	# 	d.writelines(queryD)
	# queryIDs = query["parent_id"]
	# with open(dest+"_parentIDs.csv", 'a') as d2:
	# 	queryIDs.to_csv(d2, header=False, index=False)

def processDataFromChild(idsPath, source, dest):
	print idsPath
	with open(idsPath, 'r') as f:
		ids = [l.rstrip() for l in f]

	with open(source, 'r') as f2:
		data = f2.readlines()
	data = map(lambda x: x.rstrip(), data)
	data_json_str = "[" + ','.join(data) + "]"
	data_df = pd.read_json(data_json_str)
	query = data_df[data_df.name.isin(ids)]
	queryD = query.to_dict('records')
	queryD = [json.dumps(record)+"\n" for record in queryD]
	with open(dest+".json", 'a') as d:
		d.writelines(queryD)

def main(argv):
	source = ''
	dest = ''
	t = ''
	idsPath = ''
	try:
		opts, args = getopt.getopt(argv,"i:o:t:d::")
	except getopt.GetoptError:
		print 'Usage: pruneData.py -i <input file> -o <output file name (no extension)> -t <type, 0 for not parent search> -d <name of ids file>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-i":
			source = arg
		elif opt == "-o":
			dest = arg
		elif opt == "-t":
			t = arg
		elif opt == "-d":
			idsPath = arg
	if t == '0':
		processData(source, dest)
	else:
		processDataFromChild(idsPath, source, dest)

if __name__ == "__main__":
	main(sys.argv[1:])

