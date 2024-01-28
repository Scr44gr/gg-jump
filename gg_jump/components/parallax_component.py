from arepy.ecs.components import Component
from glm import vec2


class Parallax(Component):
    def __init__(self, speed: vec2) -> None:
        self.speed = speed
