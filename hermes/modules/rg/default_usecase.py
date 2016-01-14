from interface import ImplementationInterface

import hermes.algorithms.cf as cf

# ================================================================================
# Concrete background implementations for default use cases
# ================================================================================

class Default(ImplementationInterface):
    def make_prediction_with_als(self, user_vector, content_vector):
        user_vector.prediction_vector = cf.calc_cf_mllib(user_vector.training_vector)
        return user_vector.prediction_vector

        """
        # TODO: specify rank based on what the user wants
        import pyspark.mllib.recommendation as mllib
        model = mllib.ALS.train(vector.training_vector, rank=3)
        prediction_vector = model.predictAll( vector.test_vector.map( lambda x: (x[0], x[1]) ) ).cache()
        return prediction_vector
        """

    def make_prediction_with_useruser(self, user_vector, content_vector):
        user_vector.prediction_vector = cf.calc_user_user_cf2(user_vector.training_vector)
        return user_vector.prediction_vector

    def make_prediction_with_itemitem(self, user_vector, content_vector):
        user_vector.prediction_vector = cf.calc_item_item_cf(user_vector.training_vector)
        return user_vector.prediction_vector
