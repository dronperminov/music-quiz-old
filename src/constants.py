MONGO_URL = "mongodb://localhost:27017/"
MONGO_DATABASE = "music_quiz"
MONGO_USERS_COLLECTION = "users"
MONGO_AUDIOS_COLLECTION = "audios"
MONGO_ARTISTS_COLLECTION = "artists"

VERSION = "2023-10-23-21-00"

ROCK_GENRE = "rock"
POP_GENRE = "pop"
HIP_HOP_GENRE = "hip-hop"

ROCK_GENRES = {
    "allrock", "alternative", "alternativemetal", "amerfolk", "bard", "blackmetal", "deathmetal", "doommetal", "epicmetal", "eurofolk", "extrememetal", "postmetal",
    "progmetal", "sludgemetal", "thrashmetal", "classicmetal", "folkmetal", "gothicmetal", "israelirock", "folkrock", "hardrock", "postrock", "rock", "rusrock",
    "stonerrock", "turkishrock", "ukrrock", "folk", "folkgenre", "latinfolk", "rusfolk", "turkishfolk", "postpunk", "punk", "hardcore", "metalcoregenre", "numetal",
    "posthardcore", "romances", "rusbards", "foreignbard", "metal", "ska", "turkishalternative", "rnr", "shanson", "industrial", "prog"
}

HIP_HOP_GENRES = {
    "bassgenre", "dnb", "electronics", "foreignrap", "israelirap", "rap", "rusrap", "turkishrap", "funk", "house", "dub", "dubstep", "rnb", "techno", "triphopgenre",
    "trance", "edmgenre", "idmgenre", "modern", "phonkgenre", "reggaeton", "ukgaragegenre", "breakbeatgenre", "bollywood"
}

POP_GENRES = {
    "arabicpop", "azerbaijanpop", "dance", "disco", "estrada", "israelipop", "japanesepop", "kpop", "pop", "ruspop", "turkishpop", "uzbekpop", "bollywood", "newage",
    "newwave", "hyperpopgenre", "lounge", "rusestrada"
}

GENRE_TO_RUS = {
    ROCK_GENRE: "рок",
    POP_GENRE: "поп",
    HIP_HOP_GENRE: "хип-хоп",
}

CREATION_TO_RUS = {
    "russian": "русское",
    "foreign": "зарубежное"
}
