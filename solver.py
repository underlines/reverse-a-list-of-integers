# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "numpy"
# ]
# ///

# Game:
# A random list of unique, positive integers is chosen.
# The goal is to end up with the values in the list reversed. Eg. from [8,5,1] to [1,5,8].
# 
# Two moves are possible:
# 1. Split one of the integers in the list into two parts. Eg. 8 into 6,2.
# 2. Combine two adjacent integers into its sum. Eg. 5,1 into 6.
# 
# Rules:
# - The current list can not contain two equal integers.
# - The current list can not contain an integer larger than the largest in the initial list.


import heapq
import random
import numpy as np
from collections import deque

def get_valid_splits(num, max_value):
    """Generate all possible valid splits of a number."""
    return [(i, num - i) for i in range(1, num // 2 + 1)
            if i != num - i and num - i <= max_value]

def get_valid_merges(lst, max_value):
    """Generate all possible valid merges that do not exceed max_value."""
    return [(i, lst[i] + lst[i+1]) for i in range(len(lst) - 1)
            if lst[i] + lst[i+1] not in lst and lst[i] + lst[i+1] <= max_value]

def heuristic(state, target):
    """Simple heuristic: number of positions where the elements differ."""
    return sum(1 for a, b in zip(state, target) if a != b)

def find_shortest_solution(initial, target):
    """
    (1) Original A* (Deterministic)
    """
    max_value = max(initial)
    target_tuple = tuple(target)
    
    pq = []  # Priority queue for A*
    # (priority, steps, state, path)
    heapq.heappush(pq, (0, 0, tuple(initial), []))
    visited = set()
    
    while pq:
        _, steps, state, path = heapq.heappop(pq)
        
        if state == target_tuple:
            return path
        
        if state in visited:
            continue
        visited.add(state)
        
        # Splits
        for i, num in enumerate(state):
            for a, b in get_valid_splits(num, max_value):
                new_state = list(state[:i]) + [a, b] + list(state[i+1:])
                if len(set(new_state)) == len(new_state):
                    cost = steps + 1 + heuristic(new_state, target)
                    heapq.heappush(
                        pq,
                        (cost, steps + 1, tuple(new_state), path + [(state, new_state)])
                    )
        
        # Merges
        for i, merged in get_valid_merges(state, max_value):
            new_state = list(state[:i]) + [merged] + list(state[i+2:])
            if len(set(new_state)) == len(new_state):
                cost = steps + 1 + heuristic(new_state, target)
                heapq.heappush(
                    pq,
                    (cost, steps + 1, tuple(new_state), path + [(state, new_state)])
                )
    
    return None

def find_shortest_solution_with_randomness(initial, target, randomness=0.1):
    """
    (2) Brute-force with randomness in state expansion
    """
    max_value = max(initial)
    target_tuple = tuple(target)
    
    pq = []
    # (priority, steps, state, path)
    heapq.heappush(pq, (0, 0, tuple(initial), []))
    visited = set()
    
    while pq:
        _, steps, state, path = heapq.heappop(pq)
        
        if state == target_tuple:
            return path
        
        if state in visited:
            continue
        visited.add(state)
        
        next_states = []
        
        # Splits
        for i, num in enumerate(state):
            for a, b in get_valid_splits(num, max_value):
                new_state = list(state[:i]) + [a, b] + list(state[i+1:])
                if len(set(new_state)) == len(new_state):
                    next_states.append(new_state)
        
        # Merges
        for i, merged in get_valid_merges(state, max_value):
            new_state = list(state[:i]) + [merged] + list(state[i+2:])
            if len(set(new_state)) == len(new_state):
                next_states.append(new_state)
        
        # Shuffle expansions to add non-determinism
        random.shuffle(next_states)
        
        # Push each new state into the priority queue with a random offset
        for new_state in next_states:
            cost = steps + 1 + heuristic(new_state, target)
            cost += random.uniform(0, randomness)
            heapq.heappush(
                pq,
                (cost, steps + 1, tuple(new_state), path + [(state, tuple(new_state))])
            )
    
    return None

def probabilistic_beam_search(initial, target, beam_width=5, temperature=1.0):
    """
    (3) Beam Search with probabilistic selection (softmax).
    """
    max_value = max(initial)
    target_tuple = tuple(target)
    
    # Each item is (steps, state, path)
    current_beam = [(0, tuple(initial), [])]
    visited = set()
    
    while current_beam:
        next_beam = []
        
        for steps, state, path in current_beam:
            if state == target_tuple:
                return path
            if state in visited:
                continue
            visited.add(state)
            
            # Generate possible splits
            for i, num in enumerate(state):
                for a, b in get_valid_splits(num, max_value):
                    new_state = list(state[:i]) + [a, b] + list(state[i+1:])
                    if len(set(new_state)) == len(new_state):
                        new_steps = steps + 1
                        new_cost = new_steps + heuristic(new_state, target)
                        next_beam.append((new_cost, new_steps, tuple(new_state),
                                          path + [(state, tuple(new_state))]))
            
            # Generate possible merges
            for i, merged in get_valid_merges(state, max_value):
                new_state = list(state[:i]) + [merged] + list(state[i+2:])
                if len(set(new_state)) == len(new_state):
                    new_steps = steps + 1
                    new_cost = new_steps + heuristic(new_state, target)
                    next_beam.append((new_cost, new_steps, tuple(new_state),
                                      path + [(state, tuple(new_state))]))
        
        if not next_beam:
            break
        
        # Convert costs to probabilities using softmax of -cost
        costs = np.array([item[0] for item in next_beam], dtype=float)
        probs = np.exp(-costs / temperature)
        probs /= probs.sum()
        
        # Sample up to beam_width states weighted by these probabilities
        indices = np.random.choice(
            len(next_beam),
            size=min(beam_width, len(next_beam)),
            replace=False,
            p=probs
        )
        
        new_current_beam = []
        for idx in indices:
            cost, steps, st, pth = next_beam[idx]
            new_current_beam.append((steps, st, pth))
        
        current_beam = new_current_beam
    
    return None

# ---

def do_random_walk(initial_state, steps, max_value):
    """
    Perform a random walk for 'steps' moves from 'initial_state',
    returning (final_state, walk_path).
    'walk_path' is list of (old_state, new_state).
    """
    state = list(initial_state)
    path = []
    
    for _ in range(steps):
        # Gather all valid next states
        next_states = []
        
        # Splits
        for i, num in enumerate(state):
            for a, b in get_valid_splits(num, max_value):
                new_state = list(state[:i]) + [a, b] + list(state[i+1:])
                if len(set(new_state)) == len(new_state):
                    next_states.append(new_state)
        
        # Merges
        for i, merged in get_valid_merges(state, max_value):
            new_state = list(state[:i]) + [merged] + list(state[i+2:])
            if len(set(new_state)) == len(new_state):
                next_states.append(new_state)
        
        if not next_states:
            break
        
        # Pick one random next state
        new_state = random.choice(next_states)
        path.append((tuple(state), tuple(new_state)))
        state = new_state
    
    return tuple(state), path

def hybrid_guided_random_walk_search(initial, target, random_steps=3, attempts=5):
    """
    (4) Hybrid Approach: 
        - Perform multiple random walks from 'initial' for 'random_steps' each
        - Then pick each vantage state and run A* to find a path to 'target'.
        - Return the overall shortest successful path if any.
    """
    max_value = max(initial)
    best_solution = None
    
    for _ in range(attempts):
        vantage_state, random_path = do_random_walk(initial, random_steps, max_value)
        
        if vantage_state == tuple(target):
            # If random walk already reached target
            return random_path
        
        # Now run A* (or any other method) from vantage_state to target
        a_star_solution = find_shortest_solution(list(vantage_state), target)
        
        if a_star_solution is not None:
            # Combine the random walk path + the A* path
            full_path = random_path + a_star_solution
            if best_solution is None or len(full_path) < len(best_solution):
                best_solution = full_path
    
    return best_solution

# ---

def is_valid_initial_state(state):
    return all(isinstance(x, int) and x > 0 for x in state) and len(state) == len(set(state))

def get_user_defined_state():
    while True:
        try:
            user_input = input("Enter a list of unique, positive integers separated by spaces: ")
            state = list(map(int, user_input.split()))
            if is_valid_initial_state(state):
                return state
            else:
                print("Invalid input. Ensure all numbers are unique and positive integers.")
        except ValueError:
            print("Invalid input. Please enter only integers.")

def main():
    print("Choose method to solve:")
    print("1) Original A* (Deterministic)")
    print("2) Randomness to State Expansion (Non-Deterministic Beam Search)")
    print("3) Probabilistic Beam Search (Softmax-based)")
    print("4) Hybrid Approach: Guided Random Walk + Search")
    
    method = input("Enter your choice (1, 2, 3, or 4): ").strip()
    
    # Let the user enter the initial state
    initial_state = get_user_defined_state()
    target_state = list(reversed(initial_state))
    
    if method == "2":
        try:
            randomness = float(input("Enter a randomness factor (e.g., 0.1): "))
        except ValueError:
            randomness = 0.1
        solution = find_shortest_solution_with_randomness(initial_state, target_state, randomness)
    
    elif method == "3":
        try:
            beam_width = int(input("Enter beam width (e.g., 5): "))
        except ValueError:
            beam_width = 5
        try:
            temperature = float(input("Enter temperature (e.g., 1.0): "))
        except ValueError:
            temperature = 1.0
        solution = probabilistic_beam_search(initial_state, target_state, beam_width, temperature)
    
    elif method == "4":
        try:
            random_steps = int(input("Enter number of random steps (e.g., 3): "))
        except ValueError:
            random_steps = 3
        try:
            attempts = int(input("Enter number of random-walk attempts (e.g., 5): "))
        except ValueError:
            attempts = 5
        solution = hybrid_guided_random_walk_search(initial_state, target_state, random_steps, attempts)
    
    else:
        solution = find_shortest_solution(initial_state, target_state)
    
    print(f"Initial state: {initial_state}")
    print(f"Target state: {target_state}")
    
    if solution:
        print("Solution found:")
        for step_num, (_, new_state) in enumerate(solution, start=1):
            print(f"{step_num}: {list(new_state)}")
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
