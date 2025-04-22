import os
from enum import Enum
from collections import Counter
import pickle

import bisect
from constants import WORD_LENGTH


class CharState(Enum):
    GREY = 0
    YELLOW = 1
    GREEN = 2


def word_to_pattern_value(word_guess: str, word_secret: str) -> int:
    """Pattern can be represented as "trinary number", working with int to count number of patterns would be a bit more efficient"""
    # initialized with all values being "GREY" (aka 0)
    pattern_val = 0
    word_secret_cnt = Counter(word_secret)

    # first find all matching characters
    for i in range(WORD_LENGTH):
        if word_guess[i] == word_secret[i]:
            pattern_val += CharState.GREEN.value * (3 ** i)
            word_secret_cnt[word_guess[i]] -= 1

    # then find all present characters that are in the wrong place
    for i in range(WORD_LENGTH):
        if word_secret_cnt[word_guess[i]] > 0:
            pattern_val += CharState.YELLOW.value * (3 ** i)
            word_secret_cnt[word_guess[i]] -= 1
    return pattern_val


def pattern_value_to_pattern_arr(pattern_val: int) -> tuple[CharState, ...]:
    ans = [CharState.GREY for _ in range(WORD_LENGTH)]
    for i in range(WORD_LENGTH):
        ans[i] = CharState(pattern_val % 3)
        pattern_val //= 3
    return tuple(ans)


def pattern_arr_to_pattern_value(pattern: tuple[CharState, ...]) -> int:
    ans = 0
    for i in range(WORD_LENGTH):
        ans += pattern[-1 - i].value * (3 ** i)
    return ans


def load_words(filepath: str) -> tuple[str, ...]:
    with open(filepath, 'r') as f:
        words = tuple(word.strip() for word in f.readlines())
    return words


def load_all_words() -> tuple[str, ...]:
    filepath = os.path.join(os.path.abspath(''), "data", "words_all.txt")
    return load_words(filepath)


def load_accepted_words() -> tuple[str, ...]:
    filepath = os.path.join(os.path.abspath(''), "data", "words_accepted.txt")
    return load_words(filepath)


def get_word_to_word_pattern() -> dict:
    print("Loading word pattern, this may take a while...")
    word_to_word_pattern = dict()
    acc_word = sorted(load_accepted_words())
    all_word = sorted(load_all_words())
    for word in all_word:
        for word_other in acc_word:
            word_to_word_pattern[(word, word_other)] = word_to_pattern_value(word, word_other)
            # word_to_word_pattern[(word_other, word)] = word_to_pattern_value(word_other, word)
    return word_to_word_pattern


def dump_word_to_word_pattern(word_to_word_pattern: dict):
    filepath = os.path.join(os.path.abspath(''), "data", "word_to_word_pattern.pkl")
    with open(filepath, 'wb') as f:
        pickle.dump(word_to_word_pattern, f)


def load_word_to_word_pattern():
    filepath = os.path.join(os.path.abspath(''), "data", "word_to_word_pattern.pkl")
    with open(filepath, 'rb') as f:
        data = pickle.load(f)
    return data
