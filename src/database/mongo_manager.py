from pymongo import ASCENDING, MongoClient

from src import constants


class MongoManager:
    client: MongoClient = None
    users = None
    audios = None
    artists = None

    def connect(self) -> None:
        self.client = MongoClient(constants.MONGO_URL)
        database = self.client[constants.MONGO_DATABASE]

        self.users = database[constants.MONGO_USERS_COLLECTION]
        self.audios = database[constants.MONGO_AUDIOS_COLLECTION]
        self.artists = database[constants.MONGO_ARTISTS_COLLECTION]

        self.audios.create_index([("artists.id", ASCENDING)])
        self.audios.create_index([("link", ASCENDING)], unique=True)
        self.artists.create_index([("id", ASCENDING)], unique=True)

    def close(self) -> None:
        self.client.close()
