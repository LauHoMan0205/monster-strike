# core/__init__.py
from .interfaces import IUpdateable, IDrawable, ICollidable
from .physics_body import PhysicsBody
from .physics_world import PhysicsWorld
from .game_context import GameContext, GameState