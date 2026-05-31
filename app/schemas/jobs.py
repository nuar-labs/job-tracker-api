from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class JobCreate(BaseModel):
    company: str = Field(min_length=1, max_length=255)
    role: str = Field(min_length=1, max_length=255)
    link: Optional[str] = Field(default=None, max_length=500)
    status: str = Field(default="applied", max_length=50)
    notes: Optional[str] = None


class JobUpdate(BaseModel):
    company: Optional[str] = Field(default=None, max_length=255)
    role: Optional[str] = Field(default=None, max_length=255)
    link: Optional[str] = Field(default=None, max_length=500)
    status: Optional[str] = Field(default=None, max_length=50)
    notes: Optional[str] = None


class JobPublic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    company: str
    role: str
    link: Optional[str] = None
    status: str
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime