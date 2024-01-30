from typing import Tuple

from arepy import Arepy
from arepy.event_manager.events import CollisionEvent
from arepy.event_manager.handlers import CollisionEventHandler
from glm import vec2

from .camera import Camera
from .components import (Animation, CameraFollow, Collider, Gravity,
                         Interactive, KeyboardControlled, Parallax, Rigidbody,
                         Sprite, Transform)
from .components.text_label_component import TextLabel
from .systems import (AnimationSystem, CameraMovementSystem, CollisionSystem,
                      InteractiveSystem, MovementSystem, PhysicsSystem,
                      PlayerMovementSystem, RenderCollisionSystem,
                      RenderSystem, RenderTextSystem)


class GGJumpGame(Arepy):
    title: str = "GG Jump"
    screen_width: int = 340
    screen_height: int = 240
    screen_size: Tuple[int, int] = (800, 600)
    fake_fullscreen: bool = True
    debug: bool = False
    max_frame_rate: int = 60
    # 32x32
    # Logical size

    def load_assets(self) -> None:
        asset_store = self.get_asset_store()
        asset_store.load_texture(
            self.renderer, "player", "./assets/sprites/gege-sprite-sheet.png"
        )
        asset_store.load_texture(self.renderer, "ground", "./assets/tiles/ground.png")
        asset_store.load_texture(
            self.renderer, "background", "./assets/tiles/background-back.png"
        )
        asset_store.load_texture(self.renderer, "npc", "./assets/sprites/npc-sheet.png")
        asset_store.load_texture(
            self.renderer, "forest-background", "./assets/tiles/background-loop.png"
        )
        asset_store.load_texture(
            self.renderer, "text-bubble", "./assets/sprites/text-bubble.png"
        )
        # Load Fonts
        asset_store.load_font("default", "./assets/fonts/charriot.ttf", 16)
        asset_store.load_font("default-mid", "./assets/fonts/charriot.ttf", 8)

    def create_camera(self) -> None:
        self.camera = Camera(
            position=vec2(0, 0),
            w=self.screen_width,
            h=self.screen_height * 2,
            limit=vec2(350, 1000),
        )

    def create_background(self) -> None:
        entity_builder = self.create_entity()
        entity_builder.with_component(
            Transform(
                position=vec2(0, self.screen_height),
                rotation=0,
                scale=vec2(2, 2),
            )
        )
        entity_builder.with_component(
            Sprite(
                width=350,
                height=1000,
                asset_id="background",
                src_rect=(0, 0),
                z_index=-1,
            )
        )
        entity_builder.with_component(
            Parallax(
                speed=vec2(0.1, 0.1),
            )
        )
        entity_builder.build()

    def create_forest_background(self) -> None:
        entity_builder = self.create_entity()
        entity_builder.with_component(
            Transform(
                position=vec2(0, self.screen_height),
                rotation=0,
                scale=vec2(2, 2),
            )
        )
        entity_builder.with_component(
            Sprite(
                width=350,
                height=1000,
                asset_id="forest-background",
                src_rect=(0, 0),
                z_index=-1,
            )
        )
        entity_builder.with_component(
            Parallax(
                speed=vec2(0.1, 0.1),
            )
        )
        entity_builder.build()

    def create_player(self) -> None:
        entity_builder = self.create_entity()
        entity_builder.with_component(
            Transform(
                position=vec2(0, 0),
                rotation=0,
                scale=vec2(1, 1),
            )
        )
        entity_builder.with_component(
            Sprite(
                width=32,
                height=32,
                asset_id="player",
                src_rect=(0, 32 * 3),  # Idle
                z_index=1,
            )
        )
        entity_builder.with_component(
            Animation(
                current_frame=0,
                frame_count=2,
                frame_speed_rate=5,
                is_playing=True,
                repeat=True,
                start_time=0,
            )
        )
        entity_builder.with_component(
            Rigidbody(
                velocity=vec2(0, 0),
                acceleration=vec2(0, 0),
                friction=vec2(0, 0),
            )
        )
        entity_builder.with_component(
            Collider(
                offset=vec2(0, 0),
                width=32,
                height=32,
                is_colliding=False,
            )
        )
        entity_builder.with_component(
            KeyboardControlled(left_velocity=vec2(-70, 0), right_velocity=vec2(70, 0))
        )
        entity_builder.with_component(
            Gravity(
                gravity=150,
            )
        )
        entity_builder.with_component(
            CameraFollow(offset=vec2(self.screen_width // 2, self.screen_height // 2))
        )
        entity_builder.build()

    def create_text_score(self) -> None:
        entity_builder = self.create_entity()
        entity_builder.with_component(
            Transform(
                position=vec2(0, 0),
                rotation=0,
                scale=vec2(1, 1),
            )
        )
        entity_builder.with_component(
            TextLabel(
                text="Score: 0",
                font_id="default",
                size=16,
                color=(255, 255, 255),
                position=(int(self.screen_width / 2) - 32, 0),
                is_fixed=False,
            )
        )
        entity_builder.build()

    def create_npc(self) -> None:
        """Spawn a knight npc"""
        entity_builder = self.create_entity()
        entity_builder.with_component(
            Transform(
                position=vec2(self.screen_width - 32, self.screen_height - 64),
                rotation=0,
                scale=vec2(1, 1),
            )
        )
        entity_builder.with_component(
            Sprite(
                width=32,
                height=32,
                asset_id="npc",
                src_rect=(0, 0),
                z_index=1,
            )
        )
        entity_builder.with_component(Interactive(is_interacting=False))
        entity_builder.with_component(
            Animation(
                current_frame=0,
                frame_count=2,
                frame_speed_rate=4,
                is_playing=True,
                repeat=True,
                start_time=0,
            )
        )
        entity_builder.with_component(
            Rigidbody(
                velocity=vec2(0, 0),
                acceleration=vec2(0, 0),
                friction=vec2(0, 0),
            )
        )
        entity_builder.with_component(
            Collider(
                offset=vec2(1, 1),
                width=32,
                height=32,
                is_colliding=False,
            )
        )

        entity_builder.build()

    def create_ground(self, position: vec2 = vec2(0, 0)) -> None:
        entity_builder = self.create_entity()
        entity_builder.with_component(
            Transform(
                position=position,
                rotation=0,
                scale=vec2(1, 1),
            )
        )
        entity_builder.with_component(
            Sprite(
                width=32 * 3,
                height=32,
                asset_id="ground",
                src_rect=(0, 0),
                z_index=0,
            )
        )

        entity_builder.with_component(
            Collider(
                offset=vec2(0, 0),
                width=32 * 3,
                height=32,
                is_colliding=False,
            )
        )

        entity_builder.build()

    def create_level(self) -> None:
        self.create_background()
        self.create_forest_background()
        for i in range(0, 10):
            self.create_ground(vec2(i * 32 * 3, self.screen_height - 32))

        self.create_npc()

    def setup_event_handlers(self) -> None:
        event_manager = self.get_event_manager()
        self.collision_event_handler = CollisionEventHandler()
        event_manager.subscribe(
            CollisionEvent, self.collision_event_handler.on_collision
        )

    def setup(self):
        # Initialize engine
        self.init()
        # Setup event handlers
        self.setup_event_handlers()
        # Load assets
        self.load_assets()
        self.create_text_score()
        # Create player
        self.create_camera()
        self.create_level()
        self.create_player()
        # Add systems
        self.add_system(RenderSystem)
        self.add_system(PlayerMovementSystem)
        self.add_system(AnimationSystem)
        self.add_system(MovementSystem)
        self.add_system(CollisionSystem)
        self.add_system(PhysicsSystem)
        self.add_system(RenderCollisionSystem)
        self.add_system(CameraMovementSystem)
        self.add_system(RenderTextSystem)
        self.add_system(InteractiveSystem)

    # Game loop events
    def on_update(self) -> None:
        self.get_system(CameraMovementSystem).update(self.delta_time, self.camera)
        self.get_system(CollisionSystem).update(
            self.get_event_manager(), self._registry
        )
        self.get_system(PhysicsSystem).update(
            self.delta_time, self.collision_event_handler
        )
        self.get_system(PlayerMovementSystem).update(
            self.delta_time,
            self.get_keyboard_event_handler(),
            self.get_event_manager(),
            self.collision_event_handler,
        )
        self.get_system(MovementSystem).update(self.delta_time)
        self.get_system(AnimationSystem).update(self.delta_time)
        self.get_system(InteractiveSystem).update(self.get_event_manager())
        # reset event_handlers
        self.setup_event_handlers()

    def on_render(self) -> None:
        self.get_system(RenderSystem).update(
            self.renderer, self.get_asset_store(), self.camera
        )

        self.get_system(RenderTextSystem).update(
            self.renderer, self.get_asset_store(), self.camera
        )
        if self.debug:
            self.get_system(RenderCollisionSystem).update(
                self.renderer, self.collision_event_handler, self.camera
            )

    def on_startup(self) -> None:
        pass

    def on_shutdown(self) -> None:
        pass
