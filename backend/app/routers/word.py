from ..database import SessionDep
from ..schemas.word import WordCreate, WordResponse, WordUpdate
from uuid import UUID
from typing import Annotated
from fastapi import HTTPException, APIRouter, Query, Depends
from ..crud import word as word_crud
from ..models import User
from ..utils.security import get_current_active_user

router = APIRouter(tags=["Words"])

@router.post("/words/")
async def create_word(word: WordCreate, session: SessionDep, current_user: User = Depends(get_current_active_user)) -> WordResponse:
    if current_user.is_supervisor == False:
        raise HTTPException(status_code=403, detail="Words can only be created by the system administrator.")
    return await word_crud.create_word(word=word, session=session)

from ..schemas.word import WordCreate, WordResponse, WordUpdate, WordListResponse

@router.get("/words/", response_model=WordListResponse)
async def read_words(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 50, search: str = None):
    items, total = await word_crud.read_words(session=session, offset=offset, limit=limit, search=search)
    return {"total": total, "items": items}

@router.get("/words/{word_id}") 
async def read_word(word_id: UUID, session: SessionDep) -> WordResponse:
    word_db = await word_crud.read_word(word_id=word_id, session=session)
    if not word_db:
        raise HTTPException(status_code=404, detail="Word not found")
    return word_db

@router.put("/words/{word_id}")
async def update_word(word_id: UUID, word_in: WordUpdate, session: SessionDep, current_user: User = Depends(get_current_active_user)):
    if current_user.is_supervisor == False:
        raise HTTPException(status_code=403, detail="Words can only be modified by the system administrator.")
    deck_db = await word_crud.update_deck(session=session, owner_id=current_user.id, word_id=word_id, word_in=word_in)
    if not deck_db:
        raise HTTPException(status_code=404, detail="Deck not found")
    return deck_db

@router.delete("/words/{word_id}")
async def delete_word(word_id: UUID, session: SessionDep, current_user: User = Depends(get_current_active_user)):
    if current_user.is_supervisor == False:
        raise HTTPException(status_code=403, detail="Words can only be modified by the system administrator.")
    deck_db = await word_crud.delete_deck(deck_id=word_id, owner_id=current_user.id, session=session)
    if not deck_db:
        raise HTTPException(status_code=404, detail="Deck not found")
    return deck_db