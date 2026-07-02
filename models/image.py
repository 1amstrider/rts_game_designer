from pydantic import BaseModel, Field
from typing import Optional
import uuid


class HeroImage(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    hero_id: str
    image_path: str
    is_primary: bool = False
    caption: str = ""
    order: int = 0