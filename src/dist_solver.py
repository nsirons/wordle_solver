from collections import Counter
from functools import lru_cache

from solver import Solver
from constants import WORD_LENGTH
from constants import NUMBER_OF_TURNS
from wordle import State
from enum import Enum, auto


class DistanceMatrixDict(dict):
    def __init__(self, func):
        super().__init__()
        self.func = func

    def __getitem__(self, key):
        if key not in self:
            self[key] = self.func(*key)
        return super().__getitem__(key)


class DistanceMetric(Enum):
    HAMMING_DISTANCE = auto()
    FREQ_DISTANCE = auto()


class DistSolver(Solver):
    __SOLVER_NAME = "DistanceSolver"

    def __init__(self, distance_metric: DistanceMetric):
        super().__init__(solver_name=f"{self.__SOLVER_NAME}({distance_metric})")
        distance_metric_f = None
        if distance_metric == DistanceMetric.HAMMING_DISTANCE:
            distance_metric_f = self.__hamming_distance
        elif distance_metric == DistanceMetric.FREQ_DISTANCE:
            distance_metric_f = self.__freq_distance

        self.__distance_metric = distance_metric
        self.__distance_matrix = DistanceMatrixDict(distance_metric_f)

    @lru_cache(maxsize=2 ** 11)
    def make_guess(self, state: State) -> str:
        if NUMBER_OF_TURNS - state.turns_left < 2:
            dist_arr = [(sum([self.__distance_matrix[min(word, word_dist), max(word, word_dist)] for word_dist in
                              state.words_accepted]), word) for word in state.words_all]
        else:
            dist_arr = [(sum([self.__distance_matrix[min(word, word_dist), max(word, word_dist)] for word_dist in
                              state.words_accepted]), word) for word in state.words_accepted]

        dist, word = min(dist_arr)
        return word

    @staticmethod
    def __hamming_distance(word: str, other_words: str) -> int:
        dist = 0
        for i in range(WORD_LENGTH):
            dist += word[i] != other_words[i]
        return dist

    @staticmethod
    def __freq_distance(word: str, other_words: str) -> int:
        dist = 0
        word = Counter(word)
        other_words = Counter(other_words)
        for char, char_cnt in other_words.items():
            dist += min(word[char], char_cnt)
        return WORD_LENGTH - dist

    def __hash__(self):
        # bad idea, but just to make cache work
        return hash(self.__distance_metric)

    def __eq__(self, other):
        # just to make cache work
        return isinstance(self, other.__class__) and self.__distance_metric == other.__distance_metric
