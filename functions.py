import json
import csv
import os.path

def check_file(filename):
	"""Check existence of file"""
	if os.path.isfile(filename):
		return True
	else:
		return False

def parse(input_file, output_file):
	"""Parsing csv to json"""
	input_file = csv.DictReader(open(input_file))

	i = 0
	array = {}
	for line in input_file:
		name = "object_" + str(i)
		array[name] = line
		i += 1

	with open(output_file, 'w') as f_obj:
		f_obj.write(json.dumps(array, indent=4, sort_keys=False, ensure_ascii=False))

def dump(array, filename):
	"""Dumps data to json"""
	with open(filename, 'w') as f_obj:
		f_obj.write(json.dumps(array, indent=4, sort_keys=False, ensure_ascii=False))	

def load(input_file):
	"""Loading array of objects"""
	with open(input_file) as f_obj:
		data = json.load(f_obj)
		return data