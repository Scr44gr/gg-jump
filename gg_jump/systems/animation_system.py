from arepy.ecs.systems import System
from sdl2 import SDL_GetTicks64

from ..components import Animation, Sprite


class AnimationSystem(System):
    """System that handles animations."""

    def __init__(self) -> None:
        super().__init__()
        self.require_component(Animation)
        self.require_component(Sprite)

    def update(self, delta_time: float) -> None:
        """Update the animation component of all entities that have one."""
        for entity in self.get_system_entities():
            animation = entity.get_component(Animation)
            sprite = entity.get_component(Sprite)
            current_time = SDL_GetTicks64()
            if animation.start_time == 0:
                animation.start_time = current_time

            animation.current_frame = int(
                (
                    (
                        (current_time - animation.start_time)
                        * animation.frame_speed_rate
                        / 1000
                    )
                    % animation.frame_count
                )
            )
            if not animation.is_playing:
                animation.current_frame = 0

            if not animation.repeat:
                animation.start_time = current_time

            sprite.src_rect.x = animation.current_frame * sprite.width
