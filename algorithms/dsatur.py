import pandas as pd
from collections import defaultdict

def dsatur_from_excel(filepath):
    df = pd.read_excel(filepath)

    graph = defaultdict(set)
    for _, row in df.iterrows():
        a, b = row['Panel_1'], row['Panel_2']
        graph[a].add(b)
        graph[b].add(a)

    colors = {}
    saturation = {node: 0 for node in graph}
    degrees = {node: len(neighbors) for node, neighbors in graph.items()}

    while len(colors) < len(graph):
        node = max((n for n in graph if n not in colors),
                   key=lambda x: (saturation[x], degrees[x]))

        neighbor_colors = set(colors.get(neigh) for neigh in graph[node] if neigh in colors)
        for color in range(len(graph)):
            if color not in neighbor_colors:
                colors[node] = color
                break

        for neigh in graph[node]:
            if neigh not in colors:
                saturation[neigh] = len(set(colors.get(n) for n in graph[neigh] if n in colors))

    return [(panel, f"Slot_{color + 1}") for panel, color in colors.items()]
