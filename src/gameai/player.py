import dataclasses
import enum

import pygame
import pygame.extensions.dps.core as pgcore
import pygame.extensions.dps.pg2d as pg2d

from . import const


@dataclasses.dataclass
class CharacterSettings(pg2d.SpriteOptions, pg2d.PhysicsObjectSettings):
    max_speed: float = 0
    jump_speed: int = 0
    acceleration_frames = const.DEFAULT_ACCELERATION_FRAMES
    air_manoeuvring_coefficient: float = 0.66


@dataclasses.dataclass
class PlayerSettings(CharacterSettings):
    # action names to map to key bindings
    move_left: str = const.MOVE_LEFT_ACTION
    move_right: str = const.MOVE_RIGHT_ACTION
    jump: str = const.JUMP_ACTION


class PlayerState(enum.Enum):
    IDLE = 0
    RUNNING = 1
    JUMPING = 2
    FALLING = 3


class Player(pg2d.PhysicsObject):

    settings_file: str = const.PLAYER_SETTINGS_FILE
    settings_type = PlayerSettings

    def __init__(self, settings: PlayerSettings):
        self.sprite = pg2d.PlatformerSprite(settings)
        super().__init__(settings, rect=self.sprite.rect)
        self.max_speed = settings.max_speed
        self.jump_speed = settings.jump_speed
        self._air_manoeuvring_coefficient = settings.air_manoeuvring_coefficient
        self._acceleration_frames = settings.acceleration_frames
        # action strings mapped to key bindings
        # XXX: come up with a nicer approach... maybe move these to the observer?
        self.move_left = settings.move_left
        self.move_right = settings.move_right
        self.jump = settings.jump
        self.state: PlayerState = PlayerState.IDLE

    # XXX: dt is applied in PhysicsController, so having it here
    # is potentially confusing & risks it being applied twice;
    # is there a better way to handle this? there may still be
    # cases where we want to have dt in PhysObj update(), so
    # it doesn't make sense to remove it entirely. one option is
    # to not apply it on move but rather on each apply_force call,
    # though this has a lot more potential for error than just
    # using it when applying the velocity vector...
    def update(self, dt: float):
        accel = pygame.Vector2()
        step = self.max_speed / self._acceleration_frames

        if pgcore.key.is_pressed(self.move_left):
            accel.x -= step
        if pgcore.key.is_pressed(self.move_right):
            accel.x += step

        # set player state based on movement
        # FIXME: this is clunky; would be better to have a separate
        # manager for the state machine; async? event-based?
        # need to define state transitions (X -> Y/Z)
        if int(self.velocity.x) == 0 and int(self.velocity.y) == 0:
            self.state = PlayerState.IDLE
        elif int(self.velocity.y) > 0:
            self.state = PlayerState.FALLING
        elif int(self.velocity.x) != 0 and self.state is PlayerState.IDLE:
            self.state = PlayerState.RUNNING

        if self.state in (PlayerState.JUMPING, PlayerState.FALLING):
            # limit manoeuvring in midair
            step *= self._air_manoeuvring_coefficient
        elif pgcore.key.is_pressed(self.jump):
            accel.y = -self.jump_speed
            self.state = PlayerState.JUMPING

        self.apply_force(accel)
        self.velocity.x = pygame.math.clamp(
            self.velocity.x, -self.max_speed, self.max_speed
        )

        # by checking x != 0 here we work around the case where e.g. the
        # player is moving left and the right key is pressed, zeroing
        # movement but maintaining the inverted direction for rendering
        if self.velocity.x != 0:
            self.sprite.inverted = self.velocity.x < 0

    def reset(self):
        super().reset()
        self.sprite.reset()


# TODO: player controller/observer to handle changes in state?
class PlayerObserver:

    def __init__(self):
        pass
