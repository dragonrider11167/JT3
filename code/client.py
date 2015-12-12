import game, socket, threading, collections, pygame, extentions, logging, json
module_logger=logging.getLogger("jt3.server")
debug, info, warning, error, critical = module_logger.debug, module_logger.info, module_logger.warning, module_logger.error, module_logger.critical

class ClientGame(game.Game):
	def start_connections(self):
		self.sock=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

	def start_controls_send(self):
		threading.Thread(target=self.send_controls_loop, daemon=True).start()

	def send_controls_loop(self):
		while self.running:
			self.sock.sendto(build_controls().encode("utf-8"), self.addr)

	def update(self, dt):
		to_remove=[]
		for key, entity in self.entities:
			entity.update(dt)
			entity.draw(dt)
			if entity.destroy==True:
				to_remove.append(key)
		for k in to_remove:
			del self.entities[k]

def build_controls():
	return json.dumps({
		"mouse":pygame.mouse.get_pos(),
		"up":pygame.key.get_pressed()[pygame.K_w]
	})