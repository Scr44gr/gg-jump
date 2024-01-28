from arepy.ecs.components import Component
from glm import vec2


class Grass(Component):
    def __init__(self, friction: vec2) -> None:
        self.friction = friction


class Bounce(Component):
    ...
