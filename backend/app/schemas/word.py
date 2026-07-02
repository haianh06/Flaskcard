from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class WordUpdate(BaseModel):
    kanji: Optional[str] = None
    yomikata: Optional[str] = None
    meaning: Optional[str] = None
    jlpt_level: Optional[str] = None

class WordCreate(BaseModel):
    kanji: Optional[str] = None
    yomikata: str
    meaning: str
    jlpt_level: str

class WordResponse(BaseModel):
    id: UUID
    kanji: Optional[str] = None
    yomikata: str
    meaning: str
    jlpt_level: str
    model_config = {"from_attributes": True}

class WordListResponse(BaseModel):
    total: int
    items: list[WordResponse]