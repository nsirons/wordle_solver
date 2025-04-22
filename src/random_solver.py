import random

from solver import Solver, State


class RandomSolver(Solver):
    __SOLVER_NAME = "RandomSolver"

    def __init__(self, only_accepted_words: bool = True):
        self.__only_accepted_words = only_accepted_words
        super().__init__(f"{self.__SOLVER_NAME}({'accepted words' if self.__only_accepted_words else 'all words'})")

    def make_guess(self, state: State) -> str:
        if self.__only_accepted_words:
            return random.choice(state.words_accepted)
        return random.choice(state.words_all)
