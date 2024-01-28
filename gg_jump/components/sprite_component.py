from typing import Tuple

from arepy.ecs.components import Component
from sdl2 import SDL_Rect


class Sprite(Component):
    def __init__(
        self,
        width: int,
        height: int,
        asset_id: str,
        src_rect: Tuple[int, int] = (0, 0),
        z_index: int = 0,
        flip_x: bool = False,
        flip_y: bool = False,
    ) -> None:
        self.width = width
        self.height = height
        self.asset_id = asset_id
        self.src_rect = SDL_Rect(
            w=width,
            h=height,
            x=src_rect[0],
            y=src_rect[1],
        )
        self.z_index = z_index
        self.flip_x = flip_x
        self.flip_y = flip_y
