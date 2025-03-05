from collections import deque
from typing import List, Optional, Tuple
from game import PuzzleGame
from solvers.base import GameSolver
import time

class BFSSolver(GameSolver):
    def solve(self, game: PuzzleGame) -> Optional[Tuple[List[List[int]], float]]:
        start_time = time.time()
        initial_state = game.initial_list
        queue = deque([(initial_state, [initial_state])])
        seen_states = set()
        
        while queue:
            state, path = queue.popleft()
            
            if game.is_goal_state(state):
                elapsed_time = time.time() - start_time
                return path, elapsed_time
            
            for move_type, new_state in game.get_valid_moves(state):
                new_state_tuple = tuple(new_state)
                if new_state_tuple not in seen_states:
                    seen_states.add(new_state_tuple)
                    queue.append((new_state, path + [new_state]))
        
        return None, time.time() - start_time
