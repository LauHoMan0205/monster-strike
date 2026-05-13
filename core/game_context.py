# core/game_context.py
from enum import Enum
import pygame
from config import Config
from entities.ball import Ball
from entities.player import Player
from entities.enemy import Enemy
from utils.helpers import generate_non_overlapping_enemies

class GameState(Enum):
    AIMING = "aiming"
    SHOOTING = "shooting"
    ENEMY_TURN = "enemy_turn"

class GameContext:
    def __init__(self):
        self.ball = Ball()
        self.player = Player(Config.PLAYER_MAX_HP)
        self.enemies: list[Enemy] = []
        self.score = 0
        self.state = GameState.AIMING

    def reset(self):
        self.ball.reset_position()
        self.player.reset()
        self.enemies = generate_non_overlapping_enemies()
        self.score = 0
        self.state = GameState.AIMING

    def get_alive_enemies(self) -> list[Enemy]:
        return [e for e in self.enemies if e.alive]

    def are_all_enemies_dead(self) -> bool:
        return len(self.get_alive_enemies()) == 0

    def is_game_over(self) -> bool:
        return self.are_all_enemies_dead() or not self.player.is_alive()