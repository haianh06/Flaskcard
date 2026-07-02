import asyncio
import os
import sys
import urllib.request
import json
import time
from sqlalchemy import select

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import Word

async def seed_1000_from_jisho():
    print("Fetching vocabulary from Jisho API...")
    
    levels = ["n5", "n4", "n3", "n2", "n1"]
    words_to_insert = []
    
    async with SessionLocal() as session:
        # Get existing words to avoid duplicates
        result = await session.execute(select(Word.kanji, Word.yomikata))
        existing_words = set((row.kanji, row.yomikata) for row in result.all())
        
        target_new_words = 1000
        new_words_count = 0
        
        for level in levels:
            if new_words_count >= target_new_words:
                break
                
            print(f"--- Fetching {level.upper()} vocabulary ---")
            
            # Fetch up to 20 pages per level
            for page in range(1, 21):
                if new_words_count >= target_new_words:
                    break
                    
                url = f"https://jisho.org/api/v1/search/words?keyword=%23jlpt-{level}&page={page}"
                try:
                    print(f"Fetching {url}...")
                    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                    response = urllib.request.urlopen(req)
                    data = json.loads(response.read())
                    
                    items = data.get("data", [])
                    if not items:
                        print(f"No more data for {level} on page {page}.")
                        break
                        
                    for item in items:
                        if new_words_count >= target_new_words:
                            break
                            
                        # extract kanji and reading
                        kanji = item["japanese"][0].get("word", "")
                        reading = item["japanese"][0].get("reading", "")
                        
                        if not kanji and reading:
                            kanji = reading # if no kanji, use kana as main
                            
                        if not kanji:
                            continue
                            
                        # Check for duplicates
                        if (kanji, reading) in existing_words:
                            continue
                            
                        # Extract meaning
                        meanings = []
                        for sense in item.get("senses", []):
                            if "english_definitions" in sense:
                                meanings.extend(sense["english_definitions"])
                        
                        meaning = ", ".join(meanings[:3]) # take first 3 meanings
                        
                        # Extract level tag
                        word_level = f"N{level[-1]}"
                        
                        new_word = Word(
                            kanji=kanji,
                            yomikata=reading,
                            meaning=meaning,
                            jlpt_level=word_level
                        )
                        words_to_insert.append(new_word)
                        existing_words.add((kanji, reading))
                        new_words_count += 1
                        
                    time.sleep(1) # respectful delay
                except Exception as e:
                    print(f"Error fetching {url}: {e}")
                    time.sleep(2)
                    
        if not words_to_insert:
            print("No new words to fetch! Everything is already in the database.")
            return
            
        print(f"Successfully fetched {len(words_to_insert)} NEW words. Inserting into database...")
        
        session.add_all(words_to_insert)
        await session.commit()
            
    print("Database seeding completed successfully!")

if __name__ == "__main__":
    asyncio.run(seed_1000_from_jisho())
