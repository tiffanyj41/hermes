
class Datum(object):
	"""Datum is a single data being subjected to 
	recommender system algorithms and performance metrics. 
	"""

	def __init__(self, json_path, rdd):
		self.json_path = json_path 
		self.rdd = rdd
		self.trainingRdd = None
		self.testRdd = None
		self.validationRdd = None

	def split_data(self, weights, seed):
		trainingRdd, testRdd, validationRdd = self.rdd.randomSplit(weights, seed)
		self.trainingRdd = trainingRdd.cache()
		self.testRdd = testRdd.cache()
		self.validationRdd = validationRdd.cache()




