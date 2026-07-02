import asyncio
import sys
import os
import random

# Tweak sys.path to allow importing from app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import Word

sample_words = [
    {"kanji": "猫", "yomikata": "ねこ", "meaning": "Cat", "jlpt_level": "N5"},
    {"kanji": "犬", "yomikata": "いぬ", "meaning": "Dog", "jlpt_level": "N5"},
    {"kanji": "食べる", "yomikata": "たべる", "meaning": "To eat", "jlpt_level": "N5"},
    {"kanji": "飲む", "yomikata": "のむ", "meaning": "To drink", "jlpt_level": "N5"},
    {"kanji": "行く", "yomikata": "いく", "meaning": "To go", "jlpt_level": "N5"},
    {"kanji": "来る", "yomikata": "くる", "meaning": "To come", "jlpt_level": "N5"},
    {"kanji": "大きい", "yomikata": "おおきい", "meaning": "Big", "jlpt_level": "N5"},
    {"kanji": "小さい", "yomikata": "ちいさい", "meaning": "Small", "jlpt_level": "N5"},
    {"kanji": "好き", "yomikata": "すき", "meaning": "Like", "jlpt_level": "N5"},
    {"kanji": "水", "yomikata": "みず", "meaning": "Water", "jlpt_level": "N5"},
    {"kanji": "学校", "yomikata": "がっこう", "meaning": "School", "jlpt_level": "N5"},
    {"kanji": "先生", "yomikata": "せんせい", "meaning": "Teacher", "jlpt_level": "N5"},
    {"kanji": "本", "yomikata": "ほん", "meaning": "Book", "jlpt_level": "N5"},
    {"kanji": "勉強", "yomikata": "べんきょう", "meaning": "Study", "jlpt_level": "N4"},
    {"kanji": "車", "yomikata": "くるま", "meaning": "Car", "jlpt_level": "N5"},
    {"kanji": "電車", "yomikata": "でんしゃ", "meaning": "Train", "jlpt_level": "N5"},
    {"kanji": "楽しい", "yomikata": "たのしい", "meaning": "Fun", "jlpt_level": "N4"},
    {"kanji": "高い", "yomikata": "たかい", "meaning": "High/Expensive", "jlpt_level": "N5"},
    {"kanji": "安い", "yomikata": "やすい", "meaning": "Cheap", "jlpt_level": "N5"},
    {"kanji": "新しい", "yomikata": "あたらしい", "meaning": "New", "jlpt_level": "N5"}
]

async def seed():
    print("Starting to seed 1000 words...")
    async with SessionLocal() as session:
        words_to_insert = []
        for i in range(1000):
            base_word = sample_words[i % len(sample_words)]
            
            # Đổi nhẹ tên để có sự khác biệt (ví dụ thêm số thứ tự)
            meaning = base_word["meaning"]
            if i >= len(sample_words):
                meaning += f" ({i+1})"
                
            new_word = Word(
                kanji=base_word["kanji"],
                yomikata=base_word["yomikata"],
                meaning=meaning,
                jlpt_level=base_word["jlpt_level"]
            )
            words_to_insert.append(new_word)
        
        # Insert theo lô
        session.add_all(words_to_insert)
        await session.commit()
        
    print("Successfully seeded 1000 words to Database!")

if __name__ == "__main__":
    asyncio.run(seed())
