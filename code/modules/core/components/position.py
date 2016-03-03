from framebase import frame

@frame.entities.register_this_component("position")
class PositionComponent(frame.entities.Component):
    def __init__(self):
        self.x=self.y=self.vel_x=self.vel_y=0

    @property
    def xy(self):
        return (self.x, self.y)

    def handle_event_render(self, dt):
        self.x+=self.vel_x*dt
        self.y+=self.vel_y*dt
