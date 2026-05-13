# systems/input_handler.py
import pygame
from config import Config
from core.game_context import GameContext, GameState

class InputHandler:
    def __init__(self, context: GameContext):
        self.context = context
        self.drag_start = None   # mouse down position
        self.drag_end = None     # current mouse position
        self.is_dragging = False

    def handle_events(self, events) -> bool:
        for event in events:
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                self.context.reset()
                continue

            if self.context.state == GameState.AIMING and not self.context.is_game_over():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.Vector2(event.pos)
                    # Check click on ball (dynamic position)
                    if mouse_pos.distance_to(self.context.ball.pos) <= Config.BALL_RADIUS + 10:
                        self.drag_start = mouse_pos
                        self.drag_end = mouse_pos
                        self.is_dragging = True

                elif event.type == pygame.MOUSEMOTION and self.is_dragging:
                    self.drag_end = pygame.Vector2(event.pos)

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.is_dragging:
                    self._shoot()
                    self.is_dragging = False
                    self.drag_start = None
                    self.drag_end = None
        return True

    def _shoot(self):
        if self.drag_end is None:
            return
        # Shoot direction = from mouse to ball (opposite of drag)
        shoot_vec = self.context.ball.pos - self.drag_end
        if shoot_vec.length() > Config.MAX_DRAG_LEN:
            shoot_vec = shoot_vec.normalize() * Config.MAX_DRAG_LEN
        velocity = shoot_vec * Config.POWER_FACTOR
        if velocity.length() > Config.MAX_SPEED:
            velocity = velocity.normalize() * Config.MAX_SPEED
        if velocity.length() > 0.5:
            self.context.ball.vel = velocity
            self.context.state = GameState.SHOOTING

    def get_drag_info(self):
        """Return (start_pos, end_pos, ball_pos) for drawing."""
        if self.context.state == GameState.AIMING and self.is_dragging and self.drag_end:
            return self.drag_start, self.drag_end, self.context.ball.pos
        return None, None, None