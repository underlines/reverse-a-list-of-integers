from collections import deque
from typing import List, Optional, Tuple
from game import PuzzleGame
from solvers.base import GameSolver
import time
import random

class HybridSolver(GameSolver):
    def __init__(self, beam_width: int = 10, max_time: float = 30.0):
        """
        :param beam_width: Maximum number of states to keep in each iteration.
        :param max_time: Maximum time (seconds) the solver is allowed to run.
        """
        self.beam_width = beam_width
        self.max_time = max_time

    def neighbors(self, state: List[int]) -> List[List[int]]:
        """Generate all possible next states from 'state' via a single 'add' or 'split' operation."""
        next_states = []
        n = len(state)

        # Add operation: merge two adjacent elements
        for i in range(n - 1):
            a, b = state[i], state[i + 1]
            new_val = a + b
            # Must not exceed 9 and preserve uniqueness
            if new_val <= 9:
                new_state = state[:i] + [new_val] + state[i+2:]
                if len(set(new_state)) == len(new_state):
                    next_states.append(new_state)

        # Split operation: split one element into two parts
        for i in range(n):
            x = state[i]
            for u in range(1, x):
                v = x - u
                if u != v:  # Prevent duplicate from the split itself
                    new_state = state[:i] + [u, v] + state[i+1:]
                    if all(1 <= num <= 9 for num in new_state) and len(set(new_state)) == len(new_state):
                        next_states.append(new_state)

        random.shuffle(next_states)
        return next_states

    def solve(self, game: PuzzleGame) -> Optional[Tuple[List[List[int]], float]]:
        """
        Hybrid approach with beam-search-like expansion, random fallback expansions, random restarts,
        and a user-defined time limit. Removes early breaks to allow full usage of max_time.
        """
        start_time = time.time()
        initial_state = game.initial_list

        visited_paths = dict()
        visited_paths[tuple(initial_state)] = [initial_state]
        visited = set()
        visited.add(tuple(initial_state))

        # The queue holds (state, path) pairs.
        queue = [(initial_state, [initial_state])]

        def heuristic(state: List[int]) -> float:
            # If puzzle-specific heuristic is available, use it.
            if hasattr(game, 'estimate_distance') and callable(game.estimate_distance):
                return game.estimate_distance(state)
            # Otherwise, prefer smaller states + random tie-break
            return len(state) + random.random()

        def random_unstuck_expansion() -> List[tuple]:
            """Attempt expansions from random visited states if we get stuck."""
            expansions = []
            visited_list = list(visited)
            if not visited_list:
                return expansions
            # pick up to 5 random states as seeds
            seeds = random.sample(visited_list, min(5, len(visited_list)))
            for s in seeds:
                s_path = visited_paths[s]
                for ns in self.neighbors(list(s)):
                    t_ns = tuple(ns)
                    if t_ns not in visited:
                        visited.add(t_ns)
                        new_path = s_path + [ns]
                        visited_paths[t_ns] = new_path
                        expansions.append((ns, new_path))
            return expansions

        while time.time() - start_time < self.max_time:
            # Sort states by heuristic ascending
            queue.sort(key=lambda item: heuristic(item[0]))
            # Keep only the top beam_width states
            queue = queue[:self.beam_width]

            new_queue = []
            for (state, path) in queue:
                if game.is_goal_state(state):
                    elapsed_time = time.time() - start_time
                    return path, elapsed_time

                # Expand neighbors
                for next_state in self.neighbors(state):
                    t_next = tuple(next_state)
                    if t_next not in visited:
                        visited.add(t_next)
                        new_path = path + [next_state]
                        visited_paths[t_next] = new_path
                        new_queue.append((next_state, new_path))

            if not new_queue:
                # Attempt expansions from random visited states
                fallback = random_unstuck_expansion()
                if not fallback:
                    # If no expansions at all, do a random restart from initial (no early break)
                    queue = [(initial_state, [initial_state])]
                    visited.add(tuple(initial_state))
                else:
                    new_queue.extend(fallback)

            queue = new_queue

        # If time limit is reached, no solution was found within the allowed time.
        return None, time.time() - start_time
