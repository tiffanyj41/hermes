class InitializationError(Exception): pass

class StateMachine:
	def __init__(self):
		self.handlers = []
		self.startState = None
		self.endStates = []

	def add_state(self, handler, isEndState=0):
		self.handlers.append(handler)
		if isEndState:
			self.endStates.append(handler)

	def set_start(self, handler):
		self.startState = handler		

	def run(self, cargo=None):
		if not self.startState:
			raise InitializationError("Must call .set_start() before .run()")
		if not self.endStates:
			raise InitializationError("Must call .set_start() before .run()")

		handler = self.startState

		while True:
			(newState, cargo) = handler(cargo)
			if newState in self.endStates:
				newState(cargo)
				break
			elif newState not in self.handlers:
				print self.handlers
				raise RuntimeError("Invalid state %s" % newState)
			else:
				handler = newState

		return self