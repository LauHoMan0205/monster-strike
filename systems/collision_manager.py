# systems/collision_manager.py
import random
import pygame
from config import Config
from core.game_context import GameContext
from core.physics_world import PhysicsWorld

class CollisionManager:
    def __init__(self, context: GameContext, physics_world: PhysicsWorld):
        self.context = context
        self.physics_world = physics_world
        self.floating_texts = []

    def process_ball_enemy_collisions(self) -> int:
        hit_count = 0
        for enemy in self.context.enemies:
            if not enemy.alive:
                continue
            if self.physics_world.check_collision(self.context.ball, enemy):
                # 物理反弹
                self.physics_world.resolve_ball_enemy_collision(self.context.ball, enemy)

                # 判断弱点命中（使用弹珠中心）
                ball_center = self.context.ball.pos
                is_critical = enemy.is_weakpoint_hit(ball_center, self.context.ball.radius)

                damage = self._calculate_damage(self.context.ball, enemy)
                if is_critical:
                    crit_mult = getattr(Config, 'CRITICAL_MULTIPLIER', 1.5)
                    damage = int(damage * crit_mult)

                died = enemy.take_damage(damage)
                if died:
                    hit_count += 1
                    self.context.score += 10

                self._add_floating_text(str(damage), enemy.pos, is_critical)
        return hit_count

    def _calculate_damage(self, ball, enemy) -> int:
        base = getattr(Config, 'BASE_DAMAGE', 10)
        speed_factor = getattr(Config, 'DAMAGE_SPEED_FACTOR', 0.8)
        speed = ball.vel.length()
        return max(1, int(base + speed * speed_factor))

    def _add_floating_text(self, text: str, pos: pygame.Vector2, is_critical: bool):
        color = Config.YELLOW if is_critical else Config.WHITE
        self.floating_texts.append({
            "text": text,
            "pos": pygame.Vector2(pos.x, pos.y - 20),
            "life": 30,
            "color": color
        })

    def update_floating_texts(self):
        for ft in self.floating_texts[:]:
            ft["life"] -= 1
            ft["pos"].y -= 0.5
            if ft["life"] <= 0:
                self.floating_texts.remove(ft)

    def draw_floating_texts(self, surface: pygame.Surface, font: pygame.font.Font):
        for ft in self.floating_texts:
            surf = font.render(ft["text"], True, ft["color"])
            surface.blit(surf, (int(ft["pos"].x - surf.get_width()//2), int(ft["pos"].y)))