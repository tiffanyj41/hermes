"""Script to run hermes via command line."""

import click
import ConfigParser
import itertools
import json
import logging
import sys
from pyspark import SparkConf

import hermes
import modules.config as Config
from modules.data import UserVectorData, ContentVectorData
from modules.cargo import Cargo
from modules.singleton import SCSingleton
from modules.statemachine import StateMachine


def add_states(stateMachine):
	""" json_to_rdd -> split_data - (Collaborative Filtering) -> develop_model -> calculate_metrics
	                              - (Content Based) -> ???
	"""
	stateMachine.add_state(hermes.start_state)
	stateMachine.add_state(hermes.json_to_rdd_state)
	stateMachine.add_state(hermes.split_data_state)
	stateMachine.add_state(hermes.make_prediction_state)
	stateMachine.add_state(hermes.calculate_metrics_state, isEndState=1)
	stateMachine.add_state(hermes.error_state, isEndState=1)
	stateMachine.set_start(hermes.start_state)
	return

def create_logger(name):
	logger = logging.getLogger(name)
	logger.setLevel(logging.DEBUG)
	# create hermes.log file that prints out debug messages
	fh = logging.FileHandler("hermes.log")
	fh.setLevel(logging.DEBUG)
	# create console handler for stderr that prints out error messages
	che = logging.StreamHandler()
	che.setLevel(logging.ERROR)
	# create console handler for stdout for info, debug, and error level
	choi = logging.StreamHandler(sys.stdout)
	choi.setLevel(logging.INFO)
	chod = logging.StreamHandler(sys.stdout)
	chod.setLevel(logging.DEBUG)
	choe = logging.StreamHandler(sys.stdout)
	choe.setLevel(logging.ERROR)
	# create formatter and add it to the handlers
	formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
	fh.setFormatter(formatter)
	che.setFormatter(formatter)
	choi.setFormatter(formatter)
	chod.setFormatter(formatter)
	choe.setFormatter(formatter)
	# add handlers to logger	
	logger.addHandler(fh)
	logger.addHandler(che)
	logger.addHandler(choi)
	logger.addHandler(chod)
	logger.addHandler(choe)
	return logger

def create_sparkcontext():
	conf = SparkConf().setAppName("hermes")
	return SCSingleton(conf)

def extract_configs(configs_path, list_of_files_config_path, cargo, logger):
	# TODO: is there a better way to implement this function?

	# extract list_of_files_config
	lofcp = ConfigParser.ConfigParser()
	lofcp.read(list_of_files_config_path)

	# helper functions for extracting configs
	def handle_recognized_section_item(section, item_key, item_value):
		if section == "datasets":
			datasets_items[item_key] = item_value
			return
		if section == "recommenders":
			if item_key == "recommenders":
				cargo.recommenders.extend( json.loads(item_value) )
			return
		if section == "metrics":
			if item_key == "metrics":
				cargo.metrics.extend( json.loads(item_value) )			

	def handle_unrecognized_section_item(section, item_key, item_value):
		if section == "datasets":
			# add support file
			cargo.support_files[item_key] = item_value
			return
		if section == "recommenders":
			logger.error("ERROR: skip unrecognized item " +  item_key + " under section [" + section + "] in config" + config_path)
			return
		if section == "metrics":
			logger.error("ERROR: skip unrecognized item " +  item_key + " under section [" + section + "] in config" + config_path)
			return

	def handle_dataset_section(dataset_items, config_path):
		# make sure vectorizer is initialized in order to verify the section in list_of_files_config
		# TODO: which is better? iterating through sections then items or iterating through just items of list_of_files_config?
		
		if not ("vectorizer" in datasets_items.keys()):
			logger.error("ERROR: config " + config_path + " must have vectorizer specified.")
			sys.exit()

		vectorizer = datasets_items["vectorizer"]
		lofmap = Config.map_section(lofcp, vectorizer)

		# create UserVectorData or ContentVectorData or both
		hasUserVector = False
		# check it has the required items to build a UserVectorData
		if set(Config.REQ_UV_HEADINGS) < set(datasets_items.keys()): 
			hasUserVector = True
			create_datas(lofmap, vectorizer, datasets_items, config_path, isUserVector=True)

		hasContentVector = False 
		# check it has the required items to build a ContentVectorData
		if set(Config.REQ_CV_HEADINGS) < set(datasets_items.keys()):
			hasContentVector = True
			create_datas(lofmap, vectorizer, datasets_items, config_path, isUserVector=False)

		if not hasUserVector and not hasContentVector:
			logger.error("ERROR: config " + config_path + " does not have declaration for a user vector or a content vector")
			sys.exit()	

	def create_datas(lofmap, vectorizer, datasets_items, config_path, isUserVector):
		"""
		user_vector_data = movielens_10m_ratings, bleh_ratings
		user_vector_schemas = movielens_10m_ratings_schema, bleh_schema
		user_vector_types = ratings, bleh

		"""

		if isUserVector:
			datapaths_heading = "user_vector_data"
			vector_types_heading = "user_vector_types"
			schemapaths_heading = "user_vector_schemas"
		else:
			datapaths_heading = "content_vector_data"
			vector_types_heading = "content_vector_types"
			schemapaths_heading = "content_vector_schemas"

		datapaths = json.loads(datasets_items[datapaths_heading])
		vector_types = json.loads(datasets_items[vector_types_heading])
		hasSchemas = False
		if "user_vector_schemas" in datasets_items.keys():
			schemapaths = json.loads(datasets_items[schemapaths_heading])
			hasSchemas = True

		# check that a vector type is specified for each data
		# TODO: multiple vector types for each data in the future?
		if len(datapaths) != len(vector_types):
			logger.error("ERROR: must specify a vector type for each data in config " + config_path)
			sys.exit()

		for i in range(0, len(datapaths)):
			# set datapath
			try:
				datapath = lofmap[datapaths[i]]
			except KeyError:
				logger.error("ERROR: cannot find data " + datapath + " in the list_of_files_config for config " + config_path)
				sys.exit()
    		# set vector_type
			vector_type = vector_types[i]
			# set schemapath
			try:
				if hasSchemas: schemapath = lofmap[schemapaths[i]]
			except IndexError, KeyError:
				schemapath = None

    		if isUserVector: 
    			uservectordata = UserVectorData(datapath, vector_type, schemapath, vectorizer)
    			cargo.datas.append(uservectordata)
    		else:
    			contentvectordata = ContentVectorData(datapath, vector_type, schemapath, vectorizer)
    			cargo.datas.append(contentvectordata)

	# extract configs
	for config_path in configs_path:
		cp = ConfigParser.ConfigParser()
		cp.read(config_path)
		datasets_items = {}
		# extract sections
		for section in cp.sections():
			if section in Config.HEADINGS.keys():
				# extract section's items
				for (item_key, item_value) in cp.items(section):
					if item_key in Config.HEADINGS.get(section):
						handle_recognized_section_item(section, item_key, item_value)
					else:
						handle_unrecognized_section_item(section, item_key, item_value)
				# end extract item
			else:
				logger.error("ERROR: skip unrecognized section heading [" + section + "] in config " + config_path)
			# handle "datasets" section
			if section == "datasets":
				handle_dataset_section(datasets_items, config_path)
		# end extract sections
	# end extract configs

def print_version(ctx, param, value):
	"""Print the current version of hermes and exit."""
	if not value:
		return 
	import pkg_resources
	version = None
	try:
		version = pkg_resources.get_distribution("hermes").version
	finally:
		del pkg_resources
	click.echo(version)
	ctx.exit()

# TODO: add option to print what recommenders
@click.command()
@click.option("--verbose", is_flag=True, \
	help="Print debug messages")
@click.option("--version", callback=print_version, is_flag=True, expose_value=False, is_eager=True, \
	help="Display hermes's version number")
@click.option("--hdfs_dir", default="datasets", \
	help="Name of HDFS directory to store input data.")
# IP address of fs.default.name used in HDFS
@click.argument("fs_default_ip_addr", default="localhost:9000")
@click.argument("list_of_files_config", type=click.Path(exists=True), nargs=1)
@click.argument("configs", type=click.Path(exists=True), nargs=-1)
def main(verbose, hdfs_dir, fs_default_ip_addr, list_of_files_config, configs):
	"""Hermes allows you to run multiple recommender system metrics on your chosen dataset."""

	# create logger
	logger = create_logger("hermes")

	# create state machine
	stateMachine = StateMachine()
	add_states(stateMachine)

	# create cargo
	cargo = Cargo()

	# add items to cargo
	cargo.scsingleton = create_sparkcontext()
	cargo.verbose = verbose
	cargo.hdfs_dir = hdfs_dir
	cargo.fs_default_ip_addr = fs_default_ip_addr

	# extract configs and add them to cargo
	extract_configs(configs, list_of_files_config, cargo, logger)

	# run state machine
	stateMachine.run(cargo)
	


