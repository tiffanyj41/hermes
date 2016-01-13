from interface import ImplementationInterface

import hermes.metrics.cf as cf

# ================================================================================
# Concrete background implementations for default use cases
# ================================================================================

class Default(ImplementationInterface):
    def make_prediction_with_als(self, vector):
        # TODO: specify rank based on what the user wants
        """
        import pyspark.mllib.recommendation as mllib
        model = mllib.ALS.train(vector.training_vector, rank=3)
        prediction_vector = model.predictAll( vector.test_vector.map( lambda x: (x[0], x[1]) ) ).cache()
        return prediction_vector
        """
        vector.prediction_vector = cf.calc_cf_mllib(vector.training_vector)
        return vector.prediction_vector