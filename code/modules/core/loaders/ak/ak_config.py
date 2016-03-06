from framebase import frame
import logger, framebase
globals().update(logger.build_module_logger(__name__))

@frame.akloader.register_me("config")
def ak_load_config(data, fp, dir, fn):
    return data["data"]
