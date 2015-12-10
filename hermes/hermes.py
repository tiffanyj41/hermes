"""Helper functions to hermesctl.py"""

import json
import logging
import os

import hermesui
import metrics.performance_metrics 
import modules.datum 
import modules.metricgenerator as metricgenerator
import modules.recommendergenerator as recommendergenerator
import modules.timer 
import modules.vectorgenerator as vectorgenerator

# TODO: empty certain items in cargo after no longer needed? 
# TODO: when to use error_state? do try-catch for all states?

# get logger
logger = logging.getLogger("hermes")

def start_state(cargo):
	"""Start of the state machine. Create HDFS directory and upload the input data.
	Returns: json_to_rdd_state as next state
	"""

	if cargo.verbose: logger.debug("In start_state:")

	if cargo.verbose: logger.debug("Creating the hdfs directory " + cargo.hdfs_dir)
	os.system("hdfs dfs -mkdir " + cargo.hdfs_dir)

	def load_json_files(datas):
		for i in range(0, len(datas)):
			json_path = datas[i].datapath
			if cargo.verbose: logger.debug("Loading JSON file " + json_path + " into hdfs directory " + cargo.hdfs_dir)
			os.system("hdfs dfs -put " + json_path + " " + cargo.hdfs_dir + "/" + os.path.basename(json_path))

	load_json_files(cargo.datas)

	newState = json_to_rdd_state
	if cargo.verbose: logger.debug("start_state -> json_to_rdd_state")

	return newState, cargo

def json_to_rdd_state(cargo):
	"""Parse JSON to RDD. 
	Returns: split_data_state as next state
	"""

	if cargo.verbose: logger.debug("In json_to_rdd_state:")

	# create RDD for each JSON file and store it in Cargo's vectors list
	for i in range(0, len(cargo.datas)):
		data = cargo.datas[i]
		if cargo.verbose: logger.debug("Working with json file %s" % data.datapath)

		if cargo.verbose: logger.debug("Creating dataframe based on the content of the json file")
		datapath_in_hdfs = "hdfs://" + cargo.fs_default_ip_addr + "/" + cargo.hdfs_dir + "/" + os.path.basename(data.datapath)
		data.set_dataframe(cargo.scsingleton, datapath_in_hdfs)

		if cargo.verbose: logger.debug("Creating RDD based on the computed dataframe and configuration provided by the user")
		cargo.vectors.append( vectorgenerator.VectorFactory().create_obj_vector(cargo.scsingleton.sqlCtx, data, cargo.support_files) ) 


	# TODO: clean cargo?
	# cargo.datas = []
	# cargo.hdfs_dir = None
	# cargo.fs_default_ip_addr = None

	newState = split_data_state
	if cargo.verbose: logger.debug("json_to_rdd_state -> split_data_state")

	return newState, cargo

def split_data_state(cargo):
	"""Split data to train, test, and (optional) validate.
	Returns: next state dependent whether or not it is using collaborative filtering or content based
	"""

	if cargo.verbose: logger.debug("In split_data_state:")

	for i in range(0, len(cargo.vectors)):
		vector = cargo.vectors[i]
		weights, seed = hermesui._ask_user_for_split_percentage(vector.data.datapath)
		vector.split_data(weights, seed)

	newState = make_prediction_state
	if cargo.verbose: logger.debug("split_data_state -> make_prediction_state")

	return newState, cargo

def make_prediction_state(cargo):
	"""Develop model based on the train data and make prediction based on this model. 
	Returns: calculate_metrics_state as next state
	"""

	if cargo.verbose: logger.debug("In make_prediction_state:")	

	for i in range(0, len(cargo.vectors)):
		for r in cargo.recommenders:
			# TODO: implement other implementations, ie. WithTfidf(), etc.
			# default is WithoutTfidf()
			recommender = recommendergenerator.RecommenderFactory().create_obj_recommender(r, cargo.vectors[i])
			# recommender = RecommenderFactory().create_obj_recommender(r, vector, WithTfidf())
			# recommender = RecommenderFactory().create_obj_recommender(r, vector, WithoutTfidf())
			# etc.
			with modules.timer.Timer() as t:
				cargo.vectors[i].prediction_vector = recommender.make_prediction()
			if cargo.verbose: logger.debug("Making prediction takes %s seconds" % t.secs)

	newState = calculate_metrics_state
	if cargo.verbose: logger.debug("make_prediction_state -> calculate_metrics_state")

	return newState, cargo

def calculate_metrics_state(cargo):
	"""Test the metrics specified by the user. This is an end state.
	Returns: None because this is the last state.
	"""

	if cargo.verbose: logger.debug("In calculate_metrics_state:")

	# create a metric executor
	executor = metricgenerator.MetricExecutor(metricgenerator.Metric())

	# TODO: figure out why logger prints INFO twice
	for i in range(0, len(cargo.vectors)):
		logger.info("-" * 80)
		logger.info("Data: %s" % cargo.vectors[i].data.datapath)
		for m in cargo.metrics:
			# check if metric exists
			metric = metricgenerator.MetricFactory().create_obj_metric(m)
			# set metric in executor
			executor.change_metric(metric)
			# execute the metric
			with modules.timer.Timer() as t:
				logger.info("Metric: %s = %f" % (m, executor.execute(cargo.vectors[i])))
			if cargo.verbose: logger.debug("Calculating metric takes %s seconds" % t.secs)
		logger.info("-" * 80)
	if cargo.verbose: logger.debug("calculate_metrics_state -> end_state")

	return

def error_state(cargo):
	"""Error state. Print out the error messages. This is an end state.
	Returns: None because this is the last state.
	"""
	if cargo.verbose: logger.debug("In error_state:")
	logger.error("ERROR: " + cargo.error_msg)
	if cargo.verbose: logger.debug("error_state -> end_state")
	return

