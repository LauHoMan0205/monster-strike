# entities/player.py
class Player:
    def __init__(self, max_hp: int):
        self.max_hp = max_hp
        self.hp = max_hp

    def take_damage(self, amount: int) -> int:
        self.hp = max(0, self.hp - amount)
        return amount

    def is_alive(self) -> bool:
        return self.hp > 0

    def reset(self):
        self.hp = self.max_hp