from framebase import frame
import logger, framebase, pygame
globals().update(logger.build_module_logger(__name__))

@frame.register_this("pygame_test")
class PygameTest(framebase.Module, framebase.Observer):
    def __init__(self):
        debug("PygameTest loading")

    def update(self, dt):
        if frame.statemanager.current=="example":
            pygame.draw.rect(frame.screen, (255,0,0), pygame.Rect(10,10,50,50))

    def handle_event_pygame_event(self, event):
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_n:
                frame.statemanager.push("example")
            if event.key==pygame.K_p:
                frame.statemanager.pop()
