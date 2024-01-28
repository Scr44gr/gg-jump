from arepy.ecs.systems import System

from ..camera import Camera
from ..components import CameraFollow, Transform


class CameraMovementSystem(System):
    def __init__(self) -> None:
        super().__init__()
        self.require_component(Transform)
        self.require_component(CameraFollow)

    def update(self, delta_time: int, camera: Camera):
        for entity in self.get_system_entities():
            transform = entity.get_component(Transform)
            camera_follow = entity.get_component(CameraFollow)

            camera_w = camera.w - camera_follow.offset.x
            camera_h = camera.h - camera_follow.offset.y

            if transform.position.x + (camera_w / 2) <= camera.limit.x:
                camera.position.x = transform.position.x - (camera_w / 2)

            if transform.position.y + (camera_h / 2) <= camera.limit.y:
                camera.position.y = transform.position.y - (camera_h / 2)

            camera.position.x = max(0, camera.position.x)
            camera.position.y = max(0, camera.position.y)

            camera.position.x = min(camera_w, camera.position.x)
            camera.position.y = min(camera_h, camera.position.y)

            camera.position.x = int(camera.position.x)

            camera.position.y = int(camera.position.y)
