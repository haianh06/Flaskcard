import uuid
from sqlalchemy import Column, String, Text, ForeignKey, Table, Boolean, null
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from .database import Base

deck_word_association = Table(
    'deck_words',
    Base.metadata,
    Column('deck_id', UUID(as_uuid=True), ForeignKey('decks.id'), primary_key=True),
    Column('word_id', UUID(as_uuid=True), ForeignKey('words.id'), primary_key=True)
)

class Deck(Base):
    __tablename__ = 'decks'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    title = Column(String(100), index=True, nullable=False)
    description = Column(Text, nullable=False)
    owner_id = Column(UUID(as_uuid=True), ForeignKey('user.id'))
    words = relationship("Word", secondary=deck_word_association, back_populates="decks")
    owner = relationship("User", back_populates="decks")

class Word(Base):
    __tablename__ = 'words'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    kanji = Column(String(255), index=True)
    yomikata = Column(String(255), index=True, nullable=False)
    meaning = Column(String(255), index=True, nullable=False)
    jlpt_level = Column(String(255), index=True, nullable=False)

    decks = relationship("Deck", secondary=deck_word_association, back_populates="words")

class User(Base):
    __tablename__ = 'user'
    id = Column(UUID(as_uuid=True), primary_key=True, nullable=False, index=True, default=uuid.uuid4)
    email = Column(String(255), index=True, nullable=False, unique=True)
    username = Column(String(50), index=True)
    hashed_password = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    is_supervisor = Column(Boolean, default=False)
    decks = relationship("Deck", back_populates="owner", cascade="all, delete-orphan")
