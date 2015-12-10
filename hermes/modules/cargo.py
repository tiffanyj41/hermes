class Cargo(object):
	"""Cargo contains objects that are passed around in the state machine.

	Args:
		scsingleton: Spark Context. There can only be one scsingleton running.
		verbose: a boolean variable that prints out log messages
		hdfs_dir:
		fs_default_ip_addr:
		error_msg:
	"""
	# TODO: implement cargo as object pool model?
	def __init__(self):
		self.scsingleton = None
		self.verbose = False
		self.hdfs_dir = None
		self.fs_default_ip_addr = None
		self.error_msg = ""
		self.datas = []		# used until json_to_rdd_state
		self.vectors = []	# used until develop_model_state
		self.support_files = {}
		self.recommenders = []
		self.metrics = []

