from datetime import datetime
from typing import Optional, List, Dict, Any
import uuid

from models.hero import Hero, HeroImage
from models.age import Age
from models.property import PropertyDefinition, PropertyType
from database.database import Database


class HeroService:
    def __init__(self, database: Database):
        self.db = database

    def create_hero(self, name: str, age_id: Optional[str] = None,
                    description: str = "", properties: Optional[Dict[str, Any]] = None) -> Hero:
        hero = Hero(
            name=name,
            age_id=age_id,
            description=description,
            properties=properties or {},
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat()
        )

        for prop in self.db.property_definitions:
            if prop.id not in hero.properties and prop.default_value != "":
                hero.properties[prop.id] = prop.default_value

        self.db.add_hero(hero)
        return hero

    def duplicate_hero(self, hero_id: str, new_name: Optional[str] = None) -> Optional[Hero]:
        hero = self.db.get_hero(hero_id)
        if not hero:
            return None

        new_hero = Hero(
            name=new_name or f"{hero.name} (Copy)",
            age_id=hero.age_id,
            description=hero.description,
            properties=hero.properties.copy(),
            images=[],
            created_at=datetime.now().isoformat(),
            updated_at=datetime.now().isoformat(),
            tags=hero.tags.copy()
        )

        for img in hero.images:
            new_img = HeroImage(
                hero_id=new_hero.id,
                image_path=img.image_path,
                is_primary=img.is_primary,
                caption=img.caption,
                order=img.order
            )
            new_hero.images.append(new_img)

        self.db.add_hero(new_hero)
        return new_hero

    def delete_hero(self, hero_id: str) -> bool:
        hero = self.db.get_hero(hero_id)
        if not hero:
            return False

        self._delete_hero_images(hero)
        self.db.delete_hero(hero_id)
        return True

    def rename_hero(self, hero_id: str, new_name: str) -> bool:
        hero = self.db.get_hero(hero_id)
        if not hero:
            return False
        hero.name = new_name
        hero.updated_at = datetime.now().isoformat()
        self.db.update_hero(hero)
        return True

    def update_hero_properties(self, hero_id: str, properties: Dict[str, Any]) -> bool:
        hero = self.db.get_hero(hero_id)
        if not hero:
            return False
        hero.properties.update(properties)
        hero.updated_at = datetime.now().isoformat()
        self.db.update_hero(hero)
        return True

    def set_hero_property(self, hero_id: str, prop_id: str, value: Any) -> bool:
        hero = self.db.get_hero(hero_id)
        if not hero:
            return False
        hero.set_property(prop_id, value)
        hero.updated_at = datetime.now().isoformat()
        self.db.update_hero(hero)
        return True

    def move_hero_to_age(self, hero_id: str, age_id: Optional[str]) -> bool:
        hero = self.db.get_hero(hero_id)
        if not hero:
            return False
        hero.age_id = age_id
        hero.updated_at = datetime.now().isoformat()
        self.db.update_hero(hero)
        return True

    def add_hero_image(self, hero_id: str, image_path: str, is_primary: bool = False,
                       caption: str = "") -> Optional[HeroImage]:
        hero = self.db.get_hero(hero_id)
        if not hero:
            return None

        if is_primary:
            for img in hero.images:
                img.is_primary = False

        new_image = HeroImage(
            hero_id=hero_id,
            image_path=image_path,
            is_primary=is_primary,
            caption=caption,
            order=len(hero.images)
        )
        hero.images.append(new_image)
        hero.updated_at = datetime.now().isoformat()
        self.db.update_hero(hero)
        return new_image

    def remove_hero_image(self, hero_id: str, image_id: str) -> bool:
        hero = self.db.get_hero(hero_id)
        if not hero:
            return False

        hero.images = [img for img in hero.images if img.id != image_id]
        hero.updated_at = datetime.now().isoformat()
        self.db.update_hero(hero)
        return True

    def set_primary_image(self, hero_id: str, image_id: str) -> bool:
        hero = self.db.get_hero(hero_id)
        if not hero:
            return False

        for img in hero.images:
            img.is_primary = (img.id == image_id)

        hero.updated_at = datetime.now().isoformat()
        self.db.update_hero(hero)
        return True

    def get_heroes_by_age(self, age_id: str) -> List[Hero]:
        return self.db.get_heroes_by_age(age_id)

    def get_all_heroes(self) -> List[Hero]:
        return self.db.heroes

    def search_heroes(self, query: str, age_id: Optional[str] = None,
                      tags: Optional[List[str]] = None) -> List[Hero]:
        query = query.lower()
        results = []

        for hero in self.db.heroes:
            if age_id and hero.age_id != age_id:
                continue
            if tags and not all(tag in hero.tags for tag in tags):
                continue
            if (query in hero.name.lower() or
                query in hero.description.lower() or
                any(query in str(v).lower() for v in hero.properties.values())):
                results.append(hero)

        return results

    def _delete_hero_images(self, hero: Hero) -> None:
        from config import load_config
        config = load_config()
        from pathlib import Path
        images_dir = Path(config.data_dir) / config.images_dir
        for img in hero.images:
            img_path = images_dir / img.image_path
            if img_path.exists():
                img_path.unlink()