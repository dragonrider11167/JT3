from framebase import frame
import logger, framebase
globals().update(logger.build_module_logger("states"))

class StateData:
    def __init__(self):
        self.initilized=False

@frame.register_this("statemanager")
class StateManager:
    def __init__(self):
        self.stack=[] # [[name, statedata],...]

    @property
    def current(self):
        return self.stack[-1][0] if self.stack else None

    @property
    def current_data(self):
        return self.stack[-1][1] if self.stack else None

    def push(self, state):
        debug("Entering state "+state)
        if self.current:
            frame.send_event("state_suspending", self.current)
        self.stack.append([state, StateData()])
        frame.send_event("state_starting", self.current)

    def pop(self):
        frame.send_event("state_ending", self.current)
        self.stack.pop()
