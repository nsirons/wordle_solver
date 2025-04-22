import random
from collections import Counter
import logging

from constants import NUMBER_OF_TURNS, WORD_LENGTH
from state import GameStatus, State, StateRow
from utils import load_all_words, load_accepted_words


class Wordle:
    # Load data
    __WORDS_ALL: tuple[str, ...] = load_all_words()
    __WORDS_ACCEPTED: tuple[str, ...] = load_accepted_words()
    __WORDS_ALL_SET: set[str] = set(__WORDS_ALL)

    def __init__(self, word_repeat: bool = True, logger_level: int = logging.DEBUG):
        self.__word_generator = self.__get_word_generator() if word_repeat else None
        # Game state
        self.__status: GameStatus = GameStatus.NOT_STARTED
        self.__state: State = None
        self.__word_secret: str = None
        self.__turns_left: int = None
        self.__is_hard_mode: bool = None

        # Initialize Logger
        self.__logger = logging.getLogger(self.__class__.__name__)
        self.__logger.setLevel(logger_level)
        if not self.__logger.handlers:
            handler = logging.StreamHandler()
            handler.setLevel(logger_level)
            formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")
            handler.setFormatter(formatter)
            self.__logger.addHandler(handler)

        self.__logger.debug("Wordle initialized")

    @property
    def state(self) -> State:
        return self.__state

    def start_game(self, hard_mode: bool, seed: int = None):
        if seed is not None:
            random.seed(seed)

        self.__status = GameStatus.IN_PROGRESS
        self.__state = State((), self.__WORDS_ALL, self.__WORDS_ACCEPTED)
        self.__word_secret = self.__get_word()
        self.__turns_left = NUMBER_OF_TURNS
        self.__is_hard_mode = hard_mode

    def __get_word_generator(self):
        while True:
            copy_word_arr = list(self.__WORDS_ACCEPTED)
            random.shuffle(copy_word_arr)
            for word in copy_word_arr:
                yield word

    def __get_word(self) -> str:
        if self.__word_generator is None:
            return random.choice(self.__WORDS_ACCEPTED)
        else:
            return self.__word_generator.__next__()

    def guess(self, word: str) -> State | None:
        if self.__status != GameStatus.IN_PROGRESS:
            self.__logger.debug("Can't guess if game is not in progress")
            return None
        if not self.__word_is_valid(word):
            self.__logger.debug(f"Word {word} is not valid")
            return None

        self.__logger.debug(f"Guessing with word {word}")
        correct_letters, wrong_position_letters = self.__guess_mask(word)

        # Update state
        self.__turns_left -= 1
        if all(correct_letters):
            self.__status = GameStatus.WON
            self.__logger.debug(f"Game Won")
        elif self.__turns_left == 0:
            self.__logger.debug(f"Game Lost")
            self.__status = GameStatus.LOST

        state_row_turn = StateRow(word, correct_letters, wrong_position_letters)
        self.__logger.debug(state_row_turn)

        # Update constraints
        if self.__is_hard_mode:
            pass
        self.__state = self.__state.update_state(state_row_turn)
        return self.__state

    def __word_is_valid(self, word: str) -> bool:
        if not (word in self.__WORDS_ALL_SET):
            self.__logger.debug(f"Word {word} is not in the word list")
            return False

        # if easy mode, we don't need to check the constraints, only word presence in the **ALL** word list
        if self.__is_hard_mode and not self.__state.check_word(word):
            return False
        return True

    @property
    def status(self):
        return self.__status

    @property
    def turns_left(self):
        return self.__turns_left

    def __guess_mask(self, word: str):
        correct_letters = [False for _ in range(WORD_LENGTH)]
        wrong_position_letters = [False for _ in range(WORD_LENGTH)]

        word_counter = Counter(self.__word_secret)
        potential_wrong_positions = []
        for i in range(WORD_LENGTH):
            if self.__word_secret[i] == word[i]:
                correct_letters[i] = True
                word_counter[word[i]] -= 1
            elif word[i] in self.__word_secret:
                potential_wrong_positions.append((word[i], i))

        for char, idx in potential_wrong_positions:
            if (word_counter[char] > 0):
                word_counter[char] -= 1
                wrong_position_letters[idx] = True

        return correct_letters, wrong_position_letters
