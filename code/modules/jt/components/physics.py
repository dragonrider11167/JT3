from framebase import frame

@frame.entities.register_this_component("physics")
class PhysicsComponent(frame.entities.Component):
    def __init__(self):
        self.velocity=[0.0,0.0]
        self.solid=False
        self.obeys_gravity=True
        self.obeys_drag=True
        self.static=False
        self.on_ground=0
        self.silly=False
        self.collides=True

    def handle_event_bound_to_manager(self, name):
        if name=="player":self.silly=True

    def vel_x():
        doc = "The vel_x property."
        def fget(self):
            return self.velocity[0]
        def fset(self, value):
            self.velocity[0] = value
        return locals()
    vel_x = property(**vel_x())

    def vel_y():
        doc = "The vel_y property."
        def fget(self):
            return self.velocity[1]
        def fset(self, value):
            self.velocity[1] = value
        return locals()
    vel_y = property(**vel_y())

    def handle_event_render(self, dt):
        if not self.static:
            self.on_ground-=1
            if self.obeys_gravity:
                self.velocity[0]+=frame.dphysics.get_x_gravity()*dt
                self.velocity[1]+=frame.dphysics.get_y_gravity()*dt
            if self.obeys_drag:
                if self.vel_x>0:
                    self.vel_x=max(self.vel_x-frame.dphysics.get_drag()*dt, 0)
                else:
                    self.vel_x=min(self.vel_x+frame.dphysics.get_drag()*dt, 0)
            self.entity.rect.x+=self.vel_x*dt
            if self.collides:self.collide(self.vel_x, 0)
            self.entity.rect.y+=self.vel_y*dt
            if self.collides:self.collide(0, self.vel_y)
            import random
            #if self.silly:frame.particlemanager.add_sq_particle(self.entity.rect.x, self.entity.rect.y, random.uniform(-5,5), random.uniform(-5,5), (0,255,0), (5,5), 5)

    def collide(self, xvel, yvel):
        for p in frame.entities.entities.values():
            if "physics" in p.components.keys():
                if p.physics.solid and p is not self.entity:
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
