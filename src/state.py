from enum import Enum
from collections import Counter

from constants import NUMBER_OF_TURNS, WORD_LENGTH, CHARS


class GameStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    WON = "won"
    LOST = "lost"


class StateRow:
    GREEN_BG = "\033[42m"
    GREY_BG = "\033[100m"
    YELLOW_BG = "\033[43m"
    WHITE_TEXT = "\033[97m"
    RESET = "\033[0m"  # Reset color

    def __init__(self, word: str, correct_letters: list[bool], wrong_position_letters: list[bool]):
        self._word = word
        self._correct_letters = correct_letters
        self._wrong_position_letters = wrong_position_letters

    def __repr__(self):
        s = []
        for i in range(WORD_LENGTH):
            if self._correct_letters[i]:
                s.append(f"{self.GREEN_BG}{self._word[i]}{self.RESET}")
            elif self._wrong_position_letters[i]:
                s.append(f"{self.YELLOW_BG}{self._word[i]}{self.RESET}")
            else:
                s.append(f"{self.GREY_BG}{self._word[i]}{self.RESET}")
        return "".join(s)

    def __str__(self):
        return self.__repr__()


class State:
    def __init__(self, rows: tuple[StateRow, ...], words_all: tuple[str, ...], words_accepted: tuple[str, ...]):
        self.__rows = rows

        self.__present_letters_counter = self.__get_present_letters()
        self.__letter_constraints = self.__get_letter_constraints()

        self.__words_all = tuple((word for word in words_all if self.check_word(word)))
        self.__words_accepted = tuple((word for word in words_accepted if self.check_word(word)))

    def update_state(self, row: StateRow):
        updated_rows = self.__rows + (row,)
        return State(updated_rows, self.__words_all, self.__words_accepted)

    @property
    def words_accepted(self) -> tuple[str, ...]:
        return self.__words_accepted

    @property
    def words_all(self) -> tuple[str, ...]:
        return self.__words_all

    def check_word(self, word: str) -> bool:
        for i, constraints_set in enumerate(self.__letter_constraints):
            if word[i] not in constraints_set:
                return False
            word_cnt = Counter(word)
            for key, val in self.__present_letters_counter.items():
                if word_cnt[key] < val:
                    return False
        return True

    def __repr__(self):
        return "\n".join(str(row) for row in self.__rows)

    def __eq__(self, other):
        return (isinstance(other, State) and
                self.__letter_constraints == other.__letter_constraints and
                self.__present_letters_counter == other.__present_letters_counter)

    def __hash__(self):
        a = tuple(tuple(sorted(v)) for v in self.__letter_constraints)
        b = tuple((v, self.__present_letters_counter[v]) for v in sorted(self.__present_letters_counter))
        return hash((a, b))

    def __get_letter_constraints(self) -> tuple[set[str], ...]:
        ans = [set(CHARS) for _ in range(WORD_LENGTH)]
        # TODO: this is a bit ugly and could cause problems
        present = self.__present_letters_counter
        for row in self.__rows:
            for i in range(WORD_LENGTH):
                if (row._correct_letters[i]):
                    ans[i] = {row._word[i]}
                elif row._wrong_position_letters[i]:
                    if row._word[i] in ans[i]:
                        ans[i].remove(row._word[i])
                else:
                    if row._word[i] in ans[i]:
                        ans[i].remove(row._word[i])
                    for j in range(WORD_LENGTH if row._word[i] in present else 0, WORD_LENGTH):
                        if row._word[i] in ans[j]:
                            ans[j].remove(row._word[i])
        return tuple(ans)

    def __get_present_letters(self) -> Counter:
        ans = Counter()
        for row in self.__rows:
            sub_ans = Counter()
            for i in range(WORD_LENGTH):
                if row._correct_letters[i] or row._wrong_position_letters[i]:
                    sub_ans[row._word[i]] += 1
            for key, val in sub_ans.items():
                ans[key] = max(ans[key], val)
        return ans

    @property
    def turns_left(self):
        return NUMBER_OF_TURNS - len(self.__rows)
