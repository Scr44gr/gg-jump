from ctypes import pointer

from arepy.asset_store import AssetStore
from arepy.ecs.components import Component
from arepy.ecs.registry import Entity
from arepy.ecs.systems import System
from sdl2 import SDL_FLIP_HORIZONTAL, SDL_Rect, SDL_RenderCopyEx
from sdl2.ext import Renderer

from ..camera import Camera
from ..components import CameraFollow, Parallax, Sprite, Transform


class RenderSystem(System):
    def __init__(self) -> None:
        super().__init__()
        self.require_component(Transform)
        self.require_component(Sprite)

    def update(self, renderer: Renderer, asset_store: AssetStore, camera: Camera):
        # RENDER BY Z-INDEX

        class RenderableEntity:
            def __init__(
                self,
                entity: Entity,
                sprite_component: Sprite,
                transform_component: Transform,
            ):
                self.sprite_component = sprite_component
                self.transform_component = transform_component
                self.entity = entity

        renderable_entities = [
            RenderableEntity(
                entity,
                entity.get_component(Sprite),
                entity.get_component(Transform),
            )
            for entity in self.get_system_entities()
        ]

        renderable_entities.sort(key=lambda entity: entity.sprite_component.z_index)

        for renderable_entities in renderable_entities:
            entity = renderable_entities.entity
            transform = renderable_entities.transform_component
            sprite = renderable_entities.sprite_component
            texture = asset_store.get_texture(sprite.asset_id)
            src_rect = sprite.src_rect
            is_parallax = entity.has_component(Parallax)

            if is_parallax:
                parallax = entity.get_component(Parallax)
                transform.position.x *= parallax.speed.x
                transform.position.y *= parallax.speed.y

            dst_rect = SDL_Rect(
                w=int(sprite.width * transform.scale.x),
                h=int(sprite.height * transform.scale.y),
                x=int(transform.position.x - camera.position.x),
                y=int(transform.position.y - camera.position.y),
            )
            flip_x = SDL_FLIP_HORIZONTAL if not sprite.flip_x else 0
            SDL_RenderCopyEx(
                renderer.sdlrenderer,
                texture,
                pointer(src_rect),
                pointer(dst_rect),
                0,  # angle
                None,  # center
                flip_x,  # flip
            )
