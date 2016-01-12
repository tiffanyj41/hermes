import helper 
from hermesglobals import Globals

# TODO: a better way of storing configuration from configuration file?
class Data(object):
    """ Store configuration from configuration files. """

    def __init__(self, datapath, vector_transformation, schemapath, dataname):
        #if not helper.is_filepath_valid(datapath): 
        #    raise OSError
        self.datapath = datapath
        self.dataname = dataname
        self.vector_transformation = vector_transformation
        self.schema = helper.get_schema(schemapath) 
        self.dataframe = None
        # TODO: do we need to know from which config the data is from? 

    def set_dataframe(self, sc, sqlCtx, datapath_in_hdfs):
        self.dataframe = sqlCtx.read.json(datapath_in_hdfs, self.schema)
        # explicitly repartition RDD after loading so that more tasks can run on it in parallel
        # by default, defaultMinPartitions == defaultParallelism == estimated # of cores across all of the machines in your cluster
        # TODO: a better way to go about the dataframe repartition?
        self.dataframe = self.dataframe.repartition(sc.defaultParallelism * 3)

        # set schema if it is not already set
        if self.schema is None: 
            self.schema = self.dataframe.schema

class UserVectorData(Data):
    def __init__(self, datapath, vector_transformation, schemapath, dataname):
        super(self.__class__, self).__init__(datapath, vector_transformation, schemapath, dataname)
        self.which_vector = Globals.constants.USERVECTOR

class ContentVectorData(Data):
    def __init__(self, datapath, vector_transformation, schemapath, dataname):
        super(self.__class__, self).__init__(datapath, vector_transformation, schemapath, dataname)
        self.which_vector = Globals.constants.CONTENTVECTOR





