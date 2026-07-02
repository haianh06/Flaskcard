import asyncio
import os
import sys
import urllib.request
import json
import time

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import Word

async def seed_from_jisho():
    print("Fetching vocabulary from Jisho API...")
    
    levels = ["n5", "n4", "n3"]
    words_to_insert = []
    
    # We will fetch 3 pages per level (60 words per level) to avoid rate limits
    # and provide a good solid base.
    for level in levels:
        for page in range(1, 4):
            url = f"https://jisho.org/api/v1/search/words?keyword=%23jlpt-{level}&page={page}"
            try:
                print(f"Fetching {url}...")
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                response = urllib.request.urlopen(req)
                data = json.loads(response.read())
                
                for item in data.get("data", []):
                    # extract kanji and reading
                    kanji = item["japanese"][0].get("word", "")
                    reading = item["japanese"][0].get("reading", "")
                    
                    if not kanji and reading:
                        kanji = reading # if no kanji, use kana as main
                        
                    if not kanji:
                        continue
                        
                    # Extract meaning
                    meanings = []
                    for sense in item.get("senses", []):
                        if "english_definitions" in sense:
                            meanings.extend(sense["english_definitions"])
                    
                    meaning = ", ".join(meanings[:3]) # take first 3 meanings
                    
                    # Extract level tag (some might be mixed)
                    word_level = f"N{level[-1]}"
                    
                    new_word = Word(
                        kanji=kanji,
                        yomikata=reading,
                        meaning=meaning,
                        jlpt_level=word_level
                    )
                    words_to_insert.append(new_word)
                time.sleep(1) # respectful delay
            except Exception as e:
                print(f"Error fetching {url}: {e}")
                
    if not words_to_insert:
        print("No words fetched!")
        return
        
    print(f"Successfully fetched {len(words_to_insert)} words. Inserting into database...")
    
    async with SessionLocal() as session:
        session.add_all(words_to_insert)
        await session.commit()
        
    print("Database seeding completed!")

if __name__ == "__main__":
    asyncio.run(seed_from_jisho())
