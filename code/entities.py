import extentions, json

class Entity(object):
	def __init__(self, game, eid):
		self.eid=eid
		self.components={}
		self.destroy=False
		self.game=game

	def update(self, dt):
		[x.update(dt) for x in self.components]

	def draw(self, dt):
		[x.draw(dt) for x in self.components]

	def add_component(self, prototype):
		instance=extentions.components[prototype["class"]](self)
		instance.__dict__.update(prototype)
		self.components[prototype["class"]]=instance

	def pack_data(self):
		d={"eid":self.eid, "components":{}}
		for k,c in self.components:
			d["components"][k]=c.pack_data()

	def unpack_data(self, data):
		self.eid=data["eid"]
		for k, d in data["components"]:
			self.components[k].unpack_data(d)

class Component(object):
	def __init__(self, parent):
		self.parent=parent
		self.struct=None
		self.initdata()

	def initdata(self):
		pass

	def update(self, dt):
		pass

	def draw(self):
		pass

	def pack_data(self):
		d={}
		for k, v in self.__dict__:
			if type(v) in [str, int, bool, float]:
				d[k]=v
		return d

	def unpack_data(self, data):
		self.__dict__.update(data)