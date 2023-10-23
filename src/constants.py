MONGO_URL = "mongodb://localhost:27017/"
MONGO_DATABASE = "music_quiz"
MONGO_USERS_COLLECTION = "users"
MONGO_AUDIOS_COLLECTION = "audios"
MONGO_ARTISTS_COLLECTION = "artists"

VERSION = "2023-10-24-02-00"

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

QUESTION_ARTIST_BY_TRACK = "artist_by_track"
QUESTION_ARTIST_BY_INTRO = "artist_by_intro"
QUESTION_NAME_BY_TRACK = "name_by_track"
QUESTION_LINE_BY_TEXT = "line_by_text"
QUESTION_LINE_BY_CHORUS = "line_by_chorus"

QUESTIONS = [QUESTION_ARTIST_BY_TRACK, QUESTION_ARTIST_BY_INTRO, QUESTION_NAME_BY_TRACK, QUESTION_LINE_BY_TEXT, QUESTION_LINE_BY_CHORUS]

QUESTION_TO_RUS = {
    QUESTION_ARTIST_BY_TRACK: "исполнитель по треку",
    QUESTION_ARTIST_BY_INTRO: "исполнитель по вступлению",
    QUESTION_NAME_BY_TRACK: "название по треку",
    QUESTION_LINE_BY_TEXT: "строка по тексту",
    QUESTION_LINE_BY_CHORUS: "строка по припеву"
}
