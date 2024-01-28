from arepy.ecs.components import Component
from glm import vec2


class Rigidbody(Component):
    def __init__(self, velocity: vec2, acceleration: vec2, friction: vec2) -> None:
        self.velocity = velocity
        self.acceleration = acceleration
        self.friction = friction
