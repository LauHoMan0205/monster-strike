# core/physics_world.py
import pygame
from .interfaces import ICollidable
from .physics_body import PhysicsBody

class PhysicsWorld:
    def __init__(self):
        self.bodies: list[PhysicsBody] = []

    def add_body(self, body: PhysicsBody):
        self.bodies.append(body)

    def remove_body(self, body: PhysicsBody):
        if body in self.bodies:
            self.bodies.remove(body)

    def update(self, dt: float):
        for body in self.bodies:
            body.update(dt)
            body.bounce_walls()

    def check_collision(self, a: ICollidable, b: ICollidable) -> bool:
        return a.pos.distance_to(b.pos) < a.radius + b.radius

    def resolve_collision(self, a: PhysicsBody, b: PhysicsBody):
        """Elastic collision with equal mass and restitution."""
        if a == b:
            return
        normal = (a.pos - b.pos).normalize()
        rel_vel = a.vel - b.vel
        vel_along = rel_vel.dot(normal)
        if vel_along > 0:
            return
        restitution = 0.8
        impulse = (1 + restitution) * vel_along / 2
        a.vel -= impulse * normal
        b.vel += impulse * normal
        # separation to avoid sticking
        overlap = a.radius + b.radius - a.pos.distance_to(b.pos)
        if overlap > 0:
            correction = normal * (overlap / 2)
            a.pos += correction
            b.pos -= correction

    def resolve_ball_enemy_collision(self, ball: PhysicsBody, enemy: PhysicsBody):
        """弹性碰撞，敌人视为静态（质量和速度很大），保留更多能量"""
        normal = (ball.pos - enemy.pos).normalize()
        rel_vel = ball.vel
        vel_along = rel_vel.dot(normal)
        if vel_along > 0:
            return
        restitution = 0.9            # 提高弹性，反弹更快
        impulse = (1 + restitution) * vel_along
        ball.vel -= impulse * normal
        # 分开避免粘连
        overlap = ball.radius + enemy.radius - ball.pos.distance_to(enemy.pos)
        if overlap > 0:
            ball.pos += normal * overlap