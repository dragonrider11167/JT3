from framebase import frame
import logger, framebase
globals().update(logger.build_module_logger(__name__))

@frame.register_this("controls_provider")
class FPSInTitleProvider(framebase.Observer):
    def __init__(self):
        debug("FPSInTitleProvider loading")

    def handle_event_core_loaded(self):
        self.titlebase=frame.pygame.display.get_caption()[0]

    def handle_event_render(self, dt):
        frame.pygame.display.set_caption(self.titlebase+" "+str(1/max(dt, 0.0000000000000000000000000000001)))
