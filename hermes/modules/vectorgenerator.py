
# vector generator == rdd generator

import helper 
from hermesglobals import Globals

# ================================================================================
# Vector Factory
# ================================================================================

class VectorFactory(object):
    def create_vector(self, data, support_files, runs_from_notebook=False):
        # select which vector to create
        vector = None
        if data.which_vector == Globals.constants.USERVECTOR:
            vector = UserVector
        elif data.which_vector == Globals.constants.CONTENTVECTOR:
            vector = ContentVector
        else: 
            raise Exception
        # select if we are loading modules from a directory or a zip
        generator = None
        if runs_from_notebook:
            generator = helper.load_modules_in_zip(Globals.constants.ROOT_PATH, Globals.constants.DIR_VECTORS_NAME)
        else:
            generator = helper.load_modules_in_dir(Globals.constants.DIR_VECTORS_PATH)
        # get subclasses that inherit from either UserVector or ContentVector 
        # from modules in hermes/hermes/modules/vectors directory
        for module in generator:
            for subclass in helper.get_direct_subclasses(module, vector):
                if subclass.isSameDataInstance(data):
                    return subclass(data, support_files).vector
                else:
                    # cannot find class that builds the data
                    raise ValueError

    def create_obj_vector(self, data, support_files, runs_from_notebook=False):
        # select which vector to create
        vector = None
        if data.which_vector == Globals.constants.USERVECTOR:
            vector = UserVector
        elif data.which_vector == Globals.constants.CONTENTVECTOR:
            vector = ContentVector
        else: 
            raise Exception
        # select if we are loading modules from a directory or a zip
        generator = None
        if runs_from_notebook:
            generator = helper.load_modules_in_zip(Globals.constants.ROOT_PATH, Globals.constants.DIR_VECTORS_NAME)
        else:
            generator = helper.load_modules_in_dir(Globals.constants.DIR_VECTORS_PATH)
        # get subclasses that inherit from either UserVector or ContentVector 
        # from modules in hermes/hermes/modules/vectors directory
        for module in generator:
            for subclass in helper.get_direct_subclasses(module, vector):
                if subclass.isSameDataInstance(data):
                    return subclass(data, support_files)
                else:
                    # cannot find class that builds the data
                    raise ValueError

# ================================================================================
# Vector Factory Objects
# ================================================================================

class Vector(object):
    def __init__(self, data, support_files):
        self.data = data
        self.support_files = support_files
        vector_transformation = getattr(self, data.vector_transformation)
        if not vector_transformation:
            self.vector = None
        else:
            self.vector = vector_transformation()

    def split_data(self, weights, seed):
        raise NotImplemented

# ================================================================================
# User Vector and Content Vector Factory Objects
# ================================================================================

class UserVector(Vector):
    def __init__(self, data, support_files):
        super(UserVector, self).__init__(data, support_files)
        self.training_vector = None
        self.test_vector = None
        self.validation_vector = None
        self.prediction_vector = None

    def split_data(self, weights, seed):
        training_vector, test_vector, validation_vector = self.vector.randomSplit(weights, seed)
        self.training_vector = training_vector
        self.test_vector = test_vector
        self.validation_vector = validation_vector

class ContentVector(Vector):
    def __init__(self, data, support_files, uservector=None, runs_from_notebook=False):
        super(ContentVector, self).__init__(data, support_files)
        # TODO: terrible, quick fix -> fix it for real in the future
        if uservector is not None:
            self.uservector = uservector
        else:
            self.uservector = VectorFactory().create_obj_vector(self.data.uservectordata, support_files, runs_from_notebook)



# ================================================================================
# User Vector and Content Vector for specific datasetes
# defined in hermes/hermes/modules/vectors
# ================================================================================

