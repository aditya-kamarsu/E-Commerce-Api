from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CreateCategory(BaseModel):
    name: str
    description: str | None = None


class UpdateCategory(BaseModel):
    name: str | None = None
    description: str | None = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str | None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)