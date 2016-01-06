
# vector generator == rdd generator

import helper 
from hermesglobals import Globals

# ================================================================================
# Vector Factory
# ================================================================================

class VectorFactory(object):
    def create_vector(self, sqlCtx, data, support_files):
        vector = data.which_vector
        # get subclasses that inherit from either UserVector or ContentVector 
        # from modules in hermes/hermes/modules/vectors directory
        for module in helper.load_modules_in_dir(Globals.constants.DIR_VECTORS_PATH):
            for subclass in helper.get_direct_subclasses(module, vector):
                if subclass.isSameDataInstance(data):
                    return subclass(sqlCtx, data, support_files).vector
                else:
                    # cannot find class that builds the data
                    raise ValueError

    def create_obj_vector(self, sqlCtx, data, support_files):
        vector = data.which_vector
        # get subclasses that inherit from either UserVector or ContentVector 
        # from modules in hermes/hermes/modules/vectors directory
        for module in helper.load_modules_in_dir(Globals.constants.DIR_VECTORS_PATH):
            for subclass in helper.get_direct_subclasses(module, vector):
                if subclass.isSameDataInstance(data):
                    return subclass(sqlCtx, data, support_files)
                else:
                    # cannot find class that builds the data
                    raise ValueError

# ================================================================================
# Vector Factory Objects
# ================================================================================

class Vector(object):
    def __init__(self, sqlCtx, data, support_files):
        # TODO: remove sqlCtx because it is global?
        self.sqlCtx = sqlCtx
        self.data = data
        self.support_files = support_files
        vector_transformation = getattr(self, data.vector_transformation)
        if not vector_transformation:
            self.vector = None
        else:
            self.vector = vector_transformation()
        self.training_vector = None
        self.test_vector = None
        self.validation_vector = None
        self.prediction_vector = None

    def split_data(self, weights, seed):
        training_vector, test_vector, validation_vector = self.vector.randomSplit(weights, seed)
        self.training_vector = training_vector
        self.test_vector = test_vector
        self.validation_vector = validation_vector

# ================================================================================
# User Vector and Content Vector Factory Objects
# ================================================================================

class UserVector(Vector):
    pass

class ContentVector(Vector):
    pass

# ================================================================================
# User Vector and Content Vector for specific datasetes
# defined in hermes/hermes/modules/vectors
# ================================================================================

