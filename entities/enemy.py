# entities/enemy.py
import random
import pygame
from enum import Enum
from config import Config
from core.physics_body import PhysicsBody

class WeakDirection(Enum):
    NORTH = 0
    SOUTH = 1
    WEST = 2
    EAST = 3

class Enemy(PhysicsBody):
    def __init__(self, pos: pygame.Vector2, color: tuple):
        super().__init__(pos, Config.ENEMY_RADIUS, color)
        self.alive = True
        self.max_hp = 30
        self.hp = self.max_hp
        self.countdown = random.randint(1, Config.ENEMY_BASE_COOLDOWN)
        self.attack_damage = Config.ENEMY_BASE_DAMAGE
        self.attack_animation_timer = 0
        self.weak_direction = random.choice(list(WeakDirection))
        # 弱点中心位置（在敌人圆周上）
        self.weakpoint_center = self._calculate_weakpoint_center()

    def _calculate_weakpoint_center(self) -> pygame.Vector2:
        """根据弱点方向计算弱点圆的中心坐标（在敌人圆周上）"""
        if self.weak_direction == WeakDirection.NORTH:
            offset = pygame.Vector2(0, -self.radius)
        elif self.weak_direction == WeakDirection.SOUTH:
            offset = pygame.Vector2(0, self.radius)
        elif self.weak_direction == WeakDirection.WEST:
            offset = pygame.Vector2(-self.radius, 0)
        else:  # EAST
            offset = pygame.Vector2(self.radius, 0)
        return self.pos + offset

    def update_weakpoint_center(self):
        """当敌人移动时（如果有），更新弱点中心位置"""
        self.weakpoint_center = self._calculate_weakpoint_center()

    def is_weakpoint_hit(self, ball_center: pygame.Vector2, ball_radius: float) -> bool:
        """检测弹珠碰撞圆与弱点圆是否有重叠"""
        distance = ball_center.distance_to(self.weakpoint_center)
        return distance <= ball_radius + Config.WEAKPOINT_RADIUS

    def update_countdown(self) -> bool:
        if not self.alive:
            return False
        self.countdown -= 1
        if self.countdown <= 0:
            self.countdown = Config.ENEMY_BASE_COOLDOWN
            self.attack_animation_timer = 10
            return True
        return False

    def take_damage(self, damage: int) -> bool:
        if not self.alive:
            return False
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def draw(self, surface: pygame.Surface, font: pygame.font.Font):
        if not self.alive:
            return
        super().draw(surface)

        # 眼睛
        eye_offset = self.radius // 3
        left_eye = (int(self.pos.x - eye_offset), int(self.pos.y - eye_offset))
        right_eye = (int(self.pos.x + eye_offset), int(self.pos.y - eye_offset))
        pygame.draw.circle(surface, Config.WHITE, left_eye, self.radius // 4)
        pygame.draw.circle(surface, Config.WHITE, right_eye, self.radius // 4)
        pygame.draw.circle(surface, Config.BLACK, left_eye, self.radius // 8)
        pygame.draw.circle(surface, Config.BLACK, right_eye, self.radius // 8)

        # 倒计时
        text = font.render(str(self.countdown), True, Config.WHITE)
        text_rect = text.get_rect(center=(int(self.pos.x), int(self.pos.y - self.radius - 5)))
        surface.blit(text, text_rect)

        # 血条
        bar_width = self.radius * 2
        bar_height = 4
        bar_x = int(self.pos.x - self.radius)
        bar_y = int(self.pos.y + self.radius + 2)
        hp_ratio = self.hp / self.max_hp
        pygame.draw.rect(surface, Config.RED, (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, Config.GREEN, (bar_x, bar_y, bar_width * hp_ratio, bar_height))

        # 绘制弱点圆形（半透明黄色 + 边框）
        weak_surf = pygame.Surface((Config.WEAKPOINT_RADIUS * 2, Config.WEAKPOINT_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(weak_surf, (255, 255, 0, 128), (Config.WEAKPOINT_RADIUS, Config.WEAKPOINT_RADIUS), Config.WEAKPOINT_RADIUS)
        pygame.draw.circle(weak_surf, (255, 200, 0, 255), (Config.WEAKPOINT_RADIUS, Config.WEAKPOINT_RADIUS), Config.WEAKPOINT_RADIUS, 2)
        surface.blit(weak_surf, (int(self.weakpoint_center.x - Config.WEAKPOINT_RADIUS), int(self.weakpoint_center.y - Config.WEAKPOINT_RADIUS)))

        # 攻击动画
        if self.attack_animation_timer > 0:
            alpha = self.attack_animation_timer / 10
            radius_extra = int(5 * alpha)
            pygame.draw.circle(surface, (255, 0, 0, int(255 * alpha)),
                               (int(self.pos.x), int(self.pos.y)),
                               self.radius + radius_extra, 3)
            exclaim = font.render("!", True, (255, 200, 0))
            ex_rect = exclaim.get_rect(center=(int(self.pos.x), int(self.pos.y - self.radius - 15)))
            surface.blit(exclaim, ex_rect)
            self.attack_animation_timer -= 1

    # 可选：重写 pos setter 以自动更新弱点中心
    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        self._pos = value.copy()
        self.update_weakpoint_center()