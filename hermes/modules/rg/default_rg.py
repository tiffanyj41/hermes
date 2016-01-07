from interface import ImplementationInterface

import pyspark.mllib.recommendation as mllib

# ================================================================================
# Concrete background implementations
# ================================================================================

class Default(ImplementationInterface):
    def make_prediction_with_als(self, vector):
        # TODO: specify rank based on what the user wants
        model = mllib.ALS.train(vector.training_vector, rank=3)
        prediction_vector = model.predictAll( vector.test_vector.map( lambda x: (x[0], x[1]) ) ).cache()
        return prediction_vector