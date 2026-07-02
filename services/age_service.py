from datetime import datetime
from typing import Optional, List, Dict, Any

from models.hero import Hero
from models.age import Age
from database.database import Database


class AgeService:
    def __init__(self, database: Database):
        self.db = database

    def create_age(self, name: str, description: str = "", order: int = 0, color: str = "#FFFFFF") -> Age:
        age = Age(
            name=name,
            description=description,
            order=order,
            color=color
        )
        self.db.add_age(age)
        return age

    def rename_age(self, age_id: str, new_name: str) -> bool:
        age = self.db.get_age(age_id)
        if not age:
            return False
        age.name = new_name
        self.db.update_age(age)
        return True

    def update_age(self, age_id: str, description: Optional[str] = None,
                   order: Optional[int] = None, color: Optional[str] = None) -> bool:
        age = self.db.get_age(age_id)
        if not age:
            return False

        if description is not None:
            age.description = description
        if order is not None:
            age.order = order
        if color is not None:
            age.color = color

        self.db.update_age(age)
        return True

    def delete_age(self, age_id: str) -> bool:
        age = self.db.get_age(age_id)
        if not age:
            return False

        for hero in self.db.get_heroes_by_age(age_id):
            hero.age_id = None
            self.db.update_hero(hero)

        return self.db.delete_age(age_id)

    def get_age(self, age_id: str) -> Optional[Age]:
        return self.db.get_age(age_id)

    def get_all_ages(self) -> List[Age]:
        return self.db.ages

    def get_heroes_in_age(self, age_id: str) -> List[Hero]:
        return self.db.get_heroes_by_age(age_id)

    def reorder_ages(self, age_ids: List[str]) -> None:
        for i, age_id in enumerate(age_ids):
            age = self.db.get_age(age_id)
            if age:
                age.order = i
                self.db.update_age(age)