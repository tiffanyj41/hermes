"""

with_tfidf = WithTfidf()
without_tfidf = WithoutTfidf()

recommender = ALS(with_tfidf)
recommender.make_prediction()

recommender = ALS(without_tfdif)
recommender.make_prediction()

recommender = CBWithKMeans(with_tfidf)
recommender.make_prediction()

recommender = CBWithKMeans(without_tfidf)
recommender.make_prediction()

"""

import logging
import sys
import timer
import pyspark.mllib.recommendation as mllib


# get logger
logger = logging.getLogger("hermes")

# ================================================================================
# Background implementation interface
# ================================================================================

class ImplementationInterface(object):
	def make_prediction_with_als(self):
		raise NotImplemented

	def make_prediction_with_cbkmeans(self):
		raise NotImplemented


# ================================================================================
# Concrete background implementations
# ================================================================================

# TODO: Interface is not necessary. 
# Should we remove ImplementationInterface? Or keep it for design sake?
class WithTfidf(ImplementationInterface):
	def make_prediction_with_als(self, vector):
		# create ALS model with tf-idf
		pass

	def make_prediction_with_cbkmeans(self, vector):
		# create CB with K-means with tf-idf
		pass

class WithoutTfidf(ImplementationInterface):
	def make_prediction_with_als(self, vector):
		# create ALS model without tf-idf
		# TODO: specify rank based on what the user wants
		model = mllib.ALS.train(vector.training_vector, rank=3)
		prediction_vector = model.predictAll( vector.test_vector.map( lambda x: (x[0], x[1]) ) ).cache()
		return prediction_vector


	def make_prediction_with_cbkmeans(self, vector):
		# create CB with K-means without tf-idf
		pass

# ================================================================================
# Target Interface
# ================================================================================

class AbstractInterface(object):
	def make_prediction(self):
		raise NotImplemented

# ================================================================================
# Bridge: bridge target interface & background implementation
# ================================================================================

# TODO: Interface is not necessary. 
# Should we remove ImplementationInterface? Or keep it for design sake?
class Recommender(AbstractInterface):
	def __init__(self, vector):
		self.vector = vector
		self.implementation = None

# ================================================================================
# Recommender Factory
# ================================================================================

class RecommenderFactory(object):
	def create_obj_recommender(self, recommender_str, vector, implementation=WithoutTfidf()):
		which_recommender = getattr(sys.modules[__name__], recommender_str)
		if not which_recommender:
			# cannot find class
			raise ValueError
		else:
			return which_recommender(vector, implementation)


# ================================================================================
# Variant of target interface
# ================================================================================

class ALS(Recommender):
	def __init__(self, vector, implementation=WithoutTfidf()):
		self.vector = vector
		self.implementation = implementation

	def make_prediction(self):
		return self.implementation.make_prediction_with_als(self.vector)

class CBWithKMeans(Recommender):
	def __init__(self, vector, implementation=WithoutTfidf()):
		self.vector = vector
		self.implementation = implementation

	def make_prediction(self):
		return self.implementation.make_prediction_with_cbkmeans(self.vector)

