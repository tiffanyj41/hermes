import os




class Globals(object):
    """Globals contains global variables shared by all files.
    
    Args:
        verbose: a boolean variable that prints out debug log messages
        logger: logging object that logs messages
        scsingleton: Spark Context. There can only be one scsingleton running.
        DIR_VECTORS_PATH: a constant string that refers to the directory where vectorgenerators for specific datasets are resided
        DIR_RECOMMENDERS_PATH: a constant string that refers to the directory where recommendergenerators for specific recommenders are resided
        DIR_METRICS_PATH: a constant string that refers to the directory where metricgenerators for specific metrics are resided
    """

    class Constants(object):
        def __init__(self):
            self.DIR_VECTORS_PATH = os.path.dirname(os.path.realpath(__file__)) + "/" + "vg"
            self.DIR_RECOMMENDERS_PATH = os.path.dirname(os.path.realpath(__file__)) + "/" + "rg"
            self.DIR_METRICS_PATH = os.path.dirname(os.path.realpath(__file__)) + "/" + "mg"

        def __setattr__(self, attr, value):
            if hasattr(self, attr):
                print("ERROR: cannot reset a constant variable %s = %s" % (attr, value))
            else:
                self.__dict__[attr] = value

    verbose = False
    logger = None
    scsingleton = None
    constants = Constants()
