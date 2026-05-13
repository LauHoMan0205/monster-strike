# utils/helpers.py
import random
import pygame
from config import Config
from entities.enemy import Enemy

def generate_non_overlapping_enemies() -> list[Enemy]:
    enemies = []
    for _ in range(Config.ENEMY_COUNT):
        for _ in range(200):
            x = random.randint(Config.ENEMY_RADIUS + 20, Config.SCREEN_WIDTH - Config.ENEMY_RADIUS - 20)
            y = random.randint(Config.ENEMY_RADIUS + 50, Config.SCREEN_HEIGHT - Config.ENEMY_RADIUS - 50)
            pos = pygame.Vector2(x, y)
            # Avoid overlapping with shooter position
            if pos.distance_to(Config.SHOOTER_POS) < Config.ENEMY_RADIUS + Config.BALL_RADIUS + 30:
                continue
            # Avoid overlapping with existing enemies
            overlap = any(pos.distance_to(e.pos) < Config.ENEMY_RADIUS * 2 for e in enemies)
            if not overlap:
                color = random.choice(Config.ENEMY_COLORS)
                enemies.append(Enemy(pos, color))
                break
    return enemies