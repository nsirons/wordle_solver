from collections import defaultdict
from math import log2
from functools import lru_cache

from solver import Solver
from constants import NUMBER_OF_TURNS
from wordle import State
from utils import get_word_to_word_pattern


class EntropySolver(Solver):
    __SOLVER_NAME = "EntropySolver"
    __WORD_TO_WORD_PATTERN = get_word_to_word_pattern()

    def __init__(self):
        super().__init__(self.__SOLVER_NAME)

    def make_guess(self, state: State) -> str:
        if state.turns_left == NUMBER_OF_TURNS:
            # 1st choice is always the same, so just hardcoded it
            return "slate"
        return self.__make_guess_static(state)


    @staticmethod
    def __make_guess_static(state: State) -> str:
        max_entropy_value = -1.
        max_entropy_word = None
        for word in state.words_accepted:
            pattern_cnt = defaultdict(int)
            for word_secret in state.words_accepted:
                pattern_cnt[EntropySolver.__WORD_TO_WORD_PATTERN[(word, word_secret)]] += 1
            entropy = EntropySolver.__calculate_entropy(pattern_cnt)
            if entropy > max_entropy_value:
                max_entropy_value = entropy
                max_entropy_word = word
        return max_entropy_word

    @staticmethod
    def __calculate_entropy(pattern_cnt) -> float:
        entropy = 0.0
        total = sum(pattern_cnt.values())
        for pattern in pattern_cnt.values():
            p = pattern / total
            entropy += log2(p) * p
        return -entropy
