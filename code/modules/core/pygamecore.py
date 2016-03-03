from framebase import frame
import logger, framebase, pygame
globals().update(logger.build_module_logger("pygame"))

@frame.register_this("pygame")
class PygameCore(framebase.Observer):
    def __init__(self):
        pass

    def run_main(self):
        info("Initializing PygameCore")
        pygame.init()
        frame.screen=pygame.display.set_mode((800,600))
        pygame.display.set_caption(frame.loader["window_title"])
        clock=pygame.time.Clock()
        running=True

        frame.send_event("core_loaded")

        while running:
            clock.tick(frame.loader["target_fps"])
            dt=(1/clock.get_fps() if clock.get_fps()>0 else 0)
            frame.screen.fill((0,0,0))
            frame.send_event("render", dt)
            pygame.display.update()
            for event in pygame.event.get():
                frame.send_event("pygame_event", event)
                if event.type==pygame.QUIT:
                    frame.send_event("shutdown")
                    running=False


    def handle_event_shutdown(self):
        info("Uninitializing PygameCore")
        pygame.quit()
