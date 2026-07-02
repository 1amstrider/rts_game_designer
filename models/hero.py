from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
import uuid
from datetime import datetime


class HeroImage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    hero_id: str
    image_path: str
    is_primary: bool = False
    caption: str = ""
    order: int = 0


class Hero(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    age_id: Optional[str] = None
    description: str = ""
    properties: Dict[str, Any] = {}
    images: List[HeroImage] = []
    created_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now().isoformat())
    tags: List[str] = []

    def get_property(self, prop_id: str, default: Any = None) -> Any:
        return self.properties.get(prop_id, default)

    def set_property(self, prop_id: str, value: Any) -> None:
        self.properties[prop_id] = value

    def get_primary_image(self) -> Optional[HeroImage]:
        for img in self.images:
            if img.is_primary:
                return img
        return self.images[0] if self.images else None