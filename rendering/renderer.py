# rendering/renderer.py
import math

import pygame
from config import Config
from core.game_context import GameContext, GameState
from systems.input_handler import InputHandler

class Renderer:
    def __init__(self, screen: pygame.Surface, font: pygame.font.Font, small_font: pygame.font.Font):
        self.screen = screen
        self.font = font
        self.small_font = small_font

    def render(self, context: GameContext, input_handler: InputHandler, collision_manager):
        self.screen.fill(Config.BLACK)
        self._draw_grid()
        self._draw_shooter_base()
        self._draw_enemies(context)
        self._draw_ball(context)
        self._draw_aiming_helper(context, input_handler)
        self._draw_ui(context)
        # 绘制飘字
        collision_manager.draw_floating_texts(self.screen, self.font)
        pygame.display.flip()

    def _draw_grid(self):
        for x in range(0, Config.SCREEN_WIDTH, 40):
            pygame.draw.line(self.screen, (30, 30, 30), (x, 0), (x, Config.SCREEN_HEIGHT), 1)
        for y in range(0, Config.SCREEN_HEIGHT, 40):
            pygame.draw.line(self.screen, (30, 30, 30), (0, y), (Config.SCREEN_WIDTH, y), 1)

    def _draw_shooter_base(self):
        pos = Config.SHOOTER_POS
        pygame.draw.circle(self.screen, Config.DARK_GRAY, (int(pos.x), int(pos.y)), Config.BALL_RADIUS + 5)
        pygame.draw.circle(self.screen, Config.GRAY, (int(pos.x), int(pos.y)), Config.BALL_RADIUS + 2)

    def _draw_enemies(self, context: GameContext):
        for enemy in context.enemies:
            enemy.draw(self.screen, self.small_font)

    def _draw_ball(self, context: GameContext):
        # 总是绘制球的真实位置（无论瞄准还是弹射）
        context.ball.draw(self.screen)

    def _draw_aiming_helper(self, context: GameContext, input_handler: InputHandler):
        if context.state != GameState.AIMING:
            return
        start, end = input_handler.get_drag_visuals()
        if start is None or end is None:
            return
        drag_vec = end - Config.SHOOTER_POS
        if drag_vec.length() > Config.MAX_DRAG_LEN:
            drag_vec = drag_vec.normalize() * Config.MAX_DRAG_LEN
            limited_end = Config.SHOOTER_POS + drag_vec
        else:
            limited_end = end
        pygame.draw.line(self.screen, (255, 200, 100), Config.SHOOTER_POS, limited_end, 4)
        power = min(drag_vec.length() / Config.MAX_DRAG_LEN, 1.0)
        radius_offset = int(20 * power)
        pygame.draw.circle(self.screen, (255, 220, 150), Config.SHOOTER_POS, Config.BALL_RADIUS + radius_offset, 2)
        power_text = self.font.render(f"Power: {int(power * 100)}%", True, Config.WHITE)
        self.screen.blit(power_text, (Config.SHOOTER_POS.x - 40, Config.SHOOTER_POS.y - 40))

    def _draw_ui(self, context: GameContext):
        # Score
        score_surf = self.font.render(f"Score: {context.score}", True, Config.WHITE)
        self.screen.blit(score_surf, (20, 20))

        # Enemies left
        alive_count = len(context.get_alive_enemies())
        enemy_surf = self.font.render(f"Enemies: {alive_count}", True, Config.WHITE)
        self.screen.blit(enemy_surf, (20, 55))

        # HP bar
        hp_ratio = context.player.hp / context.player.max_hp
        bar_width, bar_height = 200, 20
        x = Config.SCREEN_WIDTH - bar_width - 20
        y = 20
        pygame.draw.rect(self.screen, Config.RED, (x, y, bar_width, bar_height))
        pygame.draw.rect(self.screen, Config.GREEN, (x, y, bar_width * hp_ratio, bar_height))
        hp_text = self.font.render(f"HP: {context.player.hp}/{context.player.max_hp}", True, Config.WHITE)
        self.screen.blit(hp_text, (x, y + bar_height + 5))

        # Turn indicator
        if context.state == GameState.AIMING:
            tip = "DRAG from the BLUE ball → RELEASE to shoot"
        elif context.state == GameState.SHOOTING:
            tip = "SHOOTING... wait for ball to stop"
        else:
            tip = "ENEMY TURN - they are attacking!"
        tip_surf = self.font.render(tip, True, (220, 220, 100))
        self.screen.blit(tip_surf, (Config.SCREEN_WIDTH // 2 - tip_surf.get_width() // 2, Config.SCREEN_HEIGHT - 40))

        # Victory / defeat
        if context.are_all_enemies_dead():
            win_text = self.font.render("VICTORY! Press R to restart", True, Config.YELLOW)
            self.screen.blit(win_text, (Config.SCREEN_WIDTH // 2 - win_text.get_width() // 2, Config.SCREEN_HEIGHT // 2 - 80))
        elif not context.player.is_alive():
            lose_text = self.font.render("GAME OVER - Press R to restart", True, Config.RED)
            self.screen.blit(lose_text, (Config.SCREEN_WIDTH // 2 - lose_text.get_width() // 2, Config.SCREEN_HEIGHT // 2 - 80))

    def _draw_aiming_helper(self, context: GameContext, input_handler: InputHandler):
        if context.state != GameState.AIMING:
            return
        start, end, ball_pos = input_handler.get_drag_info()
        if start is None or end is None:
            return

        # 1. 绘制拉拽线（从球到鼠标）
        pygame.draw.line(self.screen, (255, 200, 100), ball_pos, end, 4)

        # 2. 绘制力度圆环
        drag_vec = end - ball_pos
        power = min(drag_vec.length() / Config.MAX_DRAG_LEN, 1.0)
        radius_offset = int(20 * power)
        pygame.draw.circle(self.screen, (255, 220, 150), ball_pos, Config.BALL_RADIUS + radius_offset, 2)
        power_text = self.font.render(f"Power: {int(power * 100)}%", True, Config.WHITE)
        self.screen.blit(power_text, (ball_pos.x - 40, ball_pos.y - 40))

        # 3. 绘制发射方向直线（从球向前指，长度正比于力度）
        if power > 0:
            direction = (ball_pos - end).normalize()      # 实际发射方向（与拖拽相反）
            length = 30 + power * 80                      # 最短30像素，最长110像素
            tip = ball_pos + direction * length
            pygame.draw.line(self.screen, (100, 200, 255), ball_pos, tip, 3)
            # 在末端画一个箭头三角形
            arrow_angle = math.radians(25)
            left = tip - direction.rotate_rad(arrow_angle) * 10
            right = tip - direction.rotate_rad(-arrow_angle) * 10
            pygame.draw.polygon(self.screen, (100, 200, 255), [tip, left, right])

    def _draw_aiming_helper(self, context: GameContext, input_handler: InputHandler):
        if context.state != GameState.AIMING:
            return
        start, end, ball_pos = input_handler.get_drag_info()
        if start is None or end is None:
            return

        # 1. 绘制拉拽线（从球到鼠标）
        pygame.draw.line(self.screen, (255, 200, 100), ball_pos, end, 4)

        # 2. 绘制力度圆环
        drag_vec = end - ball_pos
        power = min(drag_vec.length() / Config.MAX_DRAG_LEN, 1.0)
        radius_offset = int(20 * power)
        pygame.draw.circle(self.screen, (255, 220, 150), ball_pos, Config.BALL_RADIUS + radius_offset, 2)
        power_text = self.font.render(f"Power: {int(power * 100)}%", True, Config.WHITE)
        self.screen.blit(power_text, (ball_pos.x - 40, ball_pos.y - 40))

        # 3. 绘制发射方向直线（从球向前指，长度正比于力度）
        if power > 0:
            direction = (ball_pos - end).normalize()      # 实际发射方向（与拖拽相反）
            length = 30 + power * 80                      # 最短30像素，最长110像素
            tip = ball_pos + direction * length
            pygame.draw.line(self.screen, (100, 200, 255), ball_pos, tip, 3)
            # 在末端画一个箭头三角形
            arrow_angle = math.radians(25)
            left = tip - direction.rotate_rad(arrow_angle) * 10
            right = tip - direction.rotate_rad(-arrow_angle) * 10
            pygame.draw.polygon(self.screen, (100, 200, 255), [tip, left, right])