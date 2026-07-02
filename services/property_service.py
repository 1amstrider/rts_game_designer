from typing import Optional, List, Dict, Any
from datetime import datetime

from models.property import PropertyDefinition, PropertyCategory, PropertyType
from database.database import Database


class PropertyService:
    def __init__(self, database: Database):
        self.db = database

    def create_property(self, name: str, display_name: str = "",
                       property_type: PropertyType = PropertyType.STRING,
                       category_id: Optional[str] = None, default_value: Any = "",
                       description: str = "", enum_values: Optional[List[str]] = None,
                       is_required: bool = False, is_visible: bool = True,
                       order: int = 0, min_value: Optional[float] = None,
                       max_value: Optional[float] = None) -> PropertyDefinition:

        prop = PropertyDefinition(
            name=name,
            display_name=display_name or name,
            property_type=property_type,
            category_id=category_id,
            default_value=default_value,
            description=description,
            enum_values=enum_values or [],
            is_required=is_required,
            is_visible=is_visible,
            order=order,
            min_value=min_value,
            max_value=max_value
        )

        self.db.add_property(prop)
        return prop

    def rename_property(self, prop_id: str, new_name: str) -> bool:
        prop = self.db.get_property(prop_id)
        if not prop:
            return False
        prop.name = new_name
        self.db.update_property(prop)
        return True

    def update_property(self, prop_id: str, **kwargs) -> bool:
        prop = self.db.get_property(prop_id)
        if not prop:
            return False

        for key, value in kwargs.items():
            if hasattr(prop, key) and value is not None:
                setattr(prop, key, value)

        self.db.update_property(prop)
        return True

    def delete_property(self, prop_id: str, remove_from_heroes: bool = True) -> bool:
        if remove_from_heroes:
            for hero in self.db.heroes:
                if prop_id in hero.properties:
                    del hero.properties[prop_id]
                    self.db.update_hero(hero)

        return self.db.delete_property(prop_id)

    def get_property(self, prop_id: str) -> Optional[PropertyDefinition]:
        return self.db.get_property(prop_id)

    def get_all_properties(self) -> List[PropertyDefinition]:
        return self.db.property_definitions

    def get_properties_by_category(self, category_id: str) -> List[PropertyDefinition]:
        return self.db.get_properties_by_category(category_id)

    def get_properties_grouped_by_category(self) -> Dict[str, List[PropertyDefinition]]:
        result = {}
        for cat in self.db.property_categories:
            props = self.db.get_properties_by_category(cat.id)
            if props:
                result[cat.id] = props
        return result

    def reorder_properties(self, prop_ids: List[str]) -> None:
        for i, prop_id in enumerate(prop_ids):
            prop = self.db.get_property(prop_id)
            if prop:
                prop.order = i
                self.db.update_property(prop)

    def get_default_properties(self) -> List[PropertyDefinition]:
        defaults = [
            {"name": "temple", "display_name": "Temple", "property_type": PropertyType.STRING, "order": 0},
            {"name": "goddess", "display_name": "Goddess", "property_type": PropertyType.STRING, "order": 1},
            {"name": "unit_type", "display_name": "Unit Type", "property_type": PropertyType.STRING, "order": 2},
            {"name": "attack", "display_name": "Attack", "property_type": PropertyType.INTEGER, "default_value": 0, "min_value": 0, "order": 0},
            {"name": "defense", "display_name": "Defense", "property_type": PropertyType.INTEGER, "default_value": 0, "min_value": 0, "order": 1},
            {"name": "health", "display_name": "Health", "property_type": PropertyType.INTEGER, "default_value": 100, "min_value": 1, "order": 2},
            {"name": "speed", "display_name": "Speed", "property_type": PropertyType.FLOAT, "default_value": 1.0, "min_value": 0, "order": 3},
            {"name": "range", "display_name": "Range", "property_type": PropertyType.FLOAT, "default_value": 1.0, "min_value": 0, "order": 4},
            {"name": "armor", "display_name": "Armor", "property_type": PropertyType.INTEGER, "default_value": 0, "min_value": 0, "order": 5},
            {"name": "cost", "display_name": "Cost", "property_type": PropertyType.INTEGER, "default_value": 100, "min_value": 0, "order": 0},
            {"name": "population", "display_name": "Population", "property_type": PropertyType.INTEGER, "default_value": 1, "min_value": 0, "order": 1},
            {"name": "healing_ability", "display_name": "Healing Ability", "property_type": PropertyType.STRING, "order": 0},
            {"name": "area_of_effect", "display_name": "Area of Effect", "property_type": PropertyType.FLOAT, "default_value": 0, "min_value": 0, "order": 1},
            {"name": "mobility", "display_name": "Mobility", "property_type": PropertyType.STRING, "order": 2},
            {"name": "special_skills", "display_name": "Special Skills", "property_type": PropertyType.STRING, "order": 3},
            {"name": "passive_abilities", "display_name": "Passive Abilities", "property_type": PropertyType.STRING, "order": 4},
            {"name": "ultimate_ability", "display_name": "Ultimate Ability", "property_type": PropertyType.STRING, "order": 5},
        ]

        existing_names = {p.name for p in self.db.property_definitions}
        created = []

        cat_map = {c.name: c.id for c in self.db.property_categories}

        for prop_data in defaults:
            if prop_data["name"] not in existing_names:
                category = "Basic Stats" if prop_data.get("order", 0) < 3 else \
                           "Combat" if prop_data.get("order", 0) < 6 else \
                           "Costs" if prop_data.get("order", 0) < 2 else "Abilities"
                prop = self.create_property(
                    category_id=cat_map.get(category),
                    **prop_data
                )
                created.append(prop)

        return created

    def validate_value(self, prop: PropertyDefinition, value: Any) -> bool:
        if prop.property_type == PropertyType.INTEGER:
            try:
                int(value)
            except (ValueError, TypeError):
                return False
            if prop.min_value is not None and int(value) < prop.min_value:
                return False
            if prop.max_value is not None and int(value) > prop.max_value:
                return False
        elif prop.property_type == PropertyType.FLOAT:
            try:
                float(value)
            except (ValueError, TypeError):
                return False
            if prop.min_value is not None and float(value) < prop.min_value:
                return False
            if prop.max_value is not None and float(value) > prop.max_value:
                return False
        elif prop.property_type == PropertyType.BOOLEAN:
            if not isinstance(value, bool) and value not in ["true", "false", "1", "0", True, False]:
                return False
        elif prop.property_type == PropertyType.ENUM:
            if value not in prop.enum_values:
                return False

        return True

    def convert_value(self, prop: PropertyDefinition, value: Any) -> Any:
        if prop.property_type == PropertyType.INTEGER:
            try:
                return int(value)
            except (ValueError, TypeError):
                return prop.default_value
        elif prop.property_type == PropertyType.FLOAT:
            try:
                return float(value)
            except (ValueError, TypeError):
                return prop.default_value
        elif prop.property_type == PropertyType.BOOLEAN:
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                return value.lower() in ["true", "1", "yes"]
            return bool(value)
        return value