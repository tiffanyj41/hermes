import helper
import vectorgenerator # TODO: avoid this?

# TODO: a better way of storing configuration from configuration file?
class Data(object):
    """ Store configuration from configuration files. """

    def __init__(self, datapath, vector_transformation, schemapath, vectorizer):
        if helper.is_filepath_valid(datapath): 
            self.datapath = datapath
        self.vectorizer = vectorizer
        self.vector_transformation = vector_transformation
        self.schema = helper.get_schema(schemapath) 
        self.dataframe = None
        # TODO: do we need to know from which config the data is from? 

    def set_dataframe(self, scsingleton, datapath_in_hdfs):
        self.dataframe = scsingleton.sqlCtx.read.json(datapath_in_hdfs, self.schema)
        # explicitly repartition RDD after loading so that more tasks can run on it in parallel
        # by default, defaultMinPartitions == defaultParallelism == estimated # of cores across all of the machines in your cluster
        # TODO: a better way to go about the dataframe repartition?
        self.dataframe = self.dataframe.repartition(scsingleton.sc.defaultParallelism * 3)

        # set schema if it is not already set
        if self.schema is None: 
            self.schema = self.dataframe.schema

class UserVectorData(Data):
    def __init__(self, datapath, vector_transformation, schemapath, vectorizer):
        super(self.__class__, self).__init__(datapath, vector_transformation, schemapath, vectorizer)
        self.which_vector = vectorgenerator.UserVector

class ContentVectorData(Data):
    def __init__(self, datapath, vector_transformation, schemapath, vectorizer):
        super(self.__class__, self).__init__(datapath, vector_transformation, schemapath, vectorizer)
        self.which_vector = vectorgenerator.ContentVector





