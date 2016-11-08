# JSON blaster

import json

def parent(parent_filename, child_filename):
	'''
	For each comment in the JSON file child, links it with its parent comment
	in the JSON file parent, and returns a list of nested JSON objects of the
	form

	{ parent : {JSON object holding information about the parents}
	  child  : {JSON object holding information about the child}
	}

	Returns it as a list of JSON objects. A separate function will write these
	into a file.
	'''
	parent_file = open(parent_filename, 'r')
	child_file = open(child_filename, 'r')
	parents = [] # A Python list of translated parent JSON objects.
	children = [] # A Python list of translated child JSON objects.
	combined = [] # A Python list of the combined JSON comments, as above.
	# Populate the parent list.
	for line in parent_file:
		temp = json.loads(line)
		parents.append(temp)
	# Populate the child list.
	for line in child_file:
		temp = json.loads(line)
		children.append(temp)
	for child in children:
		parent_id = child['parent_id']
		for parent in parents:
			if parent['name'] == parent_id:
				# Make a combined JSON object as described in the docstring.
				# In Python, this involves making a dict w/ 2 keys, and then
				# we can use the JSON library to translate them back into a
				# JSON object.
				new_json = dict()
				new_json['parent'] = parent
				new_json['child'] = child
				combined.append(new_json)
	parent_file.close()
	child_file.close()
	return combined

def writeJSON(filename, json_list):
	'''
	Takes a filename and a Python list of Python-translated JSON objects
	(becomes valid JSON after a call to json.dumps()) and (over)writes it
	with each line of the new file being a JSON object in the list.
	'''
	f = open(filename, 'w')
	for obj in json_list:
		f.write(json.dumps(obj) + '\n')
	f.close()


def main():
	children = 'P2CommentsALL.json'
	parents = 'P3CommentsALL.json'
	new_json = parent(parents, children)
	writeJSON('combined.json', new_json)

if __name__ == '__main__':
	main()


