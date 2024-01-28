import logging

from arepy.ecs.systems import System
from arepy.event_manager import EventManager
from arepy.event_manager.handlers import CollisionEventHandler

from ..components import Collider, Gravity, Rigidbody


class PhysicsSystem(System):
    logger = logging.getLogger(__name__)

    def __init__(self) -> None:
        super().__init__()
        self.require_component(Rigidbody)
        self.require_component(Collider)
        self.require_component(Gravity)

    # apply gravity
    def update(self, delta_time: int, collision_handler: CollisionEventHandler):
        for entity in self.get_system_entities():
            velocity = entity.get_component(Rigidbody).velocity
            gravity = entity.get_component(Gravity).gravity
            if not collision_handler.is_colliding(entity):
                velocity.y += gravity * delta_time
            else:
                velocity.y = 0.0
