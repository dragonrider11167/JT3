from framebase import frame

@frame.entities.register_this_component("physics")
class PhysicsComponent(frame.entities.Component):
    def __init__(self):
        self.velocity=[0.0,0.0]
        self.solid=False
        self.obeys_gravity=True
        self.static=False
        self.on_ground=0
        self.silly=False

    def handle_event_bound_to_manager(self, name):
        if name=="player":self.silly=True

    @property
    def vel_x(self): return self.velocity[0]

    @property
    def vel_y(self): return self.velocity[1]

    def handle_event_render(self, dt):
        if not self.static:
            self.on_ground-=1
            if self.obeys_gravity:
                self.velocity[0]+=frame.dphysics.get_x_gravity()*dt
                self.velocity[1]+=frame.dphysics.get_y_gravity()*dt
            self.entity.rect.x+=self.vel_x*dt
            self.collide(self.vel_x, 0)
            self.entity.rect.y+=self.vel_y*dt
            self.collide(0, self.vel_y)
            import random
            # if self.silly:frame.entities.add_entity(frame.entities.Entity.from_dict({"rect":{"x":self.entity.rect.x, "y":self.entity.rect.y, "width":2, "height":2},"physics":{"velocity":[random.uniform(-50, 50), random.uniform(-50, 50)]}}))

    def collide(self, xvel, yvel):
        for p in frame.entities.entities.values():
            if "physics" in p.components.keys():
                if p.physics.solid:
                    if self.entity.rect.colliderect(p.rect.rect):
                        if xvel > 0: self.entity.rect.x=p.rect.x-self.entity.rect.width
                        if xvel < 0: self.entity.rect.x=p.rect.x+p.rect.width #self.rect.left = p.rect.right
                        if yvel > 0:
                            self.entity.rect.y=p.rect.y-self.entity.rect.height #self.rect.bottom = p.rect.top
                            self.on_ground = 100
                            self.velocity[1] = 0
                        if yvel < 0:
                            self.velocity[1] = 0
                            self.entity.rect.y = p.rect.y+p.rect.height #self.rect.top = p.rect.bottom
