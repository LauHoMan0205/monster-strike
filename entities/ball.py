# entities/ball.py
import pygame
from config import Config
from core.physics_body import PhysicsBody

class Ball(PhysicsBody):
    def __init__(self):
        super().__init__(Config.SHOOTER_POS, Config.BALL_RADIUS, Config.BLUE)

    def reset_position(self):
        self.pos = Config.SHOOTER_POS
        self.vel = pygame.Vector2(0, 0)