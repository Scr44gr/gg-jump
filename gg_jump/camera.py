from glm import vec2


class Camera:
    def __init__(self, position: vec2, w: int, h: int, limit: vec2) -> None:
        self.position = position
        self.w = w
        self.h = h
        self.limit = limit
