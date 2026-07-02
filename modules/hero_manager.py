class HeroManager:
    def __init__(self):
        self.heroes = []

    def add_hero(self, hero_data: dict):
        self.heroes.append(hero_data)
        return hero_data
