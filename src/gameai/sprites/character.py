import pygame

from gameai.config import CharacterSettings
from gameai.types import Coordinate

from .collision import CollidableObject2D, Collision2D


# XXX: functionality should be split into
# a separate side scroller specific subclass
class Character2D(CollidableObject2D):

    def __init__(self, settings: CharacterSettings):
        self._velocity = pygame.Vector2()
        self.speed = settings.speed
        self.jump_speed = settings.jump_speed
        # while these are "constant" in real physics, it's simpler to define them
        # per object/character than to implement mass & air resistance
        self.gravity = settings.gravity
        self.terminal_velocity = settings.terminal_velocity
        self.jumping = False
        self.inverted = False

        if settings.image is None:
            raise pygame.error("No image configured for character")
        super().__init__(settings)
        self.image_inverted = pygame.transform.flip(self.image, True, False)

    def move(self, keys: pygame.key.ScancodeWrapper):
        # modify the velocity vector in the direction of movement
        # if left and right keys are pressed, they should 0 out
        # jumping should have a high initial upward speed that rounds out (slerp?)
        x = 0
        y = 0

        if keys[pygame.K_RIGHT]:
            x += self.speed
        if keys[pygame.K_LEFT]:
            x -= self.speed
        if keys[pygame.K_SPACE] and not self.jumping:
            # FIXME: holding DOWN + LEFT/RIGHT + SPACE doesn't jump
            # and actually pauses all movement
            self.jumping = True
            y = -self.jump_speed
        elif self.jumping:
            # TODO: also trigger if the character is in midair
            y = self._velocity.y + self.gravity
            x /= 1.33  # XXX: slightly finer control while jumping

        # by checking x != 0 here we work around the case where e.g. the player
        # is moving left and the right key is pressed, zeroing movement but
        # maintaining the inverted direction for rendering
        if x != 0:
            self.inverted = x < 0

        self._velocity.x = x
        self._velocity.y = min(y, self.terminal_velocity)
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

    def update(self, *, screen: pygame.Surface):
        img = self.image_inverted if self.inverted else self.image
        screen.blit(img, self.rect)
