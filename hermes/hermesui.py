def _ask_user_for_rdd_format(schema_path, schema_names):
	"""Ask user for the desired RDD format.
	Args:
		schema_path: the path to the schema file
		schema_names: 
	Returns: List of schema_name's id.
	"""
	print "How do you want your data to be parsed?"
	print "For example: Given the following options"
	print "(0) movie_id"
	print "(1) rating"
	print "(2) timestamp"
	print "(3) user_id"
	print "if you wanted the data to be parsed in the format of [(user_id, movie_id, rating)],"
	print "please type in: 3 0 1\n"

	def _check_schema_ids(schema_ids, num_schema_ids):

		# check if each schema_name_id is in the range of num_schema_ids
		for schema_name_id in schema_name_ids:
			if schema_name_id not in range(0, num_schema_ids):
				print "Option provided is not in range."
				return False

		# check that there are no duplicates
		if len(schema_name_ids) != len(set(schema_name_ids)):
			print "There are duplicates. Please provide no duplicates."
			return False

		return True 


	print "For the following given schema %s" % (schema_path)
	print "how do you want your data to be parsed? "
	for i in range(0, len(schema_names)):
		print "(%s) %s" % (i, schema_names[i])

	while True:
		user_input = raw_input("Enter the numbers separated by blank space: ")
		try:
			schema_name_ids = [int(schema_name_id.strip()) for schema_name_id in user_input.split(" ")]
			if _check_schema_ids(schema_name_ids, len(schema_names)):
				break
		except ValueError:
			print "Please provide a valid number."
		
	return schema_name_ids

def _ask_user_for_split_percentage(datum_json_path):
	"""Ask user what percentage to split the data into training, test, and validation.
	Args:
		datum_json_path: the path to the data JSON file
	Returns: Tuple of percentage of training, test, and validation respectively in float notation.
	         (trainingPercentage, testPercentage, validationPercentage), seed
	"""
	print "How do you want to split your data?"
	print "For example: If you wanted to split the data into "
	print "60% training, 40% test, 0% validation, seed = 11, please type in:"
	print "Percentage for training: 60"
	print "Percentage for test: 40"
	print "Percentage for validation: 0"
	print "Seed: 11\n"


	def _check_percentage(percentage):
		"""Check if the percentage is valid.
		"""
		if percentage in range(0, 100):
			return True
		else:
			return False

	def _check_sum_percentage(a, b, c):
		"""Check if the sum of the given percentages is equal to 100.
		"""
		sum_percentage = a + b + c
		if sum_percentage == 100:
			return True
		else:
			return False

	print "For the following given data %s" % (datum_json_path)
	print "how do you want to split your data?"
	while True:
		while True:
			try:
				trainingPercentage = int(raw_input("Percentage for training: ").strip())
			except ValueError:
				print "Please provide a valid number."
			else:
				if _check_percentage(trainingPercentage):
					break
				else:
					print "Please provide a number from 0 - 100."
		while True:
			try:
				testPercentage = int(raw_input("Percentage for test: ").strip())
			except ValueError:
				print "Please provide a valid number."
			else:
				if _check_percentage(testPercentage):
					break
				else:
					print "Please provide a number from 0 - 100."
		while True:
			try:
				validationPercentage = int(raw_input("Percentage for validation: ").strip())
			except ValueError:
				print "Please provide a valid number."
			else:
				if _check_percentage(validationPercentage):
					break
				else:
					print "Please provide a number from 0 - 100."
		if _check_sum_percentage(trainingPercentage, testPercentage, validationPercentage):
			break
		else:
			print "Sum of percentages does not equal to 100. Please re-input the percentages."

	while True:
		try:
			seed = int(raw_input("Seed: ").strip())
			break
		except ValueError:
			print "Please provide a valid number."

	# convert it to a percentage from 0 - 1
	trainingPercentage = trainingPercentage/100.
	testPercentage = testPercentage/100.
	validationPercentage = validationPercentage/100.

	return [trainingPercentage, testPercentage, validationPercentage], seed



