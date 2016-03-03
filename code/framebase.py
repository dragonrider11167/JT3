

class _Frame:
    def __init__(self):
        self.modules={
            "loader":loader.Loader()
        }
        self._observers=[]

    def __getattr__(self, name):
        try:
            return object.__getattr__(self, name)
        except AttributeError:
            return self.modules[name]

    def register_this(self, name):
        def _register_module_decorator(module):
            self.modules[name]=module()
            if isinstance(self.modules[name], Observer):
                self._observers.append(self.modules[name])
        return _register_module_decorator

    def send_event(self, name, *a, **k):
        for module in self._observers:
            module.handle_event(name, *a, **k)

    def update(self, dt):
        for module in self.modules.values():
            module.update(dt)

class Serializable:
    def load_data(self, data):
        pass

    def save_data(self, data):
        pass

class Module(Serializable):
    def init_config(self):
        pass

    def update(self, dt):
        pass

class Observer:
    def handle_event(self, name, *args, **kwargs):
        try:
            getattr(self, "handle_event_"+name)(*args, **kwargs)
        except AttributeError:
            pass
import loader
frame=_Frame()
