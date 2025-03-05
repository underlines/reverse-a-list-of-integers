from collections import deque
from typing import List, Optional, Tuple
from game import PuzzleGame
from solvers.base import GameSolver
import time

class BFSSolverImproved(GameSolver):
    def neighbors(self, state: List[int]) -> List[List[int]]:
        """Generate all possible next states from 'state' via a single 'add' or 'split' operation."""
        next_states = []
        n = len(state)
        
        # Add operation: merge two adjacent elements
        for i in range(n - 1):
            a, b = state[i], state[i + 1]
            new_val = a + b
            if new_val <= 9:  # Must not exceed max initial value
                new_state = state[:i] + [new_val] + state[i+2:]
                if len(set(new_state)) == len(new_state):  # Ensure uniqueness
                    next_states.append(new_state)
        
        # Split operation: split one element into two parts
        for i in range(n):
            x = state[i]
            for u in range(1, x):
                v = x - u
                if u != v:  # Prevent duplicate numbers
                    new_state = state[:i] + [u, v] + state[i+1:]
                    if all(1 <= num <= 9 for num in new_state) and len(set(new_state)) == len(new_state):
                        next_states.append(new_state)
        
        return next_states

    def solve(self, game: PuzzleGame) -> Optional[Tuple[List[List[int]], float]]:
        start_time = time.time()
        initial_state = game.initial_list
        queue = deque([(initial_state, [initial_state])])
        visited = set()
        visited.add(tuple(initial_state))

        while queue:
            state, path = queue.popleft()
            
            if game.is_goal_state(state):
                elapsed_time = time.time() - start_time
                return path, elapsed_time
            
            for new_state in self.neighbors(state):
                new_state_tuple = tuple(new_state)
                if new_state_tuple not in visited:
                    visited.add(new_state_tuple)
                    queue.append((new_state, path + [new_state]))
        
        return None, time.time() - start_time
