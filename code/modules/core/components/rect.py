from framebase import frame

@frame.entities.register_this_component("rect")
class RectComponent(frame.entities.Component):
    def __init__(self):
        self.rect=frame.pygame.Rect(0,0,0,0)
        self.x=self.y=0
        self.outline=(255,0,0)

    def data_loaded(self):
        self.rect.width=self.width
        self.rect.height=self.height

    def process_raw(self, data):
        self._x, self._y = data.get("x", 0), data.get("y", 0)
        self.rect.top=self._y
        self.rect.left=self._x

    def __getattr__(self, k):
        if k in self.__dict__:
            return object.__getattr__(self, k)
        else:
            return getattr(self.rect, k)

    def x():
        def fget(self):
            return self._x
        def fset(self, value):
            self._x = value
            self.rect.x=value
        return locals()
    x = property(**x())

    def y():
        def fget(self):
            return self._y
        def fset(self, value):
            self._y = value
            self.rect.y=value
        return locals()
    y = property(**y())

    def handle_event_render(self, dt):
        if self.outline:
            frame.pygame.draw.rect(frame.screen, self.outline, self.rect, 2)
