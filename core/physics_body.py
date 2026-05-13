# core/physics_body.py
import pygame
from config import Config
from .interfaces import IUpdateable, ICollidable, IDrawable

class PhysicsBody(IUpdateable, ICollidable, IDrawable):
    def __init__(self, pos: pygame.Vector2, radius: float, color: tuple):
        self._pos = pos.copy()
        self.vel = pygame.Vector2(0, 0)
        self._radius = radius
        self.color = color

    @property
    def pos(self) -> pygame.Vector2:
        return self._pos

    @pos.setter
    def pos(self, value: pygame.Vector2):
        self._pos = value.copy()

    @property
    def radius(self) -> float:
        return self._radius

    def update(self, dt: float):
        self.vel *= Config.AIR_FRICTION
        self._pos += self.vel

    def bounce_walls(self) -> bool:
        bounced = False
        if self.pos.x - self.radius <= 0:
            self.pos.x = self.radius
            self.vel.x = -self.vel.x * Config.BOUNCE_DAMP
            bounced = True
        elif self.pos.x + self.radius >= Config.SCREEN_WIDTH:
            self.pos.x = Config.SCREEN_WIDTH - self.radius
            self.vel.x = -self.vel.x * Config.BOUNCE_DAMP
            bounced = True
        if self.pos.y - self.radius <= 0:
            self.pos.y = self.radius
            self.vel.y = -self.vel.y * Config.BOUNCE_DAMP
            bounced = True
        elif self.pos.y + self.radius >= Config.SCREEN_HEIGHT:
            self.pos.y = Config.SCREEN_HEIGHT - self.radius
            self.vel.y = -self.vel.y * Config.BOUNCE_DAMP
            bounced = True
        return bounced

    def is_moving(self) -> bool:
        return self.vel.length() > Config.MIN_SPEED

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)
        highlight = (int(self.pos.x - self.radius // 3), int(self.pos.y - self.radius // 3))
        pygame.draw.circle(surface, Config.WHITE, highlight, self.radius // 4)