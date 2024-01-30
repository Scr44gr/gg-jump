import logging
from typing import Dict

from arepy.ecs.registry import Registry
from arepy.ecs.systems import System
from arepy.event_manager import EventManager
from arepy.event_manager.events import CollisionEvent
from sdl2 import SDL_FRect, SDL_HasIntersectionF

from ..components import Collider, Interactive, Rigidbody, Transform
from ..components.camera_follow_component import CameraFollow
from ..events.events import RequestInteraction


class CollisionSystem(System):
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        super().__init__()
        self.require_component(Transform)
        self.require_component(Collider)

    def update(self, event_manager: EventManager, registry: Registry):
        self.logger.info("Updating CollisionSystem")
        entities = self.get_system_entities()
        for i in range(len(entities)):
            entity = entities[i]
            transform = entity.get_component(Transform)
            collider = entity.get_component(Collider)

            for j in range(i + 1, len(entities)):
                other_entity = entities[j]
                other_collider = other_entity.get_component(Collider)
                entity_rect = SDL_FRect(
                    w=float(collider.width + collider.offset.x),
                    h=float(collider.height + collider.offset.y),
                    x=float(transform.position.x),
                    y=float(transform.position.y),
                )
                other_entity_rect = SDL_FRect(
                    w=float(other_collider.width + other_collider.offset.x),
                    h=float(other_collider.height + other_collider.offset.y),
                    x=float(other_entity.get_component(Transform).position.x),
                    y=float(other_entity.get_component(Transform).position.y),
                )

                if SDL_HasIntersectionF(entity_rect, other_entity_rect):
                    event_manager.emit(CollisionEvent(entity, other_entity))
                    if entity.has_component(Interactive):
                        event_manager.emit(RequestInteraction(entity, registry))
