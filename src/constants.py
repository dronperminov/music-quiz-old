MONGO_URL = "mongodb://localhost:27017/"
MONGO_DATABASE = "music_quiz"
MONGO_USERS_COLLECTION = "users"
MONGO_AUDIOS_COLLECTION = "audios"
MONGO_ARTISTS_COLLECTION = "artists"

INTRODUCTION_TIME = 15

VERSION = "2023-10-25-14-00"

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

QUESTION_TO_TITLE = {
    QUESTION_ARTIST_BY_TRACK: "назовите исполнителя песни",
    QUESTION_ARTIST_BY_INTRO: "назовите исполнителя песни по её вступлению",
    QUESTION_NAME_BY_TRACK: "назовите название песни",
    QUESTION_LINE_BY_TEXT: "продолжите строку",
    QUESTION_LINE_BY_CHORUS: "продолжите строку припева"
}

QUESTION_ARTISTS_SOLE = "sole"
QUESTION_ARTISTS_FEATS = "feats"
QUESTION_ARTISTS = [QUESTION_ARTISTS_SOLE, QUESTION_ARTISTS_FEATS]

QUESTION_ARTISTS_TO_RUS = {
    QUESTION_ARTISTS_SOLE: "единственный исполнитель",
    QUESTION_ARTISTS_FEATS: "несколько исполнителей"
}

TEXT_LANGUAGE_RUSSIAN = "russian"
TEXT_LANGUAGE_FOREIGN = "foreign"
TEXT_LANGUAGES = [TEXT_LANGUAGE_RUSSIAN, TEXT_LANGUAGE_FOREIGN]

TEXT_LANGUAGE_TO_RUS = {
    TEXT_LANGUAGE_RUSSIAN: "русский",
    TEXT_LANGUAGE_FOREIGN: "иностранный"
}
