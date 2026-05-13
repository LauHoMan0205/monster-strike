# main.py
import pygame
import sys
from config import Config
from core.game_context import GameContext
from core.physics_world import PhysicsWorld
from systems.collision_manager import CollisionManager
from systems.turn_manager import TurnManager
from systems.input_handler import InputHandler
from rendering.renderer import Renderer

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT))
    pygame.display.set_caption("Monster Strike Lite - SOLID Refactor")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("microsoftyahei", 24, bold=True)
    small_font = pygame.font.SysFont("microsoftyahei", 18)

    context = GameContext()
    context.reset()

    physics_world = PhysicsWorld()
    physics_world.add_body(context.ball)
    for enemy in context.enemies:
        physics_world.add_body(enemy)

    collision_manager = CollisionManager(context, physics_world)
    turn_manager = TurnManager(context, collision_manager)
    input_handler = InputHandler(context)
    renderer = Renderer(screen, font, small_font)

    running = True
    # main.py 中的主循环部分
    while running:
        events = pygame.event.get()
        running = input_handler.handle_events(events)
        if running:
            dt = 1.0 / Config.FPS
            turn_manager.update(dt)
            renderer.render(context, input_handler, collision_manager)   # 新增参数
        clock.tick(Config.FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()