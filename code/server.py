import game, socket, threading, collections, pygame, extentions, logging, json
module_logger=logging.getLogger("jt3.server")
debug, info, warning, error, critical = module_logger.debug, module_logger.info, module_logger.warning, module_logger.error, module_logger.critical

class ServerGame(game.Game):
	def start_connections(self):
		self.clientcontrollers=collections.OrderedDict()
		self.sock=socket.socket(socket.AF_INET, # Internet
			socket.SOCK_DGRAM) # UDP
		self.sock.bind((self.ip, self.port))
		threading.Thread(target=self.handle_connections, daemon=True).start()
		threading.Thread(target=self.handle_send, daemon=True).start()

	def run_in_background(self):
		threading.Thread(target=self.update_loop, daemon=True).start()

	def handle_connections(self):
		while self.running:
			data, addr = self.sock.recvfrom(1024)
			data=data.decode("utf-8")
			if addr not in self.clientcontrollers:
				debug("New client connected: "+str(addr))
				self.clientcontrollers[addr]=ClientHandler(self, addr)
			self.clientcontrollers[addr].handle_controlsframe(data)

	def handle_send(self):
		clock=pygame.time.Clock()
		while self.running:
			client=0
			while client<len(self.clientcontrollers.values()):
				list(self.clientcontrollers.values())[client].send_update_packet()
				clock.tick(extentions.configuration["server_send_rate"]/len(self.clientcontrollers.values()))
				client+=1

	def update_loop(self):
		clock=pygame.time.Clock()
		while self.running:
			clock.tick(extentions.configuration["server_physics_rate"])
			self.update((1/clock.get_fps()) if clock.get_fps()!=0 else 0)

	def update(self, dt):
		to_remove=[]
		for key, entity in self.entities:
			entity.update(dt)
			if entity.destroy==True:
				to_remove.append(key)
		for k in to_remove:
			del self.entities[k]

class ClientHandler(object):
	def __init__(self, server, addr):
		self.addr=addr
		self.server=server
		self.sending_update_lock=threading.Lock()

	def handle_controlsframe(self, frame):
		data=json.loads(frame)
		if data["up"]:
			print("Up")

	def send_update_packet(self):
		for k, v in self.server.entities:
			self.server.sock.sendto(self.server.pack_all_entities().encode("utf-8"), self.addr)