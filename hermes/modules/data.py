import helper
import vectorgenerator 

class Data(object):

	def __init__(self, datapath, vector_type, schemapath, vectorizer):
		if helper.is_filepath_valid(datapath): 
			self.datapath = datapath
		self.vector_type = vector_type
		self.schema = helper.get_schema(schemapath) 
		self.dataframe = None
		self.vectorizer = vectorizer
		# TODO: do we need to know from which config the data is from? 

	def set_dataframe(self, scsingleton, datapath_in_hdfs):
		self.dataframe = scsingleton.sqlCtx.read.json(datapath_in_hdfs, self.schema)
		# explicitly repartition RDD after loading so that more tasks can run on it in parallel
    	# by default, defaultMinPartitions == defaultParallelism == estimated # of cores across all of the machines in your cluster
		self.dataframe = self.dataframe.repartition(scsingleton.sc.defaultParallelism * 3)

		# set schema if it is not already set
		if self.schema is None: 
			self.schema = self.dataframe.schema

class UserVectorData(Data):
	def __init__(self, datapath, vector_type, schemapath, vectorizer):
		super(self.__class__, self).__init__(datapath, vector_type, schemapath, vectorizer)
		self.which_vector = vectorgenerator.UserVector

class ContentVectorData(Data):
	def __init__(self, datapath, vector_type, schemapath, vectorizer):
		super(self.__class__, self).__init__(datapath, vector_type, schemapath, vectorizer)
		self.which_vector = vectorgenerator.ContentVector





