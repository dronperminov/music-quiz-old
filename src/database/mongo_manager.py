from pymongo import MongoClient

from src import constants


class MongoManager:
    client: MongoClient = None
    users = None
    audios = None

    def connect(self) -> None:
        self.client = MongoClient(constants.MONGO_URL)
        database = self.client[constants.MONGO_DATABASE]

        self.users = database[constants.MONGO_USERS_COLLECTION]
        self.audios = database[constants.MONGO_AUDIOS_COLLECTION]

    def close(self) -> None:
        self.client.close()
