from arepy.ecs.systems import System
from arepy.event_manager import EventManager
from glm import vec2

from ..components import Collider, Interactive, Sprite, TextLabel, Transform
from ..events.events import RequestInteraction


class InteractiveSystem(System):
    def __init__(self) -> None:
        super().__init__()
        self.require_component(Interactive)

    def update(self, event_manager: EventManager):
        event_manager.subscribe(RequestInteraction, self.on_request_interaction)

    def on_request_interaction(self, event: RequestInteraction):
        entity_a = event.entity
        registry = event.registry
        interactive_component = entity_a.get_component(Interactive)
        if interactive_component.is_interacting:
            entity_a.remove_component(Collider)
            return

        interactive_component.is_interacting = True
        entity = registry.create_entity()
        position = entity_a.get_component(Transform).position
        registry.add_component(
            entity,
            TextLabel,
            text="Go up!",
            position=vec2(position.x, position.y - 20),
            color=(255, 255, 255),
            font_id="default-mid",
            size=16,
            is_fixed=True,
            draw=True,
        )
        registry.add_component(
            entity,
            Sprite,
            src_rect=(0, 0, 141, 32),
            width=141,
            height=32,
            asset_id="text-bubble",
            z_index=5,
        )
        registry.add_component(
            entity,
            Transform,
            position=vec2(position.x - 32, position.y - 32),
            scale=vec2(1, 1),
            rotation=0,
        )
