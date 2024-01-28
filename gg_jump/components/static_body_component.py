from arepy.ecs.components import Component
from glm import vec2


class StaticBody(Component):
    def __init__(self, position: vec2, rotation: float, scale: vec2) -> None:
        self.position = position
        self.rotation = rotation
        self.scale = scale
