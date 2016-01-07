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

import helper

from hermesglobals import Globals
from rg.default_usecase import Default

# ================================================================================
# Bridge: bridge target interface & background implementation
# ================================================================================

class Recommender(object):
    def __init__(self, vector, implementation=Default()):
        self.vector = vector
        self.implementation = implementation

    def make_prediction(self):
        # target interface
        raise NotImplemented

# ================================================================================
# Recommender Factory
# ================================================================================

class RecommenderFactory(object):
    def create_obj_recommender(self, recommender_str, vector, implementation=Default()):
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

