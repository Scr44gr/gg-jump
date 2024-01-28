from arepy.ecs.components import Component
from glm import vec2


class CameraFollow(Component):
    def __init__(self, offset: vec2) -> None:
        self.offset = offset
