"""

with_tfidf = WithTfidf()
without_tfidf = WithoutTfidf()

recommender = ALS(with_tfidf)
recommender.make_prediction()

recommender = ALS(without_tfdif) # same as: recommender = ALS()
recommender.make_prediction()

recommender = CBWithKMeans(with_tfidf)
recommender.make_prediction()

recommender = CBWithKMeans(without_tfidf) # same as: recommender = CBWithKMeans
recommender.make_prediction()

"""

import sys
import timer
import pyspark.mllib.recommendation as mllib

from modules.globals import Globals

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

# TODO: ask Anna for the specifics
class WithTfidf(ImplementationInterface):
    """
    # TODO
    def make_prediction_with_cbkmeans(self, vector):
        # create CB with K-means with tf-idf
        raise NotImplemented
    """

class WithoutTfidf(ImplementationInterface):
    def make_prediction_with_als(self, vector):
        # create ALS model without tf-idf
        # TODO: specify rank based on what the user wants
        model = mllib.ALS.train(vector.training_vector, rank=3)
        prediction_vector = model.predictAll( vector.test_vector.map( lambda x: (x[0], x[1]) ) ).cache()
        return prediction_vector

    """
    # TODO
    def make_prediction_with_cbkmeans(self, vector):
        # create CB with K-means without tf-idf
        raise NotImplemented
    """

# ================================================================================
# Bridge: bridge target interface & background implementation
# ================================================================================

class Recommender(object):
    def __init__(self, vector, implementation=WithoutTfidf()):
        self.vector = vector
        self.implementation = implementation

    def make_prediction(self):
        # target interface
        raise NotImplemented

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
    def make_prediction(self):
        return self.implementation.make_prediction_with_als(self.vector)

class CBWithKMeans(Recommender):
    def make_prediction(self):
        return self.implementation.make_prediction_with_cbkmeans(self.vector)

