from collections import defaultdict

from src.database import database
from src.utils.artists import get_lyrics_creation
from src.utils.question import detect_chorus


def main():
    database.connect()

    # автоматическое обновление языка песни с имеющимся текстом
    audios = database.audios.find({"lyrics": {"$exists": True, "$ne": []}}, {"track_id": 1, "lyrics": 1, "creation": 1})

    for audio in audios:
        creation = get_lyrics_creation(audio["lyrics"])
        chorus = detect_chorus(audio["lyrics"]) is not None
        database.audios.update_one({"track_id": audio["track_id"]}, {"$set": {"creation": creation, "chorus": chorus}}, upsert=True)

    # автоматическая простановка языка тем песням, чьи артисты исполняют только на одном языке
    audios = list(database.audios.find({"artists": {"$size": 1}}, {"track_id": 1, "artists": 1, "creation": 1}))
    artist2creation = defaultdict(list)

    for audio in audios:
        artist_id = audio["artists"][0]["id"]
        artist2creation[artist_id].extend(audio.get("creation", []))

    # для аудиозаписей с единственным исполнителем и не проставленным языком
    for audio in database.audios.find({"artists": {"$size": 1}, "creation.0": {"$exists": False}}, {"artists": 1,"track": 1, "track_id": 1}):
        tracks_creation = artist2creation[audio["artists"][0]["id"]]
        creation = list(set(tracks_creation))

        if len(tracks_creation) < 5 or len(creation) != 1:
            continue

        print(f'Update creation of {audio["artists"][0]["name"]} - {audio["track"]} with {creation}')  # noqa
        database.audios.update_one({"track_id": audio["track_id"]}, {"$set": {"creation": creation}})


if __name__ == '__main__':
    main()
