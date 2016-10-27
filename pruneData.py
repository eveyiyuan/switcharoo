import pandas as pd
import sys, getopt
import numpy as np
import json

def processData(source, dest):
	with open(source, 'r') as f:
		data = f.readlines()
	data = map(lambda x: x.rstrip(), data)
	data_json_str = "[" + ','.join(data) + "]"
	data_df = pd.read_json(data_json_str)
	query = data_df[data_df.body.str.contains("[Tt]he ol['ed] [Rr]eddit [a-zA-Z ]+-?[AEae]-?roo+")]
	queryD = query.to_dict('records')
	queryD = [json.dumps(record)+"\n" for record in queryD]
	with open(dest, 'a') as d:
		d.writelines(queryD)

def main(argv):
	source = ''
	dest = ''
	try:
		opts, args = getopt.getopt(argv,"i:o:")
	except getopt.GetoptError:
		print 'Usage: pruneData.py -i <input file> -o <output file>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == "-i":
			source = arg
		elif opt == "-o":
			dest = arg
	processData(source, dest)

if __name__ == "__main__":
	main(sys.argv[1:])

