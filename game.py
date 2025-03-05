# This contains the generic game logic, independent of solvers.
from typing import List, Tuple, Optional

class PuzzleGame:
    def __init__(self, initial_list: List[int]):
        self.initial_list = initial_list[:]
        self.max_value = max(initial_list)

    def is_goal_state(self, state: List[int]) -> bool:
        return state == self.initial_list[::-1]

    def get_valid_moves(self, state: List[int]) -> List[Tuple[str, List[int]]]:
        moves = []
        seen = set(state)
        
        # Split moves
        for i, num in enumerate(state):
            for a in range(1, num // 2 + 1):
                b = num - a
                if a != b and a not in seen and b not in seen and max(a, b) <= self.max_value:
                    new_state = state[:i] + [a, b] + state[i+1:]
                    moves.append(("split", new_state))
        
        # Merge moves
        for i in range(len(state) - 1):
            a, b = state[i], state[i+1]
            merged = a + b
            if merged <= self.max_value and merged not in seen:
                new_state = state[:i] + [merged] + state[i+2:]
                moves.append(("merge", new_state))
        
        return moves

    def play(self, solver):
        return solver.solve(self)
