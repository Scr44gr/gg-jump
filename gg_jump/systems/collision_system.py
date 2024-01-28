import logging
from typing import Dict

from arepy.ecs.systems import System
from arepy.event_manager import EventManager
from arepy.event_manager.events import CollisionEvent
from sdl2 import SDL_HasIntersection, SDL_Rect

from ..components import Collider, Rigidbody, Transform
from ..components.camera_follow_component import CameraFollow


class CollisionSystem(System):
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        super().__init__()
        self.require_component(Transform)
        self.require_component(Collider)

    def update(self, event_manager: EventManager):
        self.logger.info("Updating CollisionSystem")
        entities = self.get_system_entities()
        for i in range(len(entities)):
            entity = entities[i]
            transform = entity.get_component(Transform)
            collider = entity.get_component(Collider)

            for j in range(i + 1, len(entities)):
                other_entity = entities[j]
                other_collider = other_entity.get_component(Collider)
                entity_rect = SDL_Rect(
                    w=int(collider.width + collider.offset.x),
                    h=int(collider.height + collider.offset.y),
                    x=int(transform.position.x),
                    y=int(transform.position.y),
                )
                other_entity_rect = SDL_Rect(
                    w=int(other_collider.width + other_collider.offset.x),
                    h=int(other_collider.height + other_collider.offset.y),
                    x=int(other_entity.get_component(Transform).position.x),
                    y=int(other_entity.get_component(Transform).position.y),
                )

                if SDL_HasIntersection(entity_rect, other_entity_rect):
                    event_manager.emit(CollisionEvent(entity, other_entity))
