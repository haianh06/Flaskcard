from typing import Annotated, Optional
from uuid import UUID
from pydantic import BaseModel, StringConstraints
from .word import WordResponse

class DeckCreate(BaseModel):
    title: str
    description: Annotated[str, StringConstraints(max_length=1000)]

class DeckResponse(BaseModel):
    id: UUID
    title: str
    description: Annotated[str, StringConstraints(max_length=1000)]
    words: list[WordResponse] = []
    model_config = {"from_attributes": True}

class DeckUpdate(BaseModel):
    title: Optional[str] = None
    description: Annotated[str | None, StringConstraints(max_length=1000)] = None
