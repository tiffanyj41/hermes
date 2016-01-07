"""Defined states in Hermes's state machine"""

import json
import logging
import os

import hermesui
import modules.helper as helper
import modules.metricgenerator as mg
import modules.recommendergenerator as rg
import modules.vectorgenerator as vg

from modules.hermesglobals import Globals
from modules.timer import Timer

# TODO: empty certain items in cargo after no longer needed? 
# TODO: when to use error_state? do try-catch for all states?

def start_state(cargo):
    """Start of the state machine. Create HDFS directory and upload the input data.
    Returns: json_to_rdd_state as next state
    """

    if Globals.verbose: Globals.logger.debug("In start_state:")

    if Globals.verbose: Globals.logger.debug("Creating the hdfs directory " + cargo.hdfs_dir)
    os.system("hdfs dfs -mkdir " + cargo.hdfs_dir)

    def load_json_files(datas):
        for i in range(0, len(datas)):
            json_path = datas[i].datapath
            if Globals.verbose: Globals.logger.debug("Loading JSON file " + json_path + " into hdfs directory " + cargo.hdfs_dir)
            os.system("hdfs dfs -put " + json_path + " " + cargo.hdfs_dir + "/" + os.path.basename(json_path))

    load_json_files(cargo.datas)

    newState = json_to_rdd_state
    if Globals.verbose: Globals.logger.debug("start_state -> json_to_rdd_state")

    return newState, cargo

# TODO: make json_to_rdd_state, split_data_state, and make_prediction_state into one state?
def json_to_rdd_state(cargo):
    """Parse JSON to RDD. 
    Returns: split_data_state as next state
    """

    if Globals.verbose: Globals.logger.debug("In json_to_rdd_state:")

    # create RDD for each JSON file and store it in Cargo's vectors list
    for i in range(0, len(cargo.datas)):
        data = cargo.datas[i]
        if Globals.verbose: Globals.logger.debug("Working with json file %s" % data.datapath)

        if Globals.verbose: Globals.logger.debug("Creating dataframe based on the content of the json file")
        datapath_in_hdfs = "hdfs://" + cargo.fs_default_ip_addr + "/" + cargo.hdfs_dir + "/" + os.path.basename(data.datapath)
        data.set_dataframe(Globals.scsingleton, datapath_in_hdfs)

        if Globals.verbose: Globals.logger.debug("Creating RDD based on the computed dataframe and configuration provided by the user")
        # TODO: remove sqlCtx since it's global?
        cargo.vectors.append( vg.VectorFactory().create_obj_vector(Globals.scsingleton.sqlCtx, data, cargo.support_files) ) 


    # TODO: clean cargo?
    # cargo.datas = []
    # cargo.hdfs_dir = None
    # cargo.fs_default_ip_addr = None

    newState = split_data_state
    if Globals.verbose: Globals.logger.debug("json_to_rdd_state -> split_data_state")

    return newState, cargo

def split_data_state(cargo):
    """Split data to train, test, and (optional) validate.
    Returns: make_prediction_state as next state
    """

    if Globals.verbose: Globals.logger.debug("In split_data_state:")

    for i in range(0, len(cargo.vectors)):
        vector = cargo.vectors[i]
        weights, seed = hermesui._ask_user_for_split_percentage(vector.data.datapath)
        vector.split_data(weights, seed)

    newState = make_prediction_state
    if Globals.verbose: Globals.logger.debug("split_data_state -> make_prediction_state")

    return newState, cargo

def make_prediction_state(cargo):
    """Develop model based on the train data and make prediction based on this model. 
    Returns: calculate_metrics_state as next state
    """

    if Globals.verbose: Globals.logger.debug("In make_prediction_state:")   

    for i in range(0, len(cargo.vectors)):
        thisvector = cargo.vectors[i]

        # select which recommenders based on the vector type
        recommenders = None
        if helper.is_direct_subclass(thisvector, vg.UserVector):
            if Globals.verbose: Globals.logger.debug("Iterating through recommenders for user vector on data %s", thisvector.data.datapath)
            recommenders = cargo.user_recommenders
        elif helper.is_direct_subclass(thisvector, vg.ContentVector):
            if Globals.verbose: Globals.logger.debug("Iterating through recommenders for content vector on data %s", thisvector.data.datapath)
            recommenders = cargo.content_recommenders

        # run all recommenders on the vector
        for r in recommenders:
            if Globals.verbose: Globals.logger.debug("Making recommendation %s on data %s", r, thisvector.data.datapath)
            # TODO: implement other use case, ie. WithTfidf(), etc.
            recommender = rg.RecommenderFactory().create_obj_recommender(r, thisvector)
            # default use case
            # recommender = RecommenderFactory().create_obj_recommender(r, vector, Default())
            # with tf-idf use case 
            # recommender = RecommenderFactory().create_obj_recommender(r, vector, WithTfidf())
            # without tf-idf use case
            # recommender = RecommenderFactory().create_obj_recommender(r, vector, WithoutTfidf())
            # etc.
            with Timer() as t:
                thisvector.prediction_vector = recommender.make_prediction()
            if Globals.verbose: Globals.logger.debug("Making prediction takes %s seconds" % t.secs)

    newState = calculate_metrics_state
    if Globals.verbose: Globals.logger.debug("make_prediction_state -> calculate_metrics_state")

    return newState, cargo

def calculate_metrics_state(cargo):
    """Test the metrics specified by the user. This is an end state.
    Returns: None because this is the last state
    """

    if Globals.verbose: Globals.logger.debug("In calculate_metrics_state:")

    # create a metric executor
    executor = mg.MetricExecutor(mg.Metric())

    # TODO: figure out why logger prints INFO twice
    for i in range(0, len(cargo.vectors)):
        Globals.logger.info("-" * 80)
        Globals.logger.info("Data: %s" % cargo.vectors[i].data.datapath)
        for m in cargo.metrics:
            # check if metric exists
            metric = mg.MetricFactory().create_obj_metric(m)
            # set metric in executor
            executor.change_metric(metric)
            # execute the metric
            with Timer() as t:
                Globals.logger.info("Metric: %s = %f" % (m, executor.execute(cargo.vectors[i])))
            if Globals.verbose: Globals.logger.debug("Calculating metric takes %s seconds" % t.secs)
        Globals.logger.info("-" * 80)
    if Globals.verbose: Globals.logger.debug("calculate_metrics_state -> end_state")

    return

def error_state(cargo):
    """Error state. Print out the error messages. This is an end state.
    Returns: None because this is the last state
    """
    if Globals.verbose: Globals.logger.debug("In error_state:")
    Globals.logger.error("ERROR: " + cargo.error_msg)
    if Globals.verbose: Globals.logger.debug("error_state -> end_state")
    return

