# systems/turn_manager.py
from core.game_context import GameContext, GameState
from systems.collision_manager import CollisionManager

class TurnManager:
    def __init__(self, context: GameContext, collision_manager: CollisionManager):
        self.context = context
        self.collision_manager = collision_manager

    def update(self, dt: float):
        if self.context.is_game_over():
            return

        self.collision_manager.update_floating_texts()

        if self.context.state == GameState.SHOOTING:
            # 子步长防止高速穿透
            self._update_ball_with_substeps(dt)
            self.collision_manager.process_ball_enemy_collisions()

            if not self.context.ball.is_moving():
                self.context.state = GameState.ENEMY_TURN

        elif self.context.state == GameState.ENEMY_TURN:
            self._execute_enemy_turn()
            # 重要：球**不**复位，停留在停止位置
            self.context.state = GameState.AIMING

    def _update_ball_with_substeps(self, dt: float):
        speed = self.context.ball.vel.length()
        steps = max(2, int(speed / 4.0) + 1)   # 速度越高步数越多
        step_dt = dt / steps
        for _ in range(steps):
            self.context.ball.update(step_dt)
            self.context.ball.bounce_walls()
            self.collision_manager.process_ball_enemy_collisions()

    def _execute_enemy_turn(self):
        total_damage = 0
        for enemy in self.context.enemies:
            if not enemy.alive:
                continue
            if enemy.update_countdown():
                total_damage += enemy.attack_damage
        self.context.player.take_damage(total_damage)