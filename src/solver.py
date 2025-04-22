from abc import ABC, abstractmethod

from wordle import State


class Solver(ABC):

    def __init__(self, solver_name: str):
        self.__solver_name = solver_name

    @abstractmethod
    def make_guess(self, state: State) -> str:
        pass

    @property
    def name(self) -> str:
        return self.__solver_name
