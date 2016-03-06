from framebase import frame
import logger, framebase
globals().update(logger.build_module_logger(__name__))

@frame.register_this("dphysics")
class DynamicPhysicsManager(framebase.Observer):
    def handle_event_loading_finished(self):
        self.gravity=frame.loader["gravity"]
        self.drag=frame.loader["drag"]

    def get_x_gravity(self):
        return self.get_gravity()[0]

    def get_y_gravity(self):
        return self.get_gravity()[1]

    def get_gravity(self):
        return self.gravity

    def get_drag(self):
        return self.drag
