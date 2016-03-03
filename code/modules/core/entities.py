from framebase import frame
import logger, framebase
globals().update(logger.build_module_logger("entities"))

class Entity(framebase.Observer):
    def __init__(self, components):
        self.components=components
        self.kill=0
        for v in self.components.values():
            v.bind(self)

    @classmethod
    def from_dict(cls, data):
        debug("Creating entity from "+str(data))
        components={}
        for k, v in data.items():
            components[k]=frame.entities.component_collection[k].from_dict(v)
        return cls(components)

    def __getattr__(self, k):
        if k in self.__dict__:
            return object.__getattr__(self, k)
        else:
            return self.components[k]

    def handle_event(self, e, *a, **k):
        for v in self.components.values():
            v.handle_event(e, *a, **k)

class Component(framebase.Observer):
    def bind(self, parent):
        self.entity=parent

    @classmethod
    def from_dict(cls, data):
        new=cls()
        new.__dict__.update(data)
        return new

@frame.register_this("entities")
class EntitiyManager(framebase.Observer):
    Entity=Entity
    Component=Component
    def __init__(self):
        self.entities={}
        self.component_collection={}

    def register_this_component(self, name):
        def _register_this_component(cls):
            self.component_collection[name]=cls
        return _register_this_component

    def handle_event(self, event, *a, **k):
        if frame.statemanager.current==frame.loader["entity_run_state"]:
            to_delete=[]
            for name, entity in self.entities.items():
                entity.handle_event(event, *a, **k)
                if entity.kill:
                    to_delete.append(name)
            for name in to_delete:
                del self.entities[name]

    def add_entity(self, e, name=None):
        self.entities[name if name else str(len(self.entities.keys()))]=e
        e.handle_event("bound_to_manager")
