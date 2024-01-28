from arepy.ecs.systems import System
from arepy.event_manager import EventManager
from arepy.event_manager.handlers.collision_event_handler import CollisionEventHandler
from arepy.event_manager.handlers.keyboard_event_handler import KeyboardEventHandler
from glm import vec2
from sdl2 import SDL_GetTicks64

from ..components import Animation, Collider, KeyboardControlled, Rigidbody, Sprite
from ..events import JumpEndEvent, JumpStartEvent


class PlayerMovementSystem(System):
    def __init__(self) -> None:
        super().__init__()
        self.require_component(Sprite)
        self.require_component(Rigidbody)
        self.require_component(KeyboardControlled)
        self.require_component(Animation)
        self.jump_start_time = 0

    def update(
        self,
        delta_time: float,
        keyboard_handler: KeyboardEventHandler,
        event_manager: EventManager,
        collision_handler: CollisionEventHandler,
    ):
        event_manager.subscribe(JumpStartEvent, self.on_jump_start)
        event_manager.subscribe(JumpEndEvent, self.on_jump_end)

        for entity in self.get_system_entities():
            rigidbody = entity.get_component(Rigidbody)
            keyboard_controlled = entity.get_component(KeyboardControlled)
            sprite = entity.get_component(Sprite)

            if not entity.has_component(Collider):
                return
            is_colliding = collision_handler.is_colliding(entity)
            animation = entity.get_component(Animation)

            is_a_key_pressed = keyboard_handler.is_key_pressed("a")
            is_d_key_pressed = keyboard_handler.is_key_pressed("d")
            is_space_pressed = keyboard_handler.is_key_pressed("space")
            is_space_released = keyboard_handler.is_key_released("space")
            if not is_colliding:
                # Falling
                sprite.src_rect.y = 3 * sprite.height
                animation.repeat = False
            if (
                is_space_pressed
                and is_colliding
                and not is_a_key_pressed
                and not is_d_key_pressed
            ):
                event_manager.emit(JumpStartEvent(entity, SDL_GetTicks64()))
                return

            if is_space_released and is_colliding:
                self.is_jumping = True
                event_manager.emit(JumpEndEvent(entity, delta_time))
                return

            if is_a_key_pressed and is_colliding:
                rigidbody.velocity = vec2(
                    keyboard_controlled.left_velocity.x, rigidbody.velocity.y
                )
                # Walking left
                sprite.src_rect.y = 0 * sprite.height
                animation.repeat = True
                sprite.flip_x = True

            elif is_d_key_pressed and is_colliding:
                rigidbody.velocity = vec2(
                    keyboard_controlled.right_velocity.x, rigidbody.velocity.y
                )
                # Walking right
                sprite.src_rect.y = 0 * sprite.height
                animation.repeat = True
                sprite.flip_x = False

            if not is_a_key_pressed and not is_d_key_pressed and is_colliding:
                rigidbody.velocity = vec2(0, rigidbody.velocity.y)
                # Idle
                sprite.src_rect.y = 1 * sprite.height
                animation.repeat = True

    def on_jump_start(self, event: JumpStartEvent):
        entity = event.entity
        keyboard_controlled = entity.get_component(KeyboardControlled)
        keyboard_controlled.jump_force += keyboard_controlled.jump_factor

    def on_jump_end(self, event: JumpEndEvent):
        entity = event.entity
        keyboard_controlled = entity.get_component(KeyboardControlled)
        rigidbody = entity.get_component(Rigidbody)
        rigidbody.velocity.y -= (
            keyboard_controlled.jump_force * keyboard_controlled.jump_speed
        ) % 150

        keyboard_controlled.jump_force = 2.0
