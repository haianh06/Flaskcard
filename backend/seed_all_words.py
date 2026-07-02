import asyncio
import os
import sys
import urllib.request
import json
import zipfile
import tempfile
import time
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import Word

def get_latest_jmdict_url():
    print("Finding the latest JMDict-simplified release...")
    api_url = "https://api.github.com/repos/scriptin/jmdict-simplified/releases/latest"
    req = urllib.request.Request(api_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read())
        for asset in data.get('assets', []):
            if asset['name'].startswith('jmdict-eng-') and asset['name'].endswith('.json.zip'):
                return asset['browser_download_url']
    raise Exception("Could not find jmdict-eng JSON zip in the latest release.")

async def seed_all_words():
    print("Starting massive vocabulary import from JMDict...")
    
    url = get_latest_jmdict_url()
    print(f"Download URL found: {url}")
    
    # Download and extract
    with tempfile.TemporaryDirectory() as tmpdir:
        zip_path = os.path.join(tmpdir, "jmdict.zip")
        print("Downloading JMDict database (this may take a minute, ~40MB)...")
        urllib.request.urlretrieve(url, zip_path)
        
        print("Extracting JMDict...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(tmpdir)
            
        json_file = None
        for f in os.listdir(tmpdir):
            if f.endswith('.json'):
                json_file = os.path.join(tmpdir, f)
                break
                
        if not json_file:
            raise Exception("No JSON file found in the archive.")
            
        print(f"Loading JSON data from {json_file}...")
        with open(json_file, 'r', encoding='utf-8') as f:
            jmdict_data = json.load(f)
            
        words = jmdict_data.get('words', [])
        total_words = len(words)
        print(f"Successfully loaded {total_words} words from JMDict.")
        
        async with SessionLocal() as session:
            print("Cleaning up any previous aborted JMDict imports to prevent duplicates...")
            await session.execute(delete(Word).where(Word.jlpt_level == "Unknown"))
            await session.commit()
            
            batch_size = 10000
            words_to_insert = []
            inserted_count = 0
            
            for i, entry in enumerate(words):
                # Extract kanji (if any, else kana)
                kanji = ""
                if entry.get("kanji"):
                    kanji = entry["kanji"][0]["text"]
                    
                reading = ""
                if entry.get("kana"):
                    reading = entry["kana"][0]["text"]
                    
                if not kanji and reading:
                    kanji = reading
                    
                if not kanji:
                    continue
                    
                # Extract meaning
                meanings = []
                for sense in entry.get("sense", []):
                    for gloss in sense.get("gloss", []):
                        meanings.append(gloss["text"])
                
                meaning = ", ".join(meanings)
                
                # Truncate to fit VARCHAR(255)
                if len(kanji) > 255: kanji = kanji[:252] + "..."
                if len(reading) > 255: reading = reading[:252] + "..."
                if len(meaning) > 255: meaning = meaning[:252] + "..."
                
                new_word = Word(
                    kanji=kanji,
                    yomikata=reading,
                    meaning=meaning,
                    jlpt_level="Unknown" # JMDict doesn't natively map JLPT easily
                )
                words_to_insert.append(new_word)
                
                if len(words_to_insert) >= batch_size:
                    session.add_all(words_to_insert)
                    await session.commit()
                    inserted_count += len(words_to_insert)
                    print(f"Inserted {inserted_count}/{total_words} words...")
                    words_to_insert = []
            
            # Insert remaining
            if words_to_insert:
                session.add_all(words_to_insert)
                await session.commit()
                inserted_count += len(words_to_insert)
                
            print(f"Database seeding completed successfully! Inserted {inserted_count} words.")

if __name__ == "__main__":
    asyncio.run(seed_all_words())
