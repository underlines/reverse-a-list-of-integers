# This script runs all solvers and compares their performance.
from game import PuzzleGame
from solvers.brute_force import BruteForceSolver
from solvers.bfs_solver import BFSSolver
from solvers.bfs_solver_improved import BFSSolverImproved
from solvers.hybrid_solver import HybridSolver


def run_solvers(initial_list):
    game = PuzzleGame(initial_list)
    
    solvers = {
        "Brute Force": BruteForceSolver(),
        "BFS Solver": BFSSolver(),
        "BFS Solver Improved": BFSSolverImproved(),
        "Hybrid Solver": HybridSolver(),
    }

    results = []
    for name, solver in solvers.items():
        print(f"Running {name} solver...")
        solution, time_taken = game.play(solver)
        if solution:
            moves = len(solution) - 1
            results.append((name, moves, time_taken, solution))
        else:
            print(f"{name} failed to find a solution.")

    print("\nSolver Comparison:")
    results.sort(key=lambda x: x[1])  # Sort by least moves
    for name, moves, time_taken, solution in results:
        print(f"\n{name}: {moves} moves, {time_taken:.4f} seconds")
        print("Solution steps:")
        for i, step in enumerate(solution):
            print(f"{i}: {step}")

if __name__ == "__main__":
    initial_list = [5, 3, 9] # (optimum 4)
    # initial_list = [3, 12, 7, 9]
    # initial_list = [4, 9, 5]
    run_solvers(initial_list)
