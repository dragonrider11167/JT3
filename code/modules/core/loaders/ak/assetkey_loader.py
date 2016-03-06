from framebase import frame
import logger, framebase, json
globals().update(logger.build_module_logger("akloader"))

@frame.register_this("akloader")
class AssetKeyLoader:
    def __init__(self):
        self.types={}

    def register_loader(self, key, func):
        self.types[key]=func

    def __call__(self, fullpath, directory, filename):
        with open(fullpath, 'r') as fd:
            data=json.load(fd)
            i=0
            for element in data["assets"]:
                if element["type"] not in self.types.keys():
                    raise AttributeError("Postponing load of ak until '"+element["type"]+"' loader defined")
            for element in data["assets"]:
                debug("Applying loader for "+element["type"]+" to node "+str(i)+" in "+fullpath)
                frame.loader.assets[element["name"]]=self.types[element["type"]](self._replace_ldir(element, directory), fullpath, directory, filename)
                i+=1

    def register_me(self, key):
        def _register_me(func):
            self.register_loader(key, func)
        return _register_me

    def _replace_ldir(self, element, directory):
        new={}
        for k, v in element.items():
            new[k]=v.replace("$LDIR", directory+'/') if type(v) is str else v
        return new

frame.loader.add_load_method(".ak", frame.akloader)
frame.loader.add_load_method(".assetkey", frame.akloader)
