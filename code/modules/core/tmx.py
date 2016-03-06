from framebase import frame
import logger, pygame, framebase
globals().update(logger.build_module_logger("tmx_loader"))

frame.loader.require_library("pygame", "pytmx")

debug("Requesting pytmx load")
try:
    frame.load_library_as_module("pytmx")
except ImportError:
    error("pytmx not availible, failing")
    frame.loader.abort_module_load("pytmx not availible")

debug("Success!")

class TMXMap:
    def __init__(self, fn):
        self.map=frame.pytmx.util_pygame.load_pygame(fn)
        self.surf=pygame.Surface((self.map.width*self.map.tilewidth, self.map.height*self.map.tileheight))
        self.named_contained_entites={}
        self.contained_entities=[]
        self._process_map()

    def _process_map(self):
        for layer in self.map.visible_layers:
            if isinstance(layer, frame.pytmx.TiledTileLayer):
                for x, y, image in layer.tiles():
                    self.surf.blit(image, (x*self.map.tilewidth, y*self.map.tileheight))
            if isinstance(layer, frame.pytmx.TiledObjectGroup):
                for obj in layer:
                    if layer.name=="collision":
                        d={"rect":{
                            "x":obj.x,
                            "y":obj.y,
                            "width":obj.width,
                            "height":obj.height
                        }}
                        d.update(frame.loader["collision_prototype"])
                        self.contained_entities.append(frame.entities.Entity.from_dict(d))
                    else:
                        self._handle_entity(obj)

    def add_entities_to(self, manager):
        for e in self.contained_entities:
            manager.add_entity(e)
        for k, e in self.named_contained_entites.items():
            manager.add_entity(e, k)

    def _handle_entity(self, data):
        if "_prototype" in data.properties:
            e=frame.entities.Entity.from_dict(frame.loader[data.properties["_prototype"]])
        e.rect.x=data.x
        e.rect.y=data.y
        if "_id" in data.properties:
            self.named_contained_entites[data.properties["_id"]]=e
        else:
            self.contained_entities.append(e)


@frame.register_this("tmxmap", insert_order=0)
class PyTmxMap(framebase.Observer):
    def __init__(self):
        self.current=None

    def load_map(self, fn):
        info("Loading map "+fn)
        frame.send_event("tmx_will_load_map", fn)
        self.current=TMXMap(fn)
        self.current.add_entities_to(frame.entities)
        frame.send_event("tmx_loaded_map", fn)

    def handle_event_render(self, dt):
        if frame.statemanager.current==frame.loader["tmx_run_state"] and self.current:
            frame.screen.blit(self.current.surf, (0,0))
