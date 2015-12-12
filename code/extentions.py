import os, fnmatch, json, sys, imp, pygame

assets={}
configuration={}
components={}

def findall(dirn, pattern):
	matches=[]
	for root, dirnames, filenames in os.walk(dirn):
		for filename in fnmatch.filter(filenames, pattern):
			matches.append(os.path.join(root, filename))
	return sorted(matches)

def load_config():
	for fn in findall("data", "*.cfg"):
		with open(fn) as fd:
			configuration.update(json.load(fd))

def load_assets():
	for fn in findall("data", "*.png"):
		img=pygame.image.load(fn)
		if not "nocc" in fn:
			img.set_colorkey((255,0,255))
			assets[fn.split(".")[0]]=img.convert_alpha()
		assets[fn.split(".")[0]]=img.convert()


def load_plugins():
	for fn in findall("data", "*.plugin.p[!c]"):
		sys.path.append(os.path.dirname(os.path.realpath(fn)))
		module=imp.load_source("module", fn)
		for funcname in dir(module):
			if funcname.startswith("init_"):
				getattr(module, funcname)()
		sys.path.remove(sys.path[-1])

def register_component(cls):
	components[cls.__name__]=cls