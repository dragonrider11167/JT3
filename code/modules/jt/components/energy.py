from framebase import frame
import random

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

@frame.entities.register_this_component("energy")
class EnergyComponent(frame.entities.Component):
    def __init__(self):
        self.amount=0.
        self.max=100
        self.incoming=0

    @property
    def room(self):
        return self.max-self.amount-self.incoming

    def transfer_via_electron(self, target, amount):
        amount=max(0, target.energy.room)
        target.energy.incoming+=amount
        self.amount-=amount
        while amount>0:
            e=frame.loader["electron_prototype"]
            e["rect"]["x"]=self.entity.rect.x+random.uniform(-20,20)
            e["rect"]["y"]=self.entity.rect.y+random.uniform(-20,20)
            e["energy"]["amount"]=min(amount, frame.loader["electron_size"])
            e=frame.entities.add_entity(frame.entities.Entity.from_dict(e))
            e.electron.target=target
            amount-=frame.loader["electron_size"]

    def handle_event_render(self, dt):
        pass#frame.screen.blit(frame.pygame.font.SysFont('mono', 16).render(str(self.amount)+"/"+str(self.max)+" ("+str(self.incoming)+")", 0, (0,0,255)), (self.entity.rect.x, self.entity.rect.y-20))

@frame.entities.register_this_component("electron")
class ElectronComponent(frame.entities.Component):
    def __init__(self):
        self.target=None
        self.speed=0
        self.jiggle=0
        self.max_speed=0

    def handle_event_render(self, dt):
        if self.target.rect.x>self.entity.rect.x:
            self.entity.physics.vel_x+=min(self.speed*dt, self.target.rect.x-self.entity.rect.x)+random.uniform(-self.jiggle*dt,self.jiggle*dt)
        if self.target.rect.x<self.entity.rect.x:
            self.entity.physics.vel_x-=min(self.speed*dt, self.entity.rect.x-self.target.rect.x)+random.uniform(-self.jiggle*dt,self.jiggle*dt)
        if self.target.rect.y>self.entity.rect.y:
            self.entity.physics.vel_y+=min(self.speed*dt, self.target.rect.y-self.entity.rect.y)+random.uniform(-self.jiggle*dt,self.jiggle*dt)
        if self.target.rect.y<self.entity.rect.y:
            self.entity.physics.vel_y-=min(self.speed*dt, self.entity.rect.y-self.target.rect.y)+random.uniform(-self.jiggle*dt,self.jiggle*dt)
        self.entity.physics.vel_x=clamp(self.entity.physics.vel_x, -self.max_speed, self.max_speed)
        self.entity.physics.vel_y=clamp(self.entity.physics.vel_y, -self.max_speed, self.max_speed)
        if self.entity.rect.colliderect(self.target.rect.rect):
            self.entity.kill=1
            self.target.energy.amount+=self.entity.energy.amount
            self.target.energy.incoming-=self.entity.energy.amount
