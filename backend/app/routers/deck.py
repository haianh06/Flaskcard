from ..schemas.deck import DeckCreate, DeckResponse, DeckUpdate
from fastapi import APIRouter, HTTPException, Query, Depends
from uuid import UUID
from typing import Annotated
from ..database import SessionDep
from ..crud import deck as deck_crud
from ..models import User
from ..utils.security import get_current_active_user

router = APIRouter(tags=["Decks"])

@router.post("/decks/")
async def create_deck(deck: DeckCreate, session: SessionDep, current_user: User = Depends(get_current_active_user)) -> DeckResponse:
    return await deck_crud.create_deck(deck_in=deck, owner_id=current_user.id, session=session)

@router.get("/decks/")
async def read_decks(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100, current_user: User = Depends(get_current_active_user)) -> list[DeckResponse]:
    return await deck_crud.read_decks(session=session, owner_id=current_user.id, offset=offset, limit=limit)

@router.get("/decks/{deck_id}")
async def read_deck(deck_id: UUID, session: SessionDep, current_user: User = Depends(get_current_active_user)) -> DeckResponse:
    deck_db = await deck_crud.read_deck(session=session, owner_id=current_user.id, deck_id=deck_id)
    if not deck_db:
        raise HTTPException(status_code=404, detail="Deck not found")
    return deck_db

@router.put("/decks/{deck_id}")
async def update_deck(deck_id: UUID, deck_in: DeckUpdate, session: SessionDep, current_user: User = Depends(get_current_active_user)):
    deck_db = await deck_crud.update_deck(session=session, owner_id=current_user.id, deck_id=deck_id, deck_in=deck_in)
    if not deck_db:
        raise HTTPException(status_code=404, detail="Deck not found")
    return deck_db

@router.delete("/decks/{deck_id}")
async def delete_deck(deck_id: UUID, session: SessionDep, current_user: User = Depends(get_current_active_user)):
    deck_db = await deck_crud.delete_deck(deck_id=deck_id, owner_id=current_user.id, session=session)
    if not deck_db:
        raise HTTPException(status_code=404, detail="Deck not found")
    return deck_db

@router.post("/decks/{deck_id}/words/{word_id}")
async def add_word_to_deck(deck_id: UUID, word_id: UUID, session: SessionDep, current_user: User = Depends(get_current_active_user)) -> DeckResponse:
    deck_db = await deck_crud.add_word_to_deck(deck_id=deck_id, word_id=word_id, owner_id=current_user.id, session=session)
    if not deck_db:
        raise HTTPException(status_code=404, detail="Deck or Word not found")
    return deck_db

@router.delete("/decks/{deck_id}/words/{word_id}")
async def delete_word_from_deck(deck_id: UUID, word_id: UUID, session: SessionDep, current_user: User = Depends(get_current_active_user)) -> DeckResponse:
    deck_db = await deck_crud.delete_word_from_deck(deck_id=deck_id, word_id=word_id, owner_id=current_user.id, session=session)
    if not deck_db:
        raise HTTPException(status_code=404, detail="Deck or Word not found")
    return deck_db
