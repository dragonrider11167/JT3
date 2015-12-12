import entities, extentions

class PositionComponent(entities.Component):
	def initdata(self):
		self.x=self.y=self.vel_x=self.vel_y=0

	def update(self, dt):
		self.x+=self.vel_x*dt
		self.y+=self.vel_y*dt

	@property
	def coords(self):
		return (self.x, self.y)

def init_component():
	extentions.register_component(PositionComponent)