from interface import ImplementationInterface

import hermes.algorithms.cf as cf

# ================================================================================
# Concrete background implementations for default use cases
# ================================================================================

class SecondUseCase(ImplementationInterface):

    def make_prediction_with_useruser(self, user_vector, content_vector):
        user_vector.prediction_vector = cf.calc_user_user_cf(user_vector.training_vector)
        return user_vector.prediction_vector

