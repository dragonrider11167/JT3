from framebase import frame
import logger, framebase
globals().update(logger.build_module_logger(__name__))

@frame.register_this("controls_provider")
class ControlsProvider(framebase.Observer):
    def __init__(self):
        debug("ControlsProvider loading")

    def handle_event_pygame_event(self, e):
        player=frame.entities.entities["player"]
        pygame=frame.pygame
        if frame.statemanager.current=="game":
            if e.type==pygame.KEYDOWN:
                if e.key==pygame.K_SPACE:
                    if player.physics.on_ground>0:
                        player.physics.velocity[1]=-frame.loader["player_jump_speed"]
                if e.key==pygame.K_a:
                    player.physics.velocity[0]=-frame.loader["player_run_speed"]
                if e.key==pygame.K_d:
                    player.physics.velocity[0]=frame.loader["player_run_speed"]
