import random

import sad
import romantic
import lofi
import party
import gaming


# ----------------------------
# ALL CATEGORIES DATABASE
# ----------------------------
CATEGORIES = {
    "sad": sad.SONGS,
    "romantic": romantic.SONGS,
    "lofi": lofi.SONGS,
    "party": party.SONGS,
    "gaming": gaming.SONGS
}


# ----------------------------
# GET SONGS BY CATEGORY
# ----------------------------
def get_songs(category: str):
    return CATEGORIES.get(category.lower(), [])


# ----------------------------
# SHUFFLE PLAYLIST
# ----------------------------
def shuffle(category: str):
    songs = get_songs(category).copy()
    random.shuffle(songs)
    return songs


# ----------------------------
# RANDOM SONG PICK
# ----------------------------
def random_song(category: str):
    songs = get_songs(category)
    if not songs:
        return None
    return random.choice(songs)


# ----------------------------
# CHECK VALID CATEGORY
# ----------------------------
def valid(category: str):
    return category.lower() in CATEGORIES


# ----------------------------
# GET ALL CATEGORIES
# ----------------------------
def all_categories():
    return list(CATEGORIES.keys())


# ----------------------------
# GET FIRST SONG
# ----------------------------
def first_song(category: str):
    songs = get_songs(category)
    return songs[0] if songs else None


# ----------------------------
# TOTAL SONG COUNT
# ----------------------------
def count(category: str):
    return len(get_songs(category))
