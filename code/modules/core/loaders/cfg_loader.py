from framebase import frame
import json

def load_cfg(fullpath, directory, filename):
    with open(fullpath, 'r') as fd:
        frame.loader.assets.update(json.load(fd))

frame.loader.add_load_method(".cfg", load_cfg)
