from framebase import frame
import logger, framebase, pygame
globals().update(logger.build_module_logger(__name__))

@frame.akloader.register_me("image")
def ak_load_image(data, fp, dir, fn):
    debug("Loading "+data["path"]+" with ak_load_image")
    image=pygame.image.load(data["path"])
    if data.get("convert_alpha", False):
        image=image.convert_alpha()
    return image
