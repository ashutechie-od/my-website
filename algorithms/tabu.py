import pandas as pd
from collections import defaultdict
import random

def build_graph(df):
    graph = defaultdict(set)
    for _, row in df.iterrows():
        a, b = row['Panel_1'], row['Panel_2']
        graph[a].add(b)
        graph[b].add(a)
    return graph

def cost(graph, coloring):
    return sum(1 for node in graph for neighbor in graph[node] if coloring[node] == coloring[neighbor])

def get_neighbors(graph, coloring):
    neighbors = []
    for node in graph:
        for color in range(len(graph)):
            if coloring[node] != color:
                new_coloring = coloring.copy()
                new_coloring[node] = color
                neighbors.append(new_coloring)
    return neighbors

def tabu_from_excel(filepath, max_iter=100, tabu_size=7):
    df = pd.read_excel(filepath)
    graph = build_graph(df)

    nodes = list(graph.keys())
    current = {node: random.randint(0, len(graph) - 1) for node in nodes}
    best = current.copy()
    best_cost = cost(graph, best)
    tabu_list = []

    for _ in range(max_iter):
        neighborhood = get_neighbors(graph, current)
        neighborhood = [n for n in neighborhood if n not in tabu_list]
        if not neighborhood:
            break

        neighbor = min(neighborhood, key=lambda n: cost(graph, n))
        current = neighbor
        current_cost = cost(graph, current)

        if current_cost < best_cost:
            best = current.copy()
            best_cost = current_cost

        tabu_list.append(current)
        if len(tabu_list) > tabu_size:
            tabu_list.pop(0)

    return [(panel, f"Slot_{slot + 1}") for panel, slot in best.items()]
