
class LevelConfig:
    def __init__(self, name, goal_score, time_limit, spawn_rate, unlocked_recipes):
        self.name = name
        self.goal_score = goal_score
        self.time_limit = time_limit
        self.spawn_rate = spawn_rate
        self.unlocked_recipes = unlocked_recipes

class LevelManager:
    def __init__(self, base):
        self.base = base
        self.levels = [
            LevelConfig("Apprentissage", 200, 120, 15.0, ["Salade de Tomate", "Rondelles d'Oignons"]),
            LevelConfig("Coup de feu", 500, 180, 12.0, ["Salade de Tomate", "Soupe d'Oignon"]),
            LevelConfig("Grillade Party", 800, 180, 10.0, ["Steak Grillé", "Salade de Tomate", "Rondelles d'Oignons"]),
            LevelConfig("Le Grand Mix", 1200, 240, 8.0, ["Meat & Onion", "Soupe d'Oignon", "Ratatouille Express"]),
            LevelConfig("Maître Chef", 2000, 300, 6.0, ["Steak Grillé", "Meat & Onion", "Ratatouille Express", "Tomato Sweet"])
        ]
        self.current_level_idx = 0

    def get_current_level(self):
        return self.levels[self.current_level_idx]

    def next_level(self):
        if self.current_level_idx < len(self.levels) - 1:
            self.current_level_idx += 1
            return True
        return False
