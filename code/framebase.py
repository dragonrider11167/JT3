

class _Frame:
    def __init__(self):
        self.modules={
            "loader":loader.Loader()
        }
        self._observers=[]

    def __getattr__(self, name):
        if name in self.__dict__:
            return object.__getattr__(self, name)
        else:
            return self.modules[name]

    def register_this(self, name):
        def _register_module_decorator(module):
            self.modules[name]=module()
            if isinstance(self.modules[name], Observer):
                self._observers.append(self.modules[name])
        return _register_module_decorator

    def send_event(self, name, *a, **k):
        # print(name)
        for module in self._observers:
            module.handle_event(name, *a, **k)

class Serializable:
    def load_data(self, data):
        pass

    def save_data(self, data):
        pass

class Observer:
    def handle_event(self, name, *args, **kwargs):
        if "handle_event_"+name in dir(self):
            getattr(self, "handle_event_"+name)(*args, **kwargs)

import loader
frame=_Frame()
