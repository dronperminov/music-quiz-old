from src.database import database
from src.utils.artists import get_lyrics_creation


def main():
    database.connect()
    audios = database.audios.find({"lyrics": {"$exists": True, "$ne": []}}, {"link": 1, "lyrics": 1})

    for audio in audios:
        creation = list(get_lyrics_creation(audio["lyrics"]))
        database.audios.update_one({"link": audio["link"]}, {"$set": {"creation": creation}}, upsert=True)


if __name__ == '__main__':
    main()
