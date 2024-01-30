# TODO: Fix this weird import
from arepy.ecs.registry import Entity, Registry
from arepy.event_manager.event_manager import Event


class JumpStartEvent(Event):
    def __init__(
        self,
        entity: Entity,
        start_time: float,
    ) -> None:
        super().__init__()
        self.entity = entity
        self.start_time = start_time

    def __repr__(self) -> str:
        return f"JumpEvent(entity={self.entity})"


class JumpEndEvent(Event):
    def __init__(self, entity: Entity, delta_time: float) -> None:
        super().__init__()
        self.entity = entity
        self.delta_time = delta_time

    def __repr__(self) -> str:
        return f"JumpEvent(entity={self.entity})"


class RequestInteraction(Event):
    def __init__(self, entity: Entity, registry: Registry) -> None:
        super().__init__()
        self.entity = entity
        self.registry = registry

    def __repr__(self) -> str:
        return f"RequestInteraction(entity={self.entity})"
