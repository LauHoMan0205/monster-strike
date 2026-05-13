# core/interfaces.py
from abc import ABC, abstractmethod
import pygame

class IUpdateable(ABC):
    @abstractmethod
    def update(self, dt: float):
        pass

class IDrawable(ABC):
    @abstractmethod
    def draw(self, surface: pygame.Surface):
        pass

class ICollidable(ABC):
    @property
    @abstractmethod
    def pos(self) -> pygame.Vector2:
        pass

    @property
    @abstractmethod
    def radius(self) -> float:
        pass