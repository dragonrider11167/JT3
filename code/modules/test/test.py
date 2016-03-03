from framebase import frame
import logger, framebase
globals().update(logger.build_module_logger(__name__))

frame.loader.require_modules("entities")

class DemoRenderComponent(frame.entities.Component):
    def handle_event_render(self, dt):
        frame.screen.blit(frame.loader["test"], (10,10))

@frame.register_this("entity_test")
class EntityTest(framebase.Observer):
    def __init__(self):
        debug("EntityTest loading")

    def handle_event_core_loaded(self):
        debug("Got core_loaded event!")
        frame.entities.add_entity(frame.entities.Entity.from_dict(frame.loader["cfg_ent_test"]))
        frame.statemanager.push("game")
