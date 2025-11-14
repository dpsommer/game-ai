import pygame

from gameai import config
from gameai.const import CAT_GAME_GRAVITY, CAT_GAME_TERMINAL_VELOCITY
from gameai.types import Coordinate

from .collision import CollidableObject2D, Collision2D
from .surface import Surface2D


# XXX: functionality should be split into
# a separate side scroller specific subclass
class Character2D(CollidableObject2D):

    def __init__(self, settings: config.CharacterSettings):
        if settings.image is None:
            raise pygame.error("No image configured for character")

        super().__init__(settings)
        self.image_inverted = pygame.transform.flip(self.image, True, False)

        self._velocity = pygame.Vector2()
        self.acceleration_frames = settings.acceleration_frames
        self.speed = settings.speed
        self.jump_speed = settings.jump_speed
        self.standing_on: Surface2D | None = None
        self.jumping = False
        self.inverted = False

    def move(self, keys: pygame.key.ScancodeWrapper):
        x = self._velocity.x
        y = 0

        if not self.standing_on and not self.jumping:
            self.jumping = True

        step = self.speed / self.acceleration_frames
        if self.jumping:
            step /= 6  # limit maneuvering in midair

        if keys[pygame.K_RIGHT]:
            x += step
        if keys[pygame.K_LEFT]:
            x -= step
        if keys[pygame.K_SPACE] and not self.jumping:
            # FIXME: holding DOWN + LEFT/RIGHT + SPACE doesn't jump
            # and actually pauses all movement
            self.jumping = True
            self.standing_on = None
            y = -self.jump_speed
        elif self.jumping:
            y = self._velocity.y + CAT_GAME_GRAVITY

        # by checking x != 0 here we work around the case where e.g. the
        # player is moving left and the right key is pressed, zeroing
        # movement but maintaining the inverted direction for rendering
        if x != 0 and not self.jumping:
            self.inverted = x < 0
            if self.standing_on is not None:
                # use min here so if x < friction we drop x-speed to 0
                friction = min(self.standing_on.friction_coefficient, abs(x))
                friction *= -1 if self.inverted else 1
                x -= friction

        self._velocity.x = pygame.math.clamp(x, -self.speed, self.speed)
        self._velocity.y = min(y, CAT_GAME_TERMINAL_VELOCITY)
        self._move_by(self._velocity)

    def _move_by(self, pos: Coordinate):
        # keep track of the last position for collision handling
        self.last_pos = self.collision_box.rect.topleft
        # move both the image and bounding box rects so we don't need to call
        # get_bounding_rect each frame for collision detection
        self.rect.move_ip(pos)
        self.collision_box.rect.move_ip(pos)

    def handle_collision(self, collision: Collision2D):
        self._move_by((collision.x, collision.y))
        if collision.x != 0:
            self._velocity.x = 0
        if collision.y != 0:
            self._velocity.y = 0
            if collision.y < 0:
                self.jumping = False
        if collision.bottom and isinstance(collision.bottom, Surface2D):
            self.standing_on = collision.bottom

    def update(self, *, screen: pygame.Surface):
        img = self.image_inverted if self.inverted else self.image
        screen.blit(img, self.rect)
