# config.py
import pygame

class Config:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    FPS = 60

    # Colors
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 50, 50)
    BLUE = (50, 100, 255)
    GREEN = (50, 255, 50)
    YELLOW = (255, 255, 50)
    GRAY = (100, 100, 100)
    DARK_GRAY = (50, 50, 50)

    # Ball physics
    BALL_RADIUS = 12
    AIR_FRICTION = 0.995
    BOUNCE_DAMP = 0.98
    MIN_SPEED = 1.0
    POWER_FACTOR = 0.12
    MAX_DRAG_LEN = 100
    MAX_SPEED = 8.0

    # Shooter
    SHOOTER_POS = pygame.Vector2(150, SCREEN_HEIGHT - 150)

    # Damage
    BASE_DAMAGE = 10
    DAMAGE_SPEED_FACTOR = 0.8
    CRITICAL_RATE = 0.1
    CRITICAL_MULTIPLIER = 1.5

    # Enemies
    ENEMY_RADIUS = 18
    ENEMY_COUNT = 6
    ENEMY_COLORS = [RED, (200, 100, 50), (180, 50, 180), (50, 200, 150), (200, 180, 50)]
    ENEMY_BASE_DAMAGE = 15
    ENEMY_BASE_COOLDOWN = 3
    WEAKPOINT_RADIUS = 10   

    # Player
    PLAYER_MAX_HP = 100