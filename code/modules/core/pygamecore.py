from framebase import frame
import logger, framebase
globals().update(logger.build_module_logger("pygame"))

try: frame.load_library_as_module("pygame")
except ImportError: error("Pygame not availible, PygameCore will fail!")

@frame.register_this("pygamecore")
class PygameCore(framebase.Observer):
    def __init__(self):
        pass

    def preinit(self):
        info("Initilizing PygameCore base")
        frame.pygame.init()
        frame.screen=frame.pygame.display.set_mode((10,10))
        frame.pygame.display.set_caption("Loading")

    def run_main(self):
        info("Initializing PygameCore")
        frame.pygame.init()
        frame.screen=frame.pygame.display.set_mode((800,600))
        frame.pygame.display.set_caption(frame.loader["window_title"])
        self.clock=frame.pygame.time.Clock()
        running=True

        debug("Creating a PyConsole (enabled ="+str(frame.loader["enable_pyconsole"])+")")
        self.pyconsole=frame._pyconsole_Console(frame.screen, (0,0,800,200), localsx={"frame":frame})

        frame.send_event("core_loaded")

        while running:
            self.clock.tick(frame.loader["target_fps"]) if frame.loader["target_fps"]!=-1 else self.clock.tick()
            dt=(1/self.clock.get_fps() if self.clock.get_fps()>0 else 0)
            frame.screen.fill((0,0,0))
            frame.send_event("render", dt)
            self.pyconsole.draw()
            frame.pygame.display.update()
            events=frame.pygame.event.get()
            frame.send_event("pygame_batch_events", events)
            self.pyconsole.process_input(events)

            for event in events:
                frame.send_event("pygame_event", event)
                if event.type==frame.pygame.KEYDOWN:
                    if event.key==frame.pygame.K_BACKQUOTE:
                        if frame.loader["enable_pyconsole"]:self.pyconsole.set_active()
                if event.type==frame.pygame.QUIT:
                    frame.send_event("shutdown")
                    running=False


    def handle_event_shutdown(self):
        info("Uninitializing PygameCore")
        frame.pygame.quit()
