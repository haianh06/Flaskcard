from ..models import Deck, Word
from sqlalchemy import select
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.word import WordCreate, WordUpdate

async def create_word(word_in: WordCreate, session: AsyncSession) -> Word:
    word_db = Word(**word_in.model_dump())
    session.add(word_db)
    await session.commit()
    await session.refresh(word_db)
    return word_db

from sqlalchemy import select, func, or_

async def read_words(session: AsyncSession, offset: int = 0, limit: int = 100, search: str = None) -> tuple[list[Word], int]:
    stmt = select(Word)
    
    if search:
        search_term = f"%{search}%"
        stmt = stmt.where(
            or_(
                Word.kanji.ilike(search_term),
                Word.yomikata.ilike(search_term),
                Word.meaning.ilike(search_term)
            )
        )
        
    count_stmt = select(func.count()).select_from(stmt.subquery())
    total = await session.scalar(count_stmt)
    
    result = await session.execute(stmt.offset(offset).limit(limit))
    return list(result.scalars().all()), total

async def read_word(session: AsyncSession, word_id: UUID) -> Word:
    word_db = await session.get(Word, word_id)
    if not word_db:
        return None
    return word_db

async def update_word(session: AsyncSession, word_id: UUID, word_in: WordUpdate):
    word_db = await session.get(Word, word_id)
    if not word_db:
        return None
    updated_word = word_in.model_dump(exclude_unset=True)
    for key, value in updated_word.items():
        setattr(word_db, key, value)
    await session.commit()
    await session.refresh(word_db)
    return word_db

async def delete_word(session: AsyncSession, word_id: UUID):
    word_db = await session.get(Word, word_id)
    if not word_db:
        return None
    await session.delete(word_db)
    await session.commit()
    return {"ok": True}