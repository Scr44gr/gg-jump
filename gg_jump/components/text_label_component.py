from typing import Tuple

from arepy.ecs.components import Component


class TextLabel(Component):
    def __init__(
        self,
        text: str,
        font_id: str,
        size: int,
        position: Tuple[int, int],
        color: Tuple[int, int, int],
        is_fixed: bool = False,
        draw: bool = True,
    ) -> None:
        self.text = text
        self.font_id = font_id
        self.size = size
        self.color = color
        self.position = position
        self.is_fixed = is_fixed
        self.draw = draw
