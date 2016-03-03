from framebase import frame

@frame.entities.register_this_component("renderer")
class SimpleRenderComponent(frame.entities.Component):
    def handle_event_render(self, dt):
        frame.screen.blit(frame.loader[self.image], self.entity.position.xy)
