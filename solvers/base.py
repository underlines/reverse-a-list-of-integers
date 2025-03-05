# This defines a base class for all solvers.
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple
from game import PuzzleGame

class GameSolver(ABC):
    @abstractmethod
    def solve(self, game: PuzzleGame) -> Optional[Tuple[List[List[int]], float]]:
        """Returns the solution steps and the time taken."""
        pass
