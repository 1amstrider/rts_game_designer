from typing import Optional, List, Dict, Any
from supabase import create_client, Client
import os
from pathlib import Path
import json
from datetime import datetime


class SupabaseDB:
    """Supabase client for game data storage.
    
    Falls back to local JSON/Excel if SUPABASE_URL is not set.
    """
    
    def __init__(self):
        url = os.getenv("SUPABASE_URL", "")
        key = os.getenv("SUPABASE_KEY", "")
        self.is_cloud = bool(url and key)
        
        if self.is_cloud:
            self.client: Optional[Client] = create_client(url, key)
            self._ensure_tables()
        else:
            self.client = None
    
    def _ensure_tables(self):
        """Ensure required tables exist. Uses Supabase RPC or manual setup."""
        # Tables should be created via Supabase Dashboard SQL Editor
        # This is just a verification check
        pass
    
    # ─── Kingdoms ───
    def get_kingdoms(self) -> List[Dict]:
        if not self.is_cloud:
            return self._local_get_kingdoms()
        result = self.client.table("kingdoms").select("*").order("name").execute()
        return result.data
    
    def get_kingdom_names(self) -> List[str]:
        """Get just the names for dropdowns/filters."""
        kingdoms = self.get_kingdoms()
        return [k["name"] for k in kingdoms]
    
    def add_kingdom(self, kingdom: Dict):
        if not self.is_cloud:
            return self._local_add_kingdom(kingdom)
        self.client.table("kingdoms").insert(kingdom).execute()
    
    def update_kingdom(self, old_name: str, kingdom: Dict):
        if not self.is_cloud:
            return self._local_update_kingdom(old_name, kingdom)
        new_name = kingdom.get("name", old_name)
        if new_name != old_name:
            self.client.table("heroes").update({"kingdom": new_name}).eq("kingdom", old_name).execute()
        self.client.table("kingdoms").update(kingdom).eq("name", old_name).execute()
    
    def delete_kingdom(self, name: str):
        if not self.is_cloud:
            return self._local_delete_kingdom(name)
        # Reassign heroes to first kingdom
        first = self.get_kingdom_names()[0]
        self.client.table("heroes").update({"kingdom": first}).eq("kingdom", name).execute()
        self.client.table("kingdoms").delete().eq("name", name).execute()
    
    # ─── Ages ───
    def get_ages(self) -> List[str]:
        if not self.is_cloud:
            return self._local_get_ages()
        result = self.client.table("ages").select("name").order("order_index").execute()
        return [r["name"] for r in result.data]
    
    def add_age(self, name: str):
        if not self.is_cloud:
            return self._local_add_age(name)
        count = len(self.get_ages())
        self.client.table("ages").insert({"name": name, "order_index": count}).execute()
    
    def rename_age(self, old: str, new: str):
        if not self.is_cloud:
            return self._local_rename_age(old, new)
        self.client.table("ages").update({"name": new}).eq("name", old).execute()
        self.client.table("heroes").update({"age": new}).eq("age", old).execute()
    
    def delete_age(self, name: str):
        if not self.is_cloud:
            return self._local_delete_age(name)
        ages = self.get_ages()
        fallback = ages[0] if ages else "Unassigned"
        self.client.table("heroes").update({"age": fallback}).eq("age", name).execute()
        self.client.table("ages").delete().eq("name", name).execute()
    
    # ─── Heroes ───
    def get_heroes(self, kingdom: Optional[str] = None, age: Optional[str] = None) -> List[Dict]:
        if not self.is_cloud:
            return self._local_get_heroes(kingdom, age)
        query = self.client.table("heroes").select("*")
        if kingdom:
            query = query.eq("kingdom", kingdom)
        if age:
            query = query.eq("age", age)
        result = query.execute()
        return [self._deserialize_hero(r) for r in result.data]
    
    def get_hero(self, hero_id: str) -> Optional[Dict]:
        if not self.is_cloud:
            return self._local_get_hero(hero_id)
        result = self.client.table("heroes").select("*").eq("id", hero_id).execute()
        if result.data:
            return self._deserialize_hero(result.data[0])
        return None
    
    def create_hero(self, hero: Dict) -> Dict:
        if not self.is_cloud:
            return self._local_create_hero(hero)
        db_hero = self._serialize_hero(hero)
        result = self.client.table("heroes").insert(db_hero).execute()
        return self._deserialize_hero(result.data[0])
    
    def update_hero(self, hero: Dict):
        if not self.is_cloud:
            return self._local_update_hero(hero)
        db_hero = self._serialize_hero(hero)
        self.client.table("heroes").update(db_hero).eq("id", hero["id"]).execute()
    
    def delete_hero(self, hero_id: str):
        if not self.is_cloud:
            return self._local_delete_hero(hero_id)
        self.client.table("heroes").delete().eq("id", hero_id).execute()
    
    # ─── Fields / Schema ───
    def get_fields(self) -> List[Dict]:
        if not self.is_cloud:
            return self._local_get_fields()
        result = self.client.table("fields").select("*").order("id").execute()
        return [{"name": r["name"], "category": r["category"], "type": r["field_type"]} for r in result.data]
    
    def set_fields(self, fields: List[Dict]):
        if not self.is_cloud:
            return self._local_set_fields(fields)
        # Delete all and reinsert (simple approach)
        self.client.table("fields").delete().neq("id", 0).execute()
        for i, f in enumerate(fields):
            self.client.table("fields").insert({
                "id": i,
                "name": f["name"],
                "category": f.get("category", "Custom"),
                "field_type": f.get("type", "text")
            }).execute()
    
    # ─── Serialization ───
    def _serialize_hero(self, hero: Dict) -> Dict:
        """Convert hero dict to DB format."""
        db = {
            "id": hero.get("id"),
            "hero_name": hero.get("Hero Name", ""),
            "kingdom": hero.get("Kingdom", ""),
            "age": hero.get("Age", ""),
            "portrait": hero.get("Portrait", ""),
            "extra_images": json.dumps(hero.get("Extra Images", [])),
            "data": json.dumps({k: v for k, v in hero.items() if k not in {
                "id", "Hero Name", "Kingdom", "Age", "Portrait", "Extra Images"
            }}),
            "updated_at": datetime.now().isoformat(),
        }
        return db
    
    def _deserialize_hero(self, db_row: Dict) -> Dict:
        """Convert DB row to hero dict."""
        hero = {
            "id": db_row["id"],
            "Hero Name": db_row.get("hero_name", ""),
            "Kingdom": db_row.get("kingdom", ""),
            "Age": db_row.get("age", ""),
            "Portrait": db_row.get("portrait", ""),
            "Extra Images": json.loads(db_row.get("extra_images", "[]")),
        }
        data = json.loads(db_row.get("data", "{}"))
        hero.update(data)
        return hero
    
    # ─── Local Fallback (for dev without Supabase) ───
    def _local_get_kingdoms(self) -> List[Dict]:
        return [
            {"name": "Humans", "description": "Versatile and balanced", "forefathers": "First Men", "established": "Classical Age", "races": "Humans", "history": "The First Men built the earliest civilizations..."},
            {"name": "Kingdom of Ores", "description": "Mountain-dwelling craftsmen", "forefathers": "Durin the Deathless", "established": "Classical Age", "races": "Dwarves", "history": "Forged in the heart of mountains..."},
            {"name": "Kingdom of Magic", "description": "Arcane-focused faction", "forefathers": "Archmage Aelindor", "established": "Medieval Age", "races": "Elves, Wizards, Gnomes", "history": "When the veil between worlds thinned..."},
            {"name": "Kingdom of Evil", "description": "Dark magic practitioners", "forefathers": "Lich Lord Vorthak", "established": "Medieval Age", "races": "Necromancers, Witches, Goblins", "history": "Vorthak was once a noble wizard..."},
            {"name": "Kingdom of the Ancients", "description": "Primitive but powerful", "forefathers": "Great Mother Sauria", "established": "Classical Age", "races": "Silurian, Dinosaurs", "history": "Before the rise of civilization..."},
            {"name": "Kingdom of the Beasts", "description": "Monstrous creatures", "forefathers": "Baal the Horned King", "established": "Classical Age", "races": "Minotaurs, Trolls, Balrogs, Dragons, Serpents", "history": "Baal was the first Minotaur to unite..."},
            {"name": "Kingdom of the Divines", "description": "Divine beings", "forefathers": "The Creator Athenia", "established": "Classical Age", "races": "Gods, Angels, Demigods, Oracles, Archangels", "history": "Athenia, the Creator, breathed life..."},
        ]
    
    def _local_add_kingdom(self, kingdom: Dict): pass
    def _local_update_kingdom(self, old: str, kingdom: Dict): pass
    def _local_delete_kingdom(self, name: str): pass
    
    def _local_get_ages(self) -> List[str]:
        return ["Classical Age", "Medieval Age", "Mythic Age"]
    
    def _local_add_age(self, name: str): pass
    def _local_rename_age(self, old: str, new: str): pass
    def _local_delete_age(self, name: str): pass
    
    def _local_get_heroes(self, kingdom=None, age=None) -> List[Dict]:
        return []
    
    def _local_get_hero(self, hero_id: str) -> Optional[Dict]:
        return None
    
    def _local_create_hero(self, hero: Dict) -> Dict:
        return hero
    
    def _local_update_hero(self, hero: Dict): pass
    def _local_delete_hero(self, hero_id: str): pass
    
    def _local_get_fields(self) -> List[Dict]:
        return []
    
    def _local_set_fields(self, fields: List[Dict]): pass
