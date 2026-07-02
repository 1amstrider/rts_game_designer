from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum
import uuid


class PropertyType(str, Enum):
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    ENUM = "enum"


class PropertyCategory(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str = ""
    order: int = 0
    is_collapsed: bool = False


class PropertyDefinition(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    display_name: str = ""
    description: str = ""
    property_type: PropertyType = PropertyType.STRING
    category_id: Optional[str] = None
    default_value: Any = ""
    enum_values: List[str] = []
    is_required: bool = False
    is_visible: bool = True
    order: int = 0
    min_value: Optional[float] = None
    max_value: Optional[float] = None

    def get_display_name(self) -> str:
        return self.display_name or self.name