"""Hermes's entry point"""

import click
import ConfigParser
import itertools
import json
import logging
import sys
from pyspark import SparkConf

import hermes
import modules.config as config

from modules.cargo import Cargo
from modules.data import UserVectorData, ContentVectorData
from modules.hermesglobals import Globals
from modules.singleton import SCSingleton
from modules.statemachine import StateMachine


def add_states(state_machine):
    """ Add states to the given state machine.

    The current implemented state machine follows this path:
        json_to_rdd -> split_data -> make_prediction -> calculate_metrics

    Args: 
        state_machine: state machine 
    """
    state_machine.add_state(hermes.start_state)
    state_machine.add_state(hermes.json_to_rdd_state)
    state_machine.add_state(hermes.split_data_state)
    state_machine.add_state(hermes.make_prediction_state)
    state_machine.add_state(hermes.calculate_metrics_state, isEndState=True)
    state_machine.add_state(hermes.error_state, isEndState=True)
    state_machine.set_start(hermes.start_state)
    return

def create_logger(name):
    """ Create logger with the given name if it's not already created. 

    Args:
        name: name of logger
    Returns:
        logger
    """
    logger = logging.getLogger(name)

    # check if logger is already created; if not, create it
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        # create hermes.log file that prints out debug messages
        fh = logging.FileHandler("hermes.log")
        fh.setLevel(logging.DEBUG)
        # create console handler for stderr that prints out error messages
        che = logging.StreamHandler()
        che.setLevel(logging.ERROR)
        # create console handler for stdout for info, debug, and error level
        chod = logging.StreamHandler(sys.stdout)
        chod.setLevel(logging.DEBUG)
        choe = logging.StreamHandler(sys.stdout)
        choe.setLevel(logging.ERROR)
        # create formatter and add it to the handlers
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        fh.setFormatter(formatter)
        che.setFormatter(formatter)
        chod.setFormatter(formatter)
        choe.setFormatter(formatter)
        # add handlers to logger    
        logger.addHandler(fh)
        logger.addHandler(che)
        logger.addHandler(chod)
        logger.addHandler(choe)

    return logger

def create_sparkcontext():
    """ Create a single Spark Context with the app name hermes.

    Returns:
        SCSingleton: wrapper object that prevents multiple instantiation of the spark context

    """
    conf = SparkConf().setAppName("hermes")
    return SCSingleton(conf)


# TODO: is there a better way to implement this function?
def extract_configs(configs_path, list_of_files_config_path, cargo):
    """ Extract configuration files and store the configurations in cargo.

    Args:
        configs_path: list of paths to configuration files
        list_of_files_config_path: path to list of files configuration file
        cargo: object passed in state machine

    """

    # extract list_of_files_config
    lofcp = ConfigParser.ConfigParser()
    lofcp.read(list_of_files_config_path)

    def handle_recognized_section_item(section, item_key, item_value):
        """ Helper function that extracts recognized section items. """
        if section == "datasets":
            datasets_items[item_key] = item_value
            # [datasets] items will be placed into cargo in handle_dataset_section()
            return
        if section == "recommenders":
            if item_key == "user_recommenders":
                # add list of recommenders for user vectors into cargo
                cargo.user_recommenders.extend( json.loads(item_value) )
            elif item_key == "content_recommenders":
                # add list of recommenders for content vectors into cargo
                cargo.content_recommenders.extend( json.loads(item_value) )
            return
        if section == "metrics":
            if item_key == "metrics":
                # add list of metrics into cargo
                cargo.metrics.extend( json.loads(item_value) )
            return          

    def handle_unrecognized_section_item(section, item_key, item_value):
        """ Helper function that extracts unrecognized section items. """
        if section == "datasets":
            # any unrecognized [datasets] items will be placed in cargo's support_files dictionary
            cargo.support_files[item_key] = item_value
            return
        if section == "recommenders":
            Globals.logger.error("ERROR: skip unrecognized item " +  item_key + " under section [" + section + "] in config" + config_path)
            return
        if section == "metrics":
            Globals.logger.error("ERROR: skip unrecognized item " +  item_key + " under section [" + section + "] in config" + config_path)
            return

    def handle_dataset_section(dataset_items, config_path):
        """ Helper function that handles [datasets] section. """
        # TODO: which is better? iterating through sections then items or iterating through just items of list_of_files_config?
        
        # make sure dataname is initialized in order to verify the section in list_of_files_config
        if not ("dataname" in datasets_items.keys()):
            Globals.logger.error("ERROR: config " + config_path + " must have dataname specified.")
            sys.exit()

        dataname = datasets_items["dataname"]
        lofmap = config.map_section(lofcp, dataname)

        # create UserVectorData or ContentVectorData or both
        hasUserVector = False
        # check it has the required items to build a UserVectorData
        if set(config.REQ_UV_HEADINGS) < set(datasets_items.keys()): 
            hasUserVector = True
            create_datas(lofmap, dataname, datasets_items, config_path, isUserVector=True)

        hasContentVector = False 
        # check it has the required items to build a ContentVectorData
        if set(config.REQ_CV_HEADINGS) < set(datasets_items.keys()):
            hasContentVector = True
            create_datas(lofmap, dataname, datasets_items, config_path, isUserVector=False)

        if not hasUserVector and not hasContentVector:
            Globals.logger.error("ERROR: config " + config_path + " does not have declaration for a user vector or a content vector")
            sys.exit()  

    def create_datas(lofmap, dataname, datasets_items, config_path, isUserVector):
        """ Helper function that creates a UserVectorData or ContentVectorData depending if it isUserVector or not. 
            
        Storing configuration for UserVector or ContentVector in an object (like UserVectorData and ContentVectorData)
        is easier than storing its individual parts. UserVectorData and ContentVectorData will be added into cargo in
        cargo's data list.
        """

        if isUserVector:
            datapaths_heading = "user_vector_data"
            vector_transformations_heading = "user_vector_transformations"
            schemapaths_heading = "user_vector_schemas"
        else:
            datapaths_heading = "content_vector_data"
            vector_transformations_heading = "content_vector_transformations"
            schemapaths_heading = "content_vector_schemas"

        datapaths = json.loads(datasets_items[datapaths_heading])
        vector_transformations = json.loads(datasets_items[vector_transformations_heading])
        hasSchemas = False
        if schemapaths_heading in datasets_items.keys():
            schemapaths = json.loads(datasets_items[schemapaths_heading])
            hasSchemas = True

        # check that a vector transformation is specified for each data
        # TODO: multiple vector trasnformation for each data in the future?
        if len(datapaths) != len(vector_transformations):
            Globals.logger.error("ERROR: must specify a vector type for each data in config " + config_path)
            sys.exit()

        for i in range(0, len(datapaths)):
            # set datapath
            try:
                datapath = lofmap[datapaths[i]]
            except KeyError:
                Globals.logger.error("ERROR: cannot find data " + datapath + " in the list_of_files_config for config " + config_path)
                sys.exit()
            # set vector_transformation
            vector_transformation = vector_transformations[i]
            # set schemapath
            try:
                if hasSchemas: schemapath = lofmap[schemapaths[i]]
            except IndexError, KeyError:
                schemapath = None

            if isUserVector: 
                uservectordata = UserVectorData(datapath, vector_transformation, schemapath, dataname)
                cargo.datas.append(uservectordata)
            else:
                contentvectordata = ContentVectorData(datapath, vector_transformation, schemapath, dataname)
                cargo.datas.append(contentvectordata)

    # extract configs
    for config_path in configs_path:
        cp = ConfigParser.ConfigParser()
        cp.read(config_path)
        datasets_items = {}
        # extract sections
        for section in cp.sections():
            if section in config.HEADINGS.keys():
                # extract section's items
                for (item_key, item_value) in cp.items(section):
                    if item_key in config.HEADINGS.get(section):
                        handle_recognized_section_item(section, item_key, item_value)
                    else:
                        handle_unrecognized_section_item(section, item_key, item_value)
                # end extract items
            else:
                Globals.logger.error("ERROR: skip unrecognized section heading [" + section + "] in config " + config_path)
            # handle [datasets] section
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

def print_data(ctx, param, value):
    """Print a list of data currently supported and exit."""
    if not value:
        return
    click.echo("This option is not yet implemented.")
    ctx.exit()

def print_recommenders(ctx, param, value):
    """Print a list of recommender system algorithms currently supported and exit."""
    if not value:
        return
    click.echo("This option is not yet implemented.")
    ctx.exit()

def print_metrics(ctx, param, value):
    """Print a list of metrics currently supported and exit."""
    if not value:
        return
    click.echo("This option is not yet implemented.")
    ctx.exit()

# TODO: implement print_data, print_recommenders, print_metrics?
@click.command()
@click.option("--version", callback=print_version, is_flag=True, expose_value=False, is_eager=True, \
    help="Display hermes's version number.")
@click.option("--data", callback=print_data, is_flag=True, expose_value=False, is_eager=True, \
    help="Print a list of data currently supported.")
@click.option("--algos", callback=print_recommenders, is_flag=True, expose_value=False, is_eager=True, \
    help="Print a list of recommender system algorithms currently supported.")
@click.option("--metrics", callback=print_metrics, is_flag=True, expose_value=False, is_eager=True, \
    help="Print a list of metrics currently supported.")
@click.option("--verbose", is_flag=True, \
    help="Print debug messages")
@click.option("--hdfs_dir", default="datasets", \
    help="Name of HDFS directory to store input data. Default = datasets.")
# IP address of fs.default.name used in HDFS
@click.argument("fs_default_ip_addr", default="localhost:9000")
@click.argument("list_of_files_config", type=click.Path(exists=True), nargs=1)
@click.argument("configs", type=click.Path(exists=True), nargs=-1)
def main(verbose, hdfs_dir, fs_default_ip_addr, list_of_files_config, configs):

    # initialize global variables
    Globals.verbose = verbose
    Globals.logger = create_logger("hermes")
    Globals.scsingleton = create_sparkcontext()

    # create state machine
    state_machine = StateMachine()
    add_states(state_machine)

    # create cargo
    cargo = Cargo()

    # add items to cargo
    cargo.hdfs_dir = hdfs_dir
    cargo.fs_default_ip_addr = fs_default_ip_addr
    # extract configs and add them to cargo
    extract_configs(configs, list_of_files_config, cargo)

    # run state machine
    state_machine.run(cargo)
    


