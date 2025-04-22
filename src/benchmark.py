import logging
import random
from collections import Counter

from constants import NUMBER_OF_TURNS
from wordle import Wordle, GameStatus
from solver import Solver


class Benchmark:
    def __init__(self, solver_arr: tuple[Solver, ...], n_tries: int = 10 ** 3, seed: int = 0):
        self.__wordle = Wordle(logger_level=logging.ERROR)
        self.__n_tries = n_tries
        self.__solver_arr = solver_arr

        random.seed(seed)

    def analyze_solver(self):
        score_counter_arr = []
        for solver in self.__solver_arr:
            score_counter = Counter()
            for _ in range(self.__n_tries):
                self.__wordle.start_game(hard_mode=True)
                state = self.__wordle.state

                while self.__wordle.status == GameStatus.IN_PROGRESS:
                    guess_str = solver.make_guess(state)
                    state = self.__wordle.guess(guess_str)

                    if self.__wordle.status == GameStatus.WON:
                        score_counter[NUMBER_OF_TURNS - self.__wordle.turns_left] += 1
                    elif self.__wordle.status == GameStatus.LOST:
                        score_counter[-1] += 1

            score_counter_arr.append([solver.name, score_counter])

        self.print_result_table(score_counter_arr)

    def expected_score(self, score_counter: Counter) -> tuple[tuple[float, float]]:
        success_rate = 1. - (score_counter[-1] / self.__n_tries)
        success_cnt_expected = 0
        success_cnt_total = 0
        for score in range(1, NUMBER_OF_TURNS + 1):
            success_cnt_expected += score * score_counter[score]
            success_cnt_total += score_counter[score]
        return success_rate, success_cnt_expected / success_cnt_total

    def print_result_table(self, score_counter_arr: list[Counter]) -> None:
        headers = ["Solver", "Success Rate", "Average Score (Success only)"]
        rows = []
        for solver_name, score_counter in score_counter_arr:
            success_rate, avg_score = self.expected_score(score_counter)

            rows.append([solver_name, f"{100 * success_rate:.2f}%", f"{avg_score:.2f}"])

        rows.sort(key=lambda x: x[2], reverse=True)  # this is so wrong but ok
        # Create header row and separator
        header_row = "| " + " | ".join(headers) + " |"
        separator = "| " + " | ".join(["---"] * len(headers)) + " |"

        data_rows = ["| " + " | ".join(str(cell) for cell in row) + " |" for row in rows]
        markdown_table = "\n".join([header_row, separator] + data_rows)

        print(markdown_table)


if __name__ == "__main__":
    from random_solver import RandomSolver
    from dist_solver import DistSolver, DistanceMetric
    from entropy_solver import EntropySolver

    solver_random_accepted = RandomSolver(only_accepted_words=True)
    solver_random_all = RandomSolver(only_accepted_words=False)
    solver_dist_hamming = DistSolver(DistanceMetric.HAMMING_DISTANCE)
    solver_dist_freq = DistSolver(DistanceMetric.FREQ_DISTANCE)
    solver_entropy = EntropySolver()
    b = Benchmark(
        solver_arr=(solver_random_accepted, solver_random_all, solver_dist_hamming, solver_dist_freq, solver_entropy),
        n_tries=2309,
        seed=1
    )
    b.analyze_solver()
