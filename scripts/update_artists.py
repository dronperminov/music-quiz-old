import random

from src.api import tokens
from src.database import database
from src.utils.artists import get_artists_creation
from src.utils.audio import parse_artist_genres


def main():
    database.connect()
    artists = list(database.artists.find({"$or": [
        {"genres.0": {"$exists": False}},
        {"creation.0": {"$exists": False}}
    ]}))

    artist_ids = [artist["id"] for artist in artists]
    artist_genres = parse_artist_genres(artist_ids, random.choice(tokens))
    artist_creation = get_artists_creation(artist_ids)

    for artist in artists:
        artist_id = artist["id"]

        if not artist.get("genres", []) and artist_genres[artist_id]:
            genres = artist_genres[artist_id]
            database.artists.update_one({"id": artist_id}, {"$set": {"genres": genres}}, upsert=True)
            print(f'Update artists {artist["name"]} genres with {genres}')  # noqa

        if not artist.get("creation", []) and artist_creation[artist_id]:
            creation = list(artist_creation[artist_id])
            database.artists.update_one({"id": artist_id}, {"$set": {"creation": creation}}, upsert=True)
            print(f'Update artists {artist["name"]} creation with {creation}')  # noqa


if __name__ == '__main__':
    main()
