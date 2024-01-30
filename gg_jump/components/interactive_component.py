from arepy.ecs.components import Component


class Interactive(Component):
    def __init__(self, is_interacting: bool) -> None:
        self.is_interacting = is_interacting
