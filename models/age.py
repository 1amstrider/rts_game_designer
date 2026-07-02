from pydantic import BaseModel, Field
from typing import Optional
import uuid


class Age(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str = ""
    order: int = 0
    color: str = "#FFFFFF"
    is_active: bool = True