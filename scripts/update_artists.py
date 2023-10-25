import random

from src.api import tokens
from src.database import database
from src.utils.artists import get_artists_creation
from src.utils.audio import parse_artist_genres


def main():
    database.connect()
    artists = database.artists.find({}, {"id": 1})
    artist_ids = [artist["id"] for artist in artists]
    artist_genres = parse_artist_genres(artist_ids, random.choice(tokens))
    artist_creation = get_artists_creation(artist_ids)

    for artist_id in artist_ids:
        genres = artist_genres[artist_id]
        creation = list(artist_creation[artist_id])
        database.artists.update_one({"id": artist_id}, {"$set": {"genres": genres, "creation": creation}}, upsert=True)


if __name__ == '__main__':
    main()
