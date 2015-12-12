import entities, extentions

class RenderComponent(entities.Component):
	def initdata(self):
		self.art=""

	def render(self, dt):
		self.parent.game.screen.blit(extentions.assets[self.art], self.parent.components["PositionComponent"].coords)

def init_component():
	extentions.register_component(RenderComponent)