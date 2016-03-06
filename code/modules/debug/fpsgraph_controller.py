from framebase import frame
import logger, framebase
globals().update(logger.build_module_logger("fpsgraph"))

@frame.register_this("fpsgraph_controller")
class FPSGraphController(framebase.Observer):
    def handle_event_core_loaded(self):
        frame.load_library_as_module("fpsgraph")

    def handle_event_pygame_batch_events(self, events):
        frame.fpsgraph.event(events)

    def handle_event_render(self, dt):
        frame.fpsgraph.update({"frame":frame})
        frame.fpsgraph.render(frame.screen)
