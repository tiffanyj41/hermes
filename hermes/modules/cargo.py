class Cargo(object):
	"""Cargo contains objects that are passed around in the state machine.

	Args:
		scsingleton: Spark Context. There can only be one scsingleton running.
		logger:
		verbose:
		hdfs_dir:
		fs_default_ip_addr:
		json_paths:
		schema_path:
		schema:
		error_msg:
	"""
	def __init__(self):
		self.scsingleton = None
		self.logger = None
		self.verbose = False
		self.hdfs_dir = None
		self.fs_default_ip_addr = None
		self.json_paths = []
		self.schema_paths = []
		self.datums = []
		self.model = None
		self.error_msg = ""

