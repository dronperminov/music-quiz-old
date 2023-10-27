from pymongo import ASCENDING, MongoClient

from src import constants


class MongoManager:
    client: MongoClient = None
    users = None
    audios = None
    artists = None
    statistic = None

    def connect(self) -> None:
        self.client = MongoClient(constants.MONGO_URL)
        database = self.client[constants.MONGO_DATABASE]

        self.users = database[constants.MONGO_USERS_COLLECTION]
        self.audios = database[constants.MONGO_AUDIOS_COLLECTION]
        self.artists = database[constants.MONGO_ARTISTS_COLLECTION]
        self.statistic = database[constants.MONGO_STATISTIC_COLLECTION]

        self.audios.create_index([("artists.id", ASCENDING)])
        self.audios.create_index([("link", ASCENDING)], unique=True)

        self.artists.create_index([("id", ASCENDING)], unique=True)
        self.artists.create_index([("genres", ASCENDING)])

        self.statistic.create_index([("username", ASCENDING)])
        self.statistic.create_index(["datetime"])
        self.statistic.create_index(["question_type"])
        self.statistic.create_index(["link"])

    def close(self) -> None:
        self.client.close()
