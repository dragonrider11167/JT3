from framebase import frame
import json

def load_image(fullpath, directory, filename):
    image=pygame.image.load(fullpath)
    if "png" in filename:
        image=image.convert_alpha()
    return image

[frame.loader.add_load_method(ext, load_image) for ext in [
    ".simple.png",
    ".simple.gif",
    ".simple.jpg",
    ".simple.jpeg"
]]
