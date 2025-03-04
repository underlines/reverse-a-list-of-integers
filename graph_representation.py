# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "matplotlib",
#   "networkx"
# ]
# ///

import networkx as nx
import matplotlib.pyplot as plt
import re

def parse_game_runs(input_text):
    game_runs = []
    current_run = {}
    for line in input_text.strip().split("\n"):
        if line.startswith("0: ") and current_run:
            game_runs.append(current_run)
            current_run = {}
        match = re.match(r'(\d+): (\[.*\])', line)
        if match:
            step, state = int(match.group(1)), eval(match.group(2))
            current_run[step] = state
    if current_run:
        game_runs.append(current_run)
    return game_runs

def detect_move_type(prev_state, new_state):
    if len(new_state) > len(prev_state):
        return "split"
    elif len(new_state) < len(prev_state):
        return "combine"
    return ""

def plot_game_graph(game_runs, output_filename="game_graph.png"):
    G = nx.DiGraph()
    initial_states = set()
    final_states = set()
    
    for run_idx, game_run in enumerate(game_runs):
        prev_step = None
        steps = list(game_run.keys())
        initial_states.add(str(game_run[steps[0]]))
        final_states.add(str(game_run[steps[-1]]))
        
        for step, state in game_run.items():
            state_label = str(state)
            G.add_node(state_label, label=state_label)
            if prev_step is not None:
                prev_label = str(game_run[prev_step])
                move_type = detect_move_type(game_run[prev_step], state)
                G.add_edge(prev_label, state_label, label=move_type)
            prev_step = step

    # Try using Graphviz's layout if available
    try:
        from networkx.drawing.nx_agraph import graphviz_layout
        pos = graphviz_layout(G, prog="dot")  # More readable hierarchical layout
    except ImportError:
        pos = nx.spring_layout(G, k=0.8)  # Fallback to spring layout with adjusted spacing

    plt.figure(figsize=(12, 8))
    node_colors = ["blue" if node in initial_states else "green" if node in final_states else "lightblue" for node in G.nodes()]
    
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color=node_colors, edge_color="gray", font_size=10, edgecolors="black")
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10)
    plt.title("Reverse Unique Integers Game Graph")
    plt.savefig(output_filename, format='png')
    plt.close()

# Example Input
input_text = """
0: [12, 4, 9]
1: [12, 4, 3, 6]
2: [5, 7, 4, 3, 6]
3: [12, 4, 3, 6]
4: [5, 7, 4, 3, 6]
5: [5, 11, 3, 6]
6: [5, 4, 7, 3, 6]
7: [5, 4, 10, 6]
8: [9, 10, 6]
9: [9, 10, 1, 5]
10: [9, 4, 6, 1, 5]
11: [9, 4, 7, 5]
12: [9, 4, 12]

0: [12, 4, 9]
1: [12, 1, 3, 9]
2: [4, 8, 1, 3, 9]
3: [4, 8, 1, 12]
4: [4, 3, 5, 1, 12]
5: [7, 5, 1, 12]
6: [7, 2, 3, 1, 12]
7: [9, 3, 1, 12]
8: [9, 4, 12]

0: [12, 4, 9]
1: [5, 7, 4, 9]
2: [5, 7, 4, 3, 6]
3: [12, 4, 3, 6]
4: [5, 7, 4, 3, 6]
5: [5, 11, 3, 6]
6: [5, 4, 7, 3, 6]
7: [5, 4, 10, 6]
8: [9, 10, 6]
9: [9, 10, 1, 5]
10: [9, 4, 6, 1, 5]
11: [9, 4, 7, 5]
12: [9, 4, 12]
"""

game_runs = parse_game_runs(input_text)
plot_game_graph(game_runs, "game_graph.png")
