from pymongo import ASCENDING, MongoClient

from src import constants


class MongoManager:
    client: MongoClient = None
    users = None
    settings = None
    audios = None
    artists = None
    statistic = None
    questions = None

    def connect(self) -> None:
        self.client = MongoClient(constants.MONGO_URL)

        users_database = self.client[constants.MONGO_USERS_DATABASE]
        self.users = users_database[constants.MONGO_USERS_COLLECTION]

        database = self.client[constants.MONGO_DATABASE]
        self.settings = database[constants.MONGO_SETTINGS_COLLECTION]
        self.audios = database[constants.MONGO_AUDIOS_COLLECTION]
        self.artists = database[constants.MONGO_ARTISTS_COLLECTION]
        self.statistic = database[constants.MONGO_STATISTIC_COLLECTION]
        self.questions = database[constants.MONGO_QUESTION_COLLECTION]

        self.audios.create_index([("artists.id", ASCENDING)])
        self.audios.create_index([("track_id", ASCENDING)], unique=True)
        self.audios.create_index(["year"])
        self.audios.create_index(["creation"])
        self.audios.create_index(["lyrics"])

        self.artists.create_index([("id", ASCENDING)], unique=True)
        self.artists.create_index([("genres", ASCENDING)])

        self.statistic.create_index([("username", ASCENDING)])
        self.statistic.create_index(["datetime"])
        self.statistic.create_index(["question_type"])
        self.statistic.create_index(["track_id"])

        self.questions.create_index([("username", ASCENDING)])

    def close(self) -> None:
        self.client.close()
