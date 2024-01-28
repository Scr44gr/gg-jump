from arepy.ecs.components import Component


class Gravity(Component):
    def __init__(self, gravity: float) -> None:
        self.gravity = gravity
