from framebase import frame
import logger, framebase, random
globals().update(logger.build_module_logger("particles"))

@frame.register_this("particlemanager")
class ParticleManager(framebase.Observer):
    def __init__(self):
        self.particles=[]

    def add_sq_particle(self, x, y, vx, vy, color, size, time):
        s=frame.pygame.Surface(size)
        s.fill(color)
        self.add_particle(x, y, vx, vy, s, time)

    def add_particle(self, x, y, vx, vy, surf, time):
        self.particles.append([x, y, vx, vy, surf, time])

    def add_particles(self, particles):
        self.particles.extend(particles)

    def handle_event_render(self, dt):
        for p in self.particles:
            p[5]-=dt
            frame.screen.blit(p[4], (p[0], p[1]))
            p[0]+=p[2]*dt
            p[1]+=p[3]*dt
            if p[5]<0:
                self.particles.remove(p)

    def add_particles_from_style(self, name, ox, oy):
        s=frame.loader[name]
        for _ in range(0, random.randint(*s["count"])):
            x=ox+random.randint(*s["spawn"])
            y=oy+random.randint(*s["spawn"])
            color=[0,0,0]
            c="rgb"
            for i in range(0, 3):
                color[i]=random.randint(*s[c[i]])
            size=[random.randint(*s["size"]), random.randint(*s["size"])]
            self.add_sq_particle(ox, oy, random.uniform(*s["speed"]), random.uniform(*s["speed"]), color, size, random.uniform(*s["time"]))
