import server, client, pygame, extentions, sys, logging
logging.basicConfig(filemode='w', filename='jt3.log',level=logging.DEBUG, format='%(relativeCreated)-6d [%(name)-20s] %(levelname)-8s: %(message)s')


extentions.load_config()
extentions.load_plugins()

if True in ["server" in x for x in sys.argv]:
	servergame=server.ServerGame("0.0.0.0:2244")
	servergame.start_connections()
	servergame.run_in_background()
	if "saserver" in sys.argv:
		while 1:pass

pygame.init()
screen=pygame.display.set_mode((100,100))
extentions.load_assets()

clientgame=client.ClientGame("localhost:2244")
clientgame.screen=screen
clientgame.start_connections()
clientgame.start_controls_send()

run=1
while run:
	for e in pygame.event.get():
		if e.type==pygame.QUIT:
			run=0
	pygame.display.flip()