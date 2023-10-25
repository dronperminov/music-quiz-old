from src.database import database
from src.utils.artists import get_lyrics_creation
from src.utils.question import detect_chorus


def main():
    database.connect()
    audios = database.audios.find({"lyrics": {"$exists": True, "$ne": []}}, {"link": 1, "lyrics": 1})

    for audio in audios:
        creation = get_lyrics_creation(audio["lyrics"])
        chorus = detect_chorus(audio["lyrics"]) is not None
        database.audios.update_one({"link": audio["link"]}, {"$set": {"creation": creation, "chorus": chorus}}, upsert=True)


if __name__ == '__main__':
    main()
