"""Create json_paths.txt and schema_paths.txt that you can pass in to hermes.
Outputs: 
	1. json_paths.txt: lists all path to JSON files used in hermes
	2. schema_paths.txt: lists all path to schema files used in hermes
"""

import os
from distutils.util import strtobool

def file_accessible(filepath, mode):
	"""Check if a file exists and is accessible."""
	try:
		f = open(filepath, mode)
		f.close()
	except IOError as e:
		return False

	return True

def parse_yn(answer):
	answer.upper().strip()

def main():

	# create output directory if it did not exist
	output_dir = os.path.dirname(os.path.realpath(__file__)) + "/output"
	if not os.path.exists(output_dir):
		os.makedirs(output_dir)

	# ask user for path to JSON file and its respective schema file
	i = 0
	json_paths = []
	schema_paths = []
	is_last = False
	while True:
		while True:
			json_path = raw_input("(" + str(i) + ") Enter path to a JSON file: ")
			if file_accessible(json_path.strip(), "r"):
				json_paths.append(json_path)
				break
			else:
				print "Please input a JSON file that exists or is accessible."
		while True:
			schema_path = raw_input("(" + str(i) + ") Enter path to its respective schema file (or empty string if there is no schema): ")
			if file_accessible(schema_path.strip(), "r"):
				schema_paths.append(schema_path)
				break
			elif schema_path.strip() == "":
				schema_paths.append("")
				break
			else:
				print "Please input a schema file that exists or is accessible."
		while True:
			add_more = raw_input("Do you need to add more JSON file? [Y/N] ")
			try:
				if bool(strtobool(add_more.upper().strip())):
					i = i + 1
				else:
					is_last = True
				break
			except ValueError:
				print "Please respond with a Y or N."
		if is_last:
			break

	# create a file with a list of JSON file paths
	json_file = output_dir + "/json_paths.txt"
	with open(json_file, "w") as f:
		for json_path in json_paths:
			f.write(json_path + "\n")

	# create a file with a list of schema file paths
	schema_file = output_dir + "/schema_paths.txt"
	with open(schema_file, "w") as f:
		for schema_path in schema_paths:
			f.write(schema_path + "\n")

	return

if __name__ == "__main__":
	main()
