import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal
from app.models import Word

# 100 Unique JLPT Vocabulary Words
vocab_list = [
    {"kanji": "私", "yomikata": "わたし", "meaning": "I, me", "jlpt_level": "N5"},
    {"kanji": "あなた", "yomikata": "あなた", "meaning": "You", "jlpt_level": "N5"},
    {"kanji": "人", "yomikata": "ひと", "meaning": "Person", "jlpt_level": "N5"},
    {"kanji": "男", "yomikata": "おとこ", "meaning": "Man", "jlpt_level": "N5"},
    {"kanji": "女", "yomikata": "おんな", "meaning": "Woman", "jlpt_level": "N5"},
    {"kanji": "子供", "yomikata": "こども", "meaning": "Child", "jlpt_level": "N5"},
    {"kanji": "友達", "yomikata": "ともだち", "meaning": "Friend", "jlpt_level": "N5"},
    {"kanji": "時間", "yomikata": "じかん", "meaning": "Time", "jlpt_level": "N5"},
    {"kanji": "今日", "yomikata": "きょう", "meaning": "Today", "jlpt_level": "N5"},
    {"kanji": "明日", "yomikata": "あした", "meaning": "Tomorrow", "jlpt_level": "N5"},
    {"kanji": "昨日", "yomikata": "きのう", "meaning": "Yesterday", "jlpt_level": "N5"},
    {"kanji": "今", "yomikata": "いま", "meaning": "Now", "jlpt_level": "N5"},
    {"kanji": "前", "yomikata": "まえ", "meaning": "Before, front", "jlpt_level": "N5"},
    {"kanji": "後", "yomikata": "あと", "meaning": "After, later", "jlpt_level": "N5"},
    {"kanji": "朝", "yomikata": "あさ", "meaning": "Morning", "jlpt_level": "N5"},
    {"kanji": "昼", "yomikata": "ひる", "meaning": "Noon, daytime", "jlpt_level": "N5"},
    {"kanji": "夜", "yomikata": "よる", "meaning": "Night", "jlpt_level": "N5"},
    {"kanji": "月", "yomikata": "つき", "meaning": "Moon, month", "jlpt_level": "N5"},
    {"kanji": "火", "yomikata": "ひ", "meaning": "Fire", "jlpt_level": "N5"},
    {"kanji": "木", "yomikata": "き", "meaning": "Tree, wood", "jlpt_level": "N5"},
    {"kanji": "金", "yomikata": "きん", "meaning": "Gold, money", "jlpt_level": "N5"},
    {"kanji": "土", "yomikata": "つち", "meaning": "Earth, soil", "jlpt_level": "N5"},
    {"kanji": "山", "yomikata": "やま", "meaning": "Mountain", "jlpt_level": "N5"},
    {"kanji": "川", "yomikata": "かわ", "meaning": "River", "jlpt_level": "N5"},
    {"kanji": "海", "yomikata": "うみ", "meaning": "Sea, ocean", "jlpt_level": "N5"},
    {"kanji": "空", "yomikata": "そら", "meaning": "Sky", "jlpt_level": "N5"},
    {"kanji": "雨", "yomikata": "あめ", "meaning": "Rain", "jlpt_level": "N5"},
    {"kanji": "雪", "yomikata": "ゆき", "meaning": "Snow", "jlpt_level": "N5"},
    {"kanji": "風", "yomikata": "かぜ", "meaning": "Wind", "jlpt_level": "N4"},
    {"kanji": "天気", "yomikata": "てんき", "meaning": "Weather", "jlpt_level": "N5"},
    {"kanji": "家", "yomikata": "いえ", "meaning": "House, home", "jlpt_level": "N5"},
    {"kanji": "部屋", "yomikata": "へや", "meaning": "Room", "jlpt_level": "N5"},
    {"kanji": "窓", "yomikata": "まど", "meaning": "Window", "jlpt_level": "N5"},
    {"kanji": "ドア", "yomikata": "どあ", "meaning": "Door", "jlpt_level": "N5"},
    {"kanji": "机", "yomikata": "つくえ", "meaning": "Desk", "jlpt_level": "N5"},
    {"kanji": "椅子", "yomikata": "いす", "meaning": "Chair", "jlpt_level": "N5"},
    {"kanji": "仕事", "yomikata": "しごと", "meaning": "Job, work", "jlpt_level": "N5"},
    {"kanji": "会社", "yomikata": "かいしゃ", "meaning": "Company", "jlpt_level": "N5"},
    {"kanji": "お金", "yomikata": "おかね", "meaning": "Money", "jlpt_level": "N5"},
    {"kanji": "名前", "yomikata": "なまえ", "meaning": "Name", "jlpt_level": "N5"},
    {"kanji": "話", "yomikata": "はなし", "meaning": "Talk, story", "jlpt_level": "N5"},
    {"kanji": "音楽", "yomikata": "おんがく", "meaning": "Music", "jlpt_level": "N5"},
    {"kanji": "歌", "yomikata": "うた", "meaning": "Song", "jlpt_level": "N5"},
    {"kanji": "映画", "yomikata": "えいが", "meaning": "Movie", "jlpt_level": "N5"},
    {"kanji": "写真", "yomikata": "しゃしん", "meaning": "Photograph", "jlpt_level": "N5"},
    {"kanji": "車", "yomikata": "くるま", "meaning": "Car", "jlpt_level": "N5"},
    {"kanji": "自転車", "yomikata": "じてんしゃ", "meaning": "Bicycle", "jlpt_level": "N5"},
    {"kanji": "駅", "yomikata": "えき", "meaning": "Train station", "jlpt_level": "N5"},
    {"kanji": "道", "yomikata": "みち", "meaning": "Road, street", "jlpt_level": "N5"},
    {"kanji": "店", "yomikata": "みせ", "meaning": "Shop, store", "jlpt_level": "N5"},
    {"kanji": "ご飯", "yomikata": "ごはん", "meaning": "Rice, meal", "jlpt_level": "N5"},
    {"kanji": "肉", "yomikata": "にく", "meaning": "Meat", "jlpt_level": "N5"},
    {"kanji": "魚", "yomikata": "さかな", "meaning": "Fish", "jlpt_level": "N5"},
    {"kanji": "野菜", "yomikata": "やさい", "meaning": "Vegetable", "jlpt_level": "N5"},
    {"kanji": "果物", "yomikata": "くだもの", "meaning": "Fruit", "jlpt_level": "N5"},
    {"kanji": "お茶", "yomikata": "おちゃ", "meaning": "Green tea", "jlpt_level": "N5"},
    {"kanji": "牛乳", "yomikata": "ぎゅうにゅう", "meaning": "Milk", "jlpt_level": "N5"},
    {"kanji": "右", "yomikata": "みぎ", "meaning": "Right", "jlpt_level": "N5"},
    {"kanji": "左", "yomikata": "ひだり", "meaning": "Left", "jlpt_level": "N5"},
    {"kanji": "上", "yomikata": "うえ", "meaning": "Up, above", "jlpt_level": "N5"},
    {"kanji": "下", "yomikata": "した", "meaning": "Down, below", "jlpt_level": "N5"},
    {"kanji": "中", "yomikata": "なか", "meaning": "Inside, middle", "jlpt_level": "N5"},
    {"kanji": "外", "yomikata": "そと", "meaning": "Outside", "jlpt_level": "N5"},
    {"kanji": "見る", "yomikata": "みる", "meaning": "To see, to watch", "jlpt_level": "N5"},
    {"kanji": "聞く", "yomikata": "きく", "meaning": "To hear, to listen", "jlpt_level": "N5"},
    {"kanji": "話す", "yomikata": "はなす", "meaning": "To speak, to talk", "jlpt_level": "N5"},
    {"kanji": "読む", "yomikata": "よむ", "meaning": "To read", "jlpt_level": "N5"},
    {"kanji": "書く", "yomikata": "かく", "meaning": "To write", "jlpt_level": "N5"},
    {"kanji": "買う", "yomikata": "かう", "meaning": "To buy", "jlpt_level": "N5"},
    {"kanji": "会う", "yomikata": "あう", "meaning": "To meet", "jlpt_level": "N5"},
    {"kanji": "休む", "yomikata": "やすむ", "meaning": "To rest, to take a break", "jlpt_level": "N5"},
    {"kanji": "寝る", "yomikata": "ねる", "meaning": "To sleep", "jlpt_level": "N5"},
    {"kanji": "起きる", "yomikata": "おきる", "meaning": "To wake up", "jlpt_level": "N5"},
    {"kanji": "歩く", "yomikata": "あるく", "meaning": "To walk", "jlpt_level": "N5"},
    {"kanji": "走る", "yomikata": "はしる", "meaning": "To run", "jlpt_level": "N5"},
    {"kanji": "泳ぐ", "yomikata": "およぐ", "meaning": "To swim", "jlpt_level": "N5"},
    {"kanji": "遊ぶ", "yomikata": "あそぶ", "meaning": "To play", "jlpt_level": "N5"},
    {"kanji": "待つ", "yomikata": "まつ", "meaning": "To wait", "jlpt_level": "N5"},
    {"kanji": "持つ", "yomikata": "もつ", "meaning": "To hold", "jlpt_level": "N5"},
    {"kanji": "教える", "yomikata": "おしえる", "meaning": "To teach", "jlpt_level": "N5"},
    {"kanji": "良い", "yomikata": "よい", "meaning": "Good", "jlpt_level": "N5"},
    {"kanji": "悪い", "yomikata": "わるい", "meaning": "Bad", "jlpt_level": "N5"},
    {"kanji": "熱い", "yomikata": "あつい", "meaning": "Hot", "jlpt_level": "N5"},
    {"kanji": "寒い", "yomikata": "さむい", "meaning": "Cold", "jlpt_level": "N5"},
    {"kanji": "早い", "yomikata": "はやい", "meaning": "Early, fast", "jlpt_level": "N5"},
    {"kanji": "遅い", "yomikata": "おそい", "meaning": "Late, slow", "jlpt_level": "N5"},
    {"kanji": "忙しい", "yomikata": "いそがしい", "meaning": "Busy", "jlpt_level": "N5"},
    {"kanji": "白い", "yomikata": "しろい", "meaning": "White", "jlpt_level": "N5"},
    {"kanji": "黒い", "yomikata": "くろい", "meaning": "Black", "jlpt_level": "N5"},
    {"kanji": "赤い", "yomikata": "あかい", "meaning": "Red", "jlpt_level": "N5"},
    {"kanji": "青い", "yomikata": "あおい", "meaning": "Blue", "jlpt_level": "N5"},
    {"kanji": "春", "yomikata": "はる", "meaning": "Spring", "jlpt_level": "N4"},
    {"kanji": "夏", "yomikata": "なつ", "meaning": "Summer", "jlpt_level": "N4"},
    {"kanji": "秋", "yomikata": "あき", "meaning": "Autumn", "jlpt_level": "N4"},
    {"kanji": "冬", "yomikata": "ふゆ", "meaning": "Winter", "jlpt_level": "N4"},
    {"kanji": "頭", "yomikata": "あたま", "meaning": "Head", "jlpt_level": "N4"},
    {"kanji": "顔", "yomikata": "かお", "meaning": "Face", "jlpt_level": "N4"},
    {"kanji": "目", "yomikata": "め", "meaning": "Eye", "jlpt_level": "N4"},
    {"kanji": "耳", "yomikata": "みみ", "meaning": "Ear", "jlpt_level": "N4"},
    {"kanji": "手", "yomikata": "て", "meaning": "Hand", "jlpt_level": "N4"}
]

async def seed_100():
    print("Seeding 100 diverse vocabulary words...")
    async with SessionLocal() as session:
        words_to_insert = []
        for word_data in vocab_list:
            new_word = Word(
                kanji=word_data["kanji"],
                yomikata=word_data["yomikata"],
                meaning=word_data["meaning"],
                jlpt_level=word_data["jlpt_level"]
            )
            words_to_insert.append(new_word)
        
        session.add_all(words_to_insert)
        await session.commit()
        
    print("Successfully seeded 100 new unique words to Database!")

if __name__ == "__main__":
    asyncio.run(seed_100())
