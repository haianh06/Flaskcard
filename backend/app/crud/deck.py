from ..schemas.deck import DeckCreate, DeckUpdate
from ..models import Deck, Word
from sqlalchemy import select
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

async def create_deck(deck_in: DeckCreate, owner_id: UUID, session: AsyncSession) -> Deck:
    deck_db = Deck(**deck_in.model_dump(), owner_id=owner_id) 
    session.add(deck_db)
    await session.commit()
    result = await session.execute(select(Deck).filter(Deck.id == deck_db.id).options(selectinload(Deck.words)))
    return result.scalar_one()

async def read_decks(session: AsyncSession, owner_id: UUID, offset: int = 0, limit: int = 100) -> list[Deck]:
    result = await session.execute(select(Deck).filter(Deck.owner_id == owner_id).options(selectinload(Deck.words)).offset(offset).limit(limit))
    return list(result.scalars().all())

async def read_deck(session: AsyncSession, owner_id: UUID, deck_id: UUID) -> Deck:
    result = await session.execute(select(Deck).filter(Deck.id == deck_id, Deck.owner_id == owner_id).options(selectinload(Deck.words)))
    return result.scalar_one_or_none()

async def update_deck(session: AsyncSession, owner_id: UUID, deck_id: UUID, deck_in: DeckUpdate):
    result = await session.execute(select(Deck).filter(Deck.id == deck_id, Deck.owner_id == owner_id).options(selectinload(Deck.words)))
    deck_db = result.scalar_one_or_none()
    if not deck_db:
        return None
    updated_data = deck_in.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(deck_db, key, value)
    await session.commit()
    result = await session.execute(select(Deck).filter(Deck.id == deck_db.id).options(selectinload(Deck.words)))
    return result.scalar_one()

async def delete_deck(deck_id: UUID, owner_id: UUID, session: AsyncSession):
    result = await session.execute(select(Deck).filter(Deck.id == deck_id, Deck.owner_id == owner_id).options(selectinload(Deck.words)))
    deck_db = result.scalar_one_or_none()
    if not deck_db:
        return None
    await session.delete(deck_db)
    await session.commit()
    return {"ok": True}    

async def add_word_to_deck(deck_id: UUID, word_id: UUID, owner_id: UUID, session: AsyncSession) -> Deck:
    result = await session.execute(select(Deck).filter(Deck.id == deck_id, Deck.owner_id == owner_id).options(selectinload(Deck.words)))
    deck_db = result.scalar_one_or_none()
    word_db = await session.get(Word, word_id)
    if not deck_db or not word_db:
        return None
    if word_db not in deck_db.words: 
        deck_db.words.append(word_db)
        await session.commit()
        result = await session.execute(select(Deck).filter(Deck.id == deck_db.id).options(selectinload(Deck.words)))
        return result.scalar_one()
    return deck_db

async def delete_word_from_deck(deck_id: UUID, word_id: UUID, owner_id: UUID, session: AsyncSession) -> Deck:
    result = await session.execute(select(Deck).filter(Deck.id == deck_id, Deck.owner_id == owner_id).options(selectinload(Deck.words)))
    deck_db = result.scalar_one_or_none()
    word_db = await session.get(Word, word_id)
    if not deck_db or not word_db:
        return None
    if word_db in deck_db.words: 
        deck_db.words.remove(word_db)
        await session.commit()
        result = await session.execute(select(Deck).filter(Deck.id == deck_db.id).options(selectinload(Deck.words)))
        return result.scalar_one()
    return deck_db
