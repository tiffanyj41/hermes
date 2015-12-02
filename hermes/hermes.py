"""Helper functions to hermesctl.py"""

import json
import os
from pyspark.sql.types import StructType

import hermes_ui
import metrics.performance_metrics 
import modules.datum 
import modules.timer 

# TODO: empty certain items in cargo after no longer needed? 
# TODO: when to use error_state? do try-catch for all states?

def start_state(cargo):
	"""Start of the state machine. Create HDFS directory and upload the input data.
	Returns: json_to_rdd_state as next state
	"""

	if cargo.verbose: cargo.logger.debug("In start_state:")

	if (len(cargo.json_paths) != len(cargo.schema_paths)) and (len(cargos.schema_paths) > 0):
		cargo.error_msg = "Each JSON file does not have its respective schema file."
		newState = error_state
		return newstate, cargo

	if cargo.verbose: cargo.logger.debug("Creating the hdfs directory " + cargo.hdfs_dir)
	os.system("hdfs dfs -mkdir " + cargo.hdfs_dir)

	for i in range(0, len(cargo.json_paths)):
		json_path = cargo.json_paths[i]
		if cargo.verbose: cargo.logger.debug("Loading JSON file " + json_path + " into hdfs directory " + cargo.hdfs_dir)
		os.system("hdfs dfs -put " + json_path + " " + cargo.hdfs_dir + "/" + os.path.basename(json_path))

	newState = json_to_rdd_state
	if cargo.verbose: cargo.logger.debug("start_state -> json_to_rdd_state")

	return newState, cargo

def json_to_rdd_state(cargo):
	"""Parse JSON to RDD. 
	Returns: split_data_state as next state
	"""

	if cargo.verbose: cargo.logger.debug("In json_to_rdd_state:")

	num_json_files = len(cargo.json_paths)
	num_schema_files = len(cargo.schema_paths)

	# load schema files
	schemas = []
	for i in range(0, num_schema_files):
		schema_path = cargo.schema_paths[i]
		if not schema_path:
			# no schema for its respective json file
			schemas.append(None)
		else:
			if cargo.verbose: cargo.logger.debug("Loading schema file %s" % schema_path)
			with open(schema_path, "r") as schema_file:
				schema = StructType.fromJson(json.load(schema_file))
				schemas.append(schema)

	# create RDD for each JSON file and store it in a Datum object
	datums = []
	for i in range(0, num_json_files):
		json_path = cargo.json_paths[i]
		schema_path = cargo.schema_paths[i]
		try:
			schema = schemas[i]
		except IndexError:
			schema = None

		if cargo.verbose: cargo.logger.debug("Creating dataframe based on the content of the json file %s" % json_path)
		dataframe = cargo.scsingleton.sqlCtx.read.json("hdfs://" + cargo.fs_default_ip_addr + "/" + cargo.hdfs_dir + "/" + os.path.basename(json_path), schema=schema)
		# explicitly repartition RDD after loading so that more tasks can run on it in parallel
    	# by default, defaultMinPartitions == defaultParallelism == estimated # of cores across all of the machines in your cluster
		dataframe = dataframe.repartition(cargo.scsingleton.sc.defaultParallelism * 3)

		if schema is None:
			schema = dataframe.schema

		rdd_format = hermes_ui._ask_user_for_rdd_format(schema_path, schema.names)

		if cargo.verbose: cargo.logger.debug("Creating RDD based on the format given by the user for json file %s" % json_path)
		rdd = dataframe.map(lambda row: tuple(row[i] for i in rdd_format)).cache()
		
		if cargo.verbose: cargo.logger.debug("Storing RDD in Datum object for json file %s" % json_path)
		datum = modules.datum.Datum(json_path, rdd)
		datums.append(datum)
	
	cargo.datums = datums

	newState = split_data_state
	if cargo.verbose: cargo.logger.debug("json_to_rdd_state -> split_data_state")

	return newState, cargo

def split_data_state(cargo):
	"""Split data to train, test, and (optional) validate.
	Returns: next state dependent whether or not it is using collaborative filtering or content based
	"""

	if cargo.verbose: cargo.logger.debug("In split_data_state:")

	for i in range(0, len(cargo.datums)):
		datum = cargo.datums[i]
		weights, seed = hermes_ui._ask_user_for_split_percentage(datum.json_path)
		datum.split_data(weights, seed)

	newState = develop_model_state
	if cargo.verbose: cargo.logger.debug("split_data_state -> develop_model_state")

	return newState, cargo

def develop_model_state(cargo):
	"""Develop model based on the train data. This model will be used to predict test data.
	Returns: calculate_metrics_state as next state
	"""

	if cargo.verbose: cargo.logger.debug("In develop_model_state:")	

	for i in range(0, len(cargo.datums)):
		datum = cargo.datums[i]
		with modules.timer.Timer() as t:
			# TODO: build model, please do not hardcode what to use for model
			from pyspark.mllib.recommendation import ALS
			cargo.model = ALS.train(datum.trainingRdd, rank=3)
		if cargo.verbose: cargo.logger.debug("Building model takes %s seconds" % t.secs)


	newState = calculate_metrics_state
	if cargo.verbose: cargo.logger.debug("develop_model_state -> calculate_metrics_state")

	return newState, cargo

def calculate_metrics_state(cargo):
	"""Test the metrics specified by the user. This is an end state.
	Returns: None because this is the last state.
	"""

	if cargo.verbose: cargo.logger.debug("In calculate_metrics_state:")	

	for i in range(0, len(cargo.datums)):
		datum = cargo.datums[i]
		with modules.timer.Timer() as t:
			# TODO: make a prediction, please do not hardcode what to do here
			testPredRDD = cargo.model.predictAll( datum.testRdd.map( lambda x: (x[0], x[1]) ) ).cache()
		if cargo.verbose: cargo.logger.debug("Making prediction takes %s seconds" % t.secs)
		with modules.timer.Timer() as t:
			# TODO: calculate metric, please do not hardcode what to use for metric
			testRmse = metrics.performance_metrics.calculate_rmse_using_rdd(datum.testRdd, testPredRDD)
		if cargo.verbose: cargo.logger.debug("Calculating metric takes %s seconds" % t.secs)
    	print "testRmse", testRmse

	if cargo.verbose: cargo.logger.debug("calculate_metrics_state -> end_state")

	return

def error_state(cargo):
	"""Error state. Print out the error messages. This is an end state.
	Returns: None because this is the last state.
	"""
	if cargo.verbose: cargo.logger.debug("In error_state:")
	cargo.logger.error("ERROR: " + cargo.error_msg)
	if cargo.verbose: cargo.logger.debug("error_state -> end_state")
	return

