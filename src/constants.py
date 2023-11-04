MONGO_URL = "mongodb://localhost:27017/"
MONGO_DATABASE = "music_quiz"
MONGO_USERS_DATABASE = "quiz"
MONGO_USERS_COLLECTION = "users"
MONGO_SETTINGS_COLLECTION = "settings"
MONGO_AUDIOS_COLLECTION = "audios"
MONGO_ARTISTS_COLLECTION = "artists"
MONGO_STATISTIC_COLLECTION = "statistic"
MONGO_QUESTION_COLLECTION = "questions"

INTRODUCTION_TIME = 15
CHORUS_THRESHOLD = 0.9
LINE_THRESHOLD = 80
CHORUS_MIN_LENGTH = 4
TOP_COUNT = 10
CROP_IMAGE_SIZE = 200
QUESTION_STATISTICS_LIMIT = 250
REPEAT_PROBABILITY = 0.005
LEADERBOARD_QUESTIONS_COUNT = 100

ROCK_GENRE = "rock"
POP_GENRE = "pop"
HIP_HOP_GENRE = "hip-hop"
ELECTRONICS_GENRE = "electronic"
DISCO_GENRE = "disco"
JAZZ_SOUL_GENRE = "jazz-soul"
GENRES = [ROCK_GENRE, POP_GENRE, HIP_HOP_GENRE, ELECTRONICS_GENRE, DISCO_GENRE, JAZZ_SOUL_GENRE]

GENRE_TO_YANDEX = {
    ROCK_GENRE: {
        "allrock", "alternative", "alternativemetal", "amerfolk", "bard", "blackmetal", "classicmetal", "deathmetal", "doommetal", "epicmetal", "eurofolk",
        "extrememetal", "folk", "folkgenre", "folkmetal", "folkrock", "foreignbard", "gothicmetal", "hardcore", "hardrock", "indie", "industrial", "israelirock",
        "latinfolk", "local-indie", "metal", "metalcoregenre", "newage", "newwave", "numetal", "posthardcore", "postmetal", "postpunk", "postrock", "prog",
        "progmetal", "punk", "rnr", "rock", "romances", "rusbards", "rusfolk", "rusrock", "ska", "sludgemetal", "stonerrock", "thrashmetal",
        "turkishalternative", "turkishfolk", "turkishrock", "ukrrock"
    },

    HIP_HOP_GENRE: {
        "foreignrap", "israelirap", "modern", "phonkgenre", "rap", "reggaeton", "rusrap", "triphopgenre", "turkishrap"
    },

    POP_GENRE: {
        "arabicpop", "azerbaijanpop", "dance", "estrada", "hyperpopgenre", "israelipop", "japanesepop", "kpop", "newwave", "pop", "rusestrada", "ruspop", "shanson",
        "turkishpop", "uzbekpop", "edmgenre"
    },

    ELECTRONICS_GENRE: {
        "ambientgenre", "bassgenre", "breakbeatgenre", "dnb", "dub", "dubstep", "electronics", "house", "idmgenre", "techno", "trance", "ukgaragegenre"
    },

    DISCO_GENRE: {
        "disco"
    },

    JAZZ_SOUL_GENRE: {
        "bebopgenre", "bigbands", "blues", "conjazz", "country", "experimental", "funk", "jazz", "rnb", "smoothjazz", "soul", "tradjazz", "vocaljazz"
    }
}

GENRE_TO_RUS = {
    ROCK_GENRE: "рок",
    POP_GENRE: "поп",
    HIP_HOP_GENRE: "хип-хоп",
    ELECTRONICS_GENRE: "электронная",
    DISCO_GENRE: "диско",
    JAZZ_SOUL_GENRE: "джаз / соул"
}

CREATION_TO_RUS = {
    "russian": "русское",
    "foreign": "зарубежное"
}

QUESTION_YEARS = [1980, 1990, 2000, 2010, 2015]

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

QUESTION_TO_WEIGHT = {
    QUESTION_ARTIST_BY_TRACK: 1,
    QUESTION_ARTIST_BY_INTRO: 2,
    QUESTION_NAME_BY_TRACK: 3,
    QUESTION_LINE_BY_TEXT: 5,
    QUESTION_LINE_BY_CHORUS: 3
}

ARTIST_QUESTIONS = [QUESTION_ARTIST_BY_TRACK, QUESTION_ARTIST_BY_INTRO]
TEXT_QUESTIONS = [QUESTION_LINE_BY_TEXT, QUESTION_LINE_BY_CHORUS]

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
