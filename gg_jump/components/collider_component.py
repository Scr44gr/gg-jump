from arepy.ecs.components import Component
from glm import vec2


class Collider(Component):
    def __init__(
        self,
        width: int,
        height: int,
        offset: vec2 = vec2(0, 0),
        is_colliding: bool = False,
    ):
        self.width = width
        self.height = height
        self.offset = offset
        self.is_colliding = is_colliding
