import json
import os
from pathlib import Path
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid

from models.hero import Hero, HeroImage
from models.age import Age
from models.property import PropertyDefinition, PropertyCategory, PropertyType
from config import load_config, save_config, ensure_directories, AppConfig


class Database:
    def __init__(self, config: Optional[AppConfig] = None):
        self.config = config or load_config()
        ensure_directories(self.config)

        self.heroes: List[Hero] = []
        self.ages: List[Age] = []
        self.property_definitions: List[PropertyDefinition] = []
        self.property_categories: List[PropertyCategory] = []

        self._load_data()
        self._ensure_defaults()

    def _get_data_path(self) -> Path:
        return Path(self.config.data_dir) / "database.json"

    def _get_excel_path(self) -> Path:
        return Path(self.config.data_dir) / self.config.excel_file

    def _load_data(self) -> None:
        data_path = self._get_data_path()
        if data_path.exists():
            try:
                data = json.loads(data_path.read_text())
                self.heroes = [Hero(**h) for h in data.get("heroes", [])]
                self.ages = [Age(**a) for a in data.get("ages", [])]
                self.property_definitions = [PropertyDefinition(**p) for p in data.get("properties", [])]
                self.property_categories = [PropertyCategory(**c) for c in data.get("categories", [])]
            except Exception as e:
                print(f"Error loading database: {e}")

    def _save_data(self) -> None:
        data_path = self._get_data_path()
        data = {
            "heroes": [h.model_dump() for h in self.heroes],
            "ages": [a.model_dump() for a in self.ages],
            "properties": [p.model_dump() for p in self.property_definitions],
            "categories": [c.model_dump() for c in self.property_categories],
        }
        data_path.write_text(json.dumps(data, indent=2))

    def _ensure_defaults(self) -> None:
        if not self.ages:
            default_ages = [
                Age(name="Stone Age", order=0, color="#8B7355"),
                Age(name="Bronze Age", order=1, color="#CD7F32"),
                Age(name="Iron Age", order=2, color="#777777"),
                Age(name="Medieval Age", order=3, color="#8B4513"),
            ]
            self.ages.extend(default_ages)

        if not self.property_categories:
            default_categories = [
                PropertyCategory(name="Basic Stats", order=0),
                PropertyCategory(name="Combat", order=1),
                PropertyCategory(name="Abilities", order=2),
                PropertyCategory(name="Costs", order=3),
            ]
            self.property_categories.extend(default_categories)

        if not self.property_definitions:
            cat_map = {c.name: c.id for c in self.property_categories}
            default_props = [
                PropertyDefinition(name="temple", display_name="Temple", property_type=PropertyType.STRING, category_id=cat_map.get("Basic Stats")),
                PropertyDefinition(name="goddess", display_name="Goddess", property_type=PropertyType.STRING, category_id=cat_map.get("Basic Stats")),
                PropertyDefinition(name="unit_type", display_name="Unit Type", property_type=PropertyType.STRING, category_id=cat_map.get("Basic Stats")),
                PropertyDefinition(name="attack", display_name="Attack", property_type=PropertyType.INTEGER, category_id=cat_map.get("Combat"), default_value=0, min_value=0),
                PropertyDefinition(name="defense", display_name="Defense", property_type=PropertyType.INTEGER, category_id=cat_map.get("Combat"), default_value=0, min_value=0),
                PropertyDefinition(name="health", display_name="Health", property_type=PropertyType.INTEGER, category_id=cat_map.get("Combat"), default_value=100, min_value=1),
                PropertyDefinition(name="speed", display_name="Speed", property_type=PropertyType.FLOAT, category_id=cat_map.get("Combat"), default_value=1.0, min_value=0),
                PropertyDefinition(name="range", display_name="Range", property_type=PropertyType.FLOAT, category_id=cat_map.get("Combat"), default_value=1.0, min_value=0),
                PropertyDefinition(name="armor", display_name="Armor", property_type=PropertyType.INTEGER, category_id=cat_map.get("Combat"), default_value=0, min_value=0),
                PropertyDefinition(name="cost", display_name="Cost", property_type=PropertyType.INTEGER, category_id=cat_map.get("Costs"), default_value=100, min_value=0),
                PropertyDefinition(name="population", display_name="Population", property_type=PropertyType.INTEGER, category_id=cat_map.get("Costs"), default_value=1, min_value=0),
                PropertyDefinition(name="healing_ability", display_name="Healing Ability", property_type=PropertyType.STRING, category_id=cat_map.get("Abilities")),
                PropertyDefinition(name="area_of_effect", display_name="Area of Effect", property_type=PropertyType.FLOAT, category_id=cat_map.get("Abilities"), default_value=0, min_value=0),
                PropertyDefinition(name="mobility", display_name="Mobility", property_type=PropertyType.STRING, category_id=cat_map.get("Abilities")),
                PropertyDefinition(name="special_skills", display_name="Special Skills", property_type=PropertyType.STRING, category_id=cat_map.get("Abilities")),
                PropertyDefinition(name="passive_abilities", display_name="Passive Abilities", property_type=PropertyType.STRING, category_id=cat_map.get("Abilities")),
                PropertyDefinition(name="ultimate_ability", display_name="Ultimate Ability", property_type=PropertyType.STRING, category_id=cat_map.get("Abilities")),
            ]
            self.property_definitions.extend(default_props)

        self._save_data()

    def get_hero(self, hero_id: str) -> Optional[Hero]:
        for hero in self.heroes:
            if hero.id == hero_id:
                return hero
        return None

    def get_heroes_by_age(self, age_id: str) -> List[Hero]:
        return [h for h in self.heroes if h.age_id == age_id]

    def add_hero(self, hero: Hero) -> None:
        self.heroes.append(hero)
        self._save_data()

    def update_hero(self, hero: Hero) -> None:
        for i, h in enumerate(self.heroes):
            if h.id == hero.id:
                self.heroes[i] = hero
                break
        self._save_data()

    def delete_hero(self, hero_id: str) -> None:
        self.heroes = [h for h in self.heroes if h.id != hero_id]
        self._save_data()

    def get_age(self, age_id: str) -> Optional[Age]:
        for age in self.ages:
            if age.id == age_id:
                return age
        return None

    def add_age(self, age: Age) -> None:
        self.ages.append(age)
        self._save_data()

    def update_age(self, age: Age) -> None:
        for i, a in enumerate(self.ages):
            if a.id == age.id:
                self.ages[i] = age
                break
        self._save_data()

    def delete_age(self, age_id: str) -> None:
        self.ages = [a for a in self.ages if a.id != age_id]
        for hero in self.heroes:
            if hero.age_id == age_id:
                hero.age_id = None
        self._save_data()

    def get_ages(self) -> List[Age]:
        return sorted(self.ages, key=lambda a: a.order)

    def get_property(self, prop_id: str) -> Optional[PropertyDefinition]:
        for prop in self.property_definitions:
            if prop.id == prop_id:
                return prop
        return None

    def get_properties_by_category(self, category_id: str) -> List[PropertyDefinition]:
        return [p for p in self.property_definitions if p.category_id == category_id]

    def add_property(self, prop: PropertyDefinition) -> None:
        self.property_definitions.append(prop)
        self._save_data()

    def update_property(self, prop: PropertyDefinition) -> None:
        for i, p in enumerate(self.property_definitions):
            if p.id == prop.id:
                self.property_definitions[i] = prop
                break
        self._save_data()

    def delete_property(self, prop_id: str) -> None:
        self.property_definitions = [p for p in self.property_definitions if p.id != prop_id]
        for hero in self.heroes:
            if prop_id in hero.properties:
                del hero.properties[prop_id]
        self._save_data()

    def get_category(self, cat_id: str) -> Optional[PropertyCategory]:
        for cat in self.property_categories:
            if cat.id == cat_id:
                return cat
        return None

    def add_category(self, cat: PropertyCategory) -> None:
        self.property_categories.append(cat)
        self._save_data()

    def update_category(self, cat: PropertyCategory) -> None:
        for i, c in enumerate(self.property_categories):
            if c.id == cat.id:
                self.property_categories[i] = cat
                break
        self._save_data()

    def delete_category(self, cat_id: str) -> None:
        self.property_categories = [c for c in self.property_categories if c.id != cat_id]
        for prop in self.property_definitions:
            if prop.category_id == cat_id:
                prop.category_id = None
        self._save_data()