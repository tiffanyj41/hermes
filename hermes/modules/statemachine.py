class InitializationError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class StateMachine:
    """
    To emulate a state machine.

    Example:
    # state1 -> state2 -> state3a
                       -> state3b
    # where state1, state2, state3a, and state3b are defined functions.

        import StateMachine
        sm = StateMachine()
        sm.add_state(state1)
        sm.add_state(state2)
        sm.add_state(state3a, isEndState=True)
        sm.add_state(state3b, isEndState=True)
        sm.set_start(state1)
        sm.run()
    """

    def __init__(self):
        self.handlers = []
        self.startState = None
        self.endStates = []

    def add_state(self, handler, isEndState=False):
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