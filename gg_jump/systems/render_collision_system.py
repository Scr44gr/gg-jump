from arepy.ecs.systems import System
from arepy.event_manager.handlers import CollisionEventHandler
from sdl2 import SDL_Rect
from sdl2.ext import Renderer

from ..camera import Camera
from ..components import Collider, Parallax, Transform


class RenderCollisionSystem(System):
    def __init__(self) -> None:
        super().__init__()
        self.require_component(Transform)
        self.require_component(Collider)

    def update(
        self,
        renderer: Renderer,
        collision_event_handler: CollisionEventHandler,
        camera: Camera,
    ):
        for entity in self.get_system_entities():
            transform = entity.get_component(Transform)
            collider = entity.get_component(Collider)

            rect = SDL_Rect(
                w=int(collider.width + collider.offset.x),
                h=int(collider.height + collider.offset.y),
                x=int(transform.position.x - camera.position.x),
                y=int(transform.position.y - camera.position.y),
            )
            is_colliding = collision_event_handler.is_colliding(entity)
            color = (255, 0, 0) if is_colliding else (0, 255, 0)

            renderer.draw_rect(
                rects=rect,
                color=color,
            )
