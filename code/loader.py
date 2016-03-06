import os, logger, framebase, imp, collections
globals().update(logger.build_module_logger(__name__))

POISON_NAMES=["__pycache__", ".pyc", ".nfs"]

class RequiredModulesNotLoaded(Exception):pass
class AbortModuleLoad(Exception):pass

class Loader:
    def __init__(self):
        self.load_methods={
            ".py":[self.load_plugin]
        }
        self.assets={}
        self._selected=[]

    def require_modules(self, *a):
        for item in a:
            if item not in framebase.frame.modules.keys(): raise RequiredModulesNotLoaded()

    def abort_module_load(self, err=""):
        raise AbortModuleLoad(err)

    def require_library(self, *ls):
        for l in ls:
            try: __import__(l)
            except ImportError:
                exception("Couldn't load "+l)
                raise AbortModuleLoad(l+" not availible")

    def add_load_method(self, ext, func):
        if ext not in self.load_methods.keys():
            self.load_methods[ext]=[]
        self.load_methods[ext].append(func)

    def __getitem__(self, name):
        return self.assets[name]

    def load_plugin(self, fullpath, directory, filename):
        with open(fullpath) as f:
            mangled_name="x_"+filename.replace(".py","")
            imp.load_source(mangled_name, fullpath)

    def load_file(self, fname):
        debug("Loading file '"+fname+"'")
        loaders=[]
        for extention in self.load_methods.keys():
            if fname.endswith(extention):
                debug("  (Under rule '"+extention+"')")
                loaders.extend(self.load_methods[extention])
        for loader in loaders:
            loader(fname, *os.path.split(fname))

    def add_directory(self, directory):
        for name in POISON_NAMES:
            if name in directory:
                return
        debug("Selecting from directory '"+directory+"'")
        for fn in os.listdir(directory):
            joined=os.path.join(directory, fn)
            if os.path.isdir(joined):
                self.add_directory(joined)
            else:
                self._selected.append(joined)

    def load_selected(self):
        debug("Loading...")
        to_load=list(collections.OrderedDict.fromkeys(self._selected)) #remove duplicates
        last_attempt=None
        while to_load:
            debug("Loading attempt start. List = "+str(to_load))
            next_to_load=[]
            for item in to_load:
                try:
                    self.load_file(item)
                except BaseException as e:
                    if not (isinstance(e, RequiredModulesNotLoaded) or isinstance(e, AbortModuleLoad)): exception("Encountered error loading "+str(item)+":"+str(e))
                    else:debug("Delaying load until module requirements satasfied")
                    if not isinstance(e, AbortModuleLoad):
                        next_to_load.append(item)
                    else:info("Module load aborted: "+str(e))
            if next_to_load==last_attempt:
                warning("Loop detected, aborting load. to_load = "+str(to_load))
                break
            to_load=next_to_load
            last_attempt=to_load
        info("Loading Finished")
        framebase.frame.send_event("loading_finished")
