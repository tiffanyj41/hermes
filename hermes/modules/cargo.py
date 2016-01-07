class Cargo(object):
    """Cargo is the object passed around in the state machine. 
    It encapsulates all the parameters needed for each state in one object.

    * hdfs_dir: Name of HDFS directory to store input data. 
        One of the option passed in when running hermes binary. 
        Default = datasets.
    * fs_default_ip_addr: IP address of fs.default.name used in HDFS. 
        One of the arguments passed in when running hermes binary. 
        Default = localhost:9000.
    * datas: List of Data objects initialized when extracting the configuration file. 
    * vectors: List of Vector objects initialized during one of the states in the state machine, json_to_rdd_state.
    * support_files: Unrecognized items in [datasets] section of the configuration file that is presumed to be support files for the creation of a Vector.
    * recommenders: List of recommender system algorithms initialized when extracting the configuration file.
    * metrics: List of metrics initialized when extracting the configuration file.
    * error_msg: It starts out as an empty string that will be initialized as an error message to the error state.
    """
    # TODO: implement cargo as object pool model?
    def __init__(self):
        self.hdfs_dir = None
        self.fs_default_ip_addr = None
        self.datas = []     # used until json_to_rdd_state
        self.vectors = []   # used until develop_model_state
        self.support_files = {}
        # TODO: clean up so that there is only recommenders...and not user_recommenders & content_recommenders
        self.user_recommenders = []
        self.content_recommenders = []
        self.metrics = []
        self.error_msg = ""

