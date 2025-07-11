import pandas as pd
from collections import defaultdict

def greedy_from_excel(filepath):
    df = pd.read_excel(filepath)

    graph = defaultdict(set)
    for _, row in df.iterrows():
        a, b = row['Panel_1'], row['Panel_2']
        graph[a].add(b)
        graph[b].add(a)

    colors = {}
    for node in sorted(graph, key=lambda x: len(graph[x]), reverse=True):
        neighbor_colors = set(colors.get(neigh) for neigh in graph[node] if neigh in colors)
        for color in range(len(graph)):
            if color not in neighbor_colors:
                colors[node] = color
                break

    return [(panel, f"Slot_{color + 1}") for panel, color in colors.items()]
