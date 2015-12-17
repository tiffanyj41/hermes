class Globals(object):
    """Globals contains global variables shared by all files.
    
    Args:
        verbose: a boolean variable that prints out debug log messages
        logger: logging object that logs messages
        scsingleton: Spark Context. There can only be one scsingleton running.
    """
    verbose = False
    logger = None
    scsingleton = None
