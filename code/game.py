import autostruct

class Game(object):
	def __init__(self, connstr):
		self.ip=connstr.split(":")[0]
		self.port=int(connstr.split(":")[1])
		self.addr=(self.ip, self.port)
		self.entities={}
		self.gametime=0
		self.running=True

	def pack_all_entities(self):
		d={"gametime":self.gametime, "entities":{}}
		for k, v in self.entities:
			d["entities"][k]=v.pack_data()

	def load_entity_datagram(self, data):
		self.gametime=data["gametime"]
		for k, d in data["entities"]:
			self.entities[k].unpack_data(d)

	def update(self, dt):
		pass

	def start_connections(self):
		pass

	def stop(self):
		self.running=False