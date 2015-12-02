"""Script to run hermes via command line."""

import click
import sys

import hermes
from modules.cargo import Cargo
from modules.statemachine import StateMachine


def add_states(stateMachine):
	""" json_to_rdd -> split_data - (Collaborative Filtering) -> develop_model -> calculate_metrics
	                              - (Content Based) -> ???
	"""
	stateMachine.add_state(hermes.start_state)
	stateMachine.add_state(hermes.json_to_rdd_state)
	stateMachine.add_state(hermes.split_data_state)
	stateMachine.add_state(hermes.develop_model_state)
	stateMachine.add_state(hermes.calculate_metrics_state, isEndState=1)
	stateMachine.add_state(hermes.error_state, isEndState=1)
	stateMachine.set_start(hermes.start_state)
	return

def create_logger():
	import logging
	logger = logging.getLogger(__name__)
	logger.setLevel(logging.DEBUG)
	# create file handler which logs even debug messages
	fh = logging.FileHandler("hermes.log")
	fh.setLevel(logging.DEBUG)
	# create console handler for stderr with a higher log level 
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
	from pyspark import SparkConf
	from modules.singleton import SCSingleton
	conf = SparkConf().setAppName("hermes")
	return SCSingleton(conf)

def extract_paths(file_with_paths):
	return [line.rstrip("\n") for line in open(file_with_paths)]

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

@click.command()
@click.option("--verbose", is_flag=True, \
	help="Print debug messages")
@click.option("--version", callback=print_version, is_flag=True, expose_value=False, is_eager=True, \
	help="Display hermes's version number")
@click.option("--hdfs_dir", default="datasets", \
	help="Name of HDFS directory to store input data.")
# IP address of fs.default.name used in HDFS
@click.argument("fs_default_ip_addr", default="localhost:9000")
# Path to a file that lists JSON files.
@click.argument("file_to_json_paths", type=click.Path(exists=True), nargs=1)
@click.option("--schemas", type=click.Path(exists=True), nargs=1, \
	help="Path to a file that lists each JSON file's schema.")
def main(verbose, hdfs_dir, fs_default_ip_addr, file_to_json_paths, schemas):
	"""Hermes allows you to run multiple recommender system metrics on your chosen dataset."""

	# create state machine
	stateMachine = StateMachine()
	add_states(stateMachine)

	# create cargo
	cargo = Cargo()

	# add items to cargo
	cargo.scsingleton = create_sparkcontext()
	cargo.logger = create_logger()
	cargo.verbose = verbose
	cargo.hdfs_dir = hdfs_dir
	cargo.fs_default_ip_addr = fs_default_ip_addr
	cargo.json_paths = extract_paths(file_to_json_paths)
	cargo.schema_paths = extract_paths(schemas)

	# run state machine
	stateMachine.run(cargo)
	


