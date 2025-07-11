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

def fitness(graph, coloring):
    return sum(1 for node in graph for neighbor in graph[node] if coloring[node] == coloring[neighbor])

def create_individual(nodes, num_colors):
    return {node: random.randint(0, num_colors - 1) for node in nodes}

def crossover(parent1, parent2):
    child = {}
    for node in parent1:
        child[node] = parent1[node] if random.random() < 0.5 else parent2[node]
    return child

def mutate(individual, num_colors, mutation_rate=0.1):
    for node in individual:
        if random.random() < mutation_rate:
            individual[node] = random.randint(0, num_colors - 1)

def genetic_from_excel(filepath, population_size=50, generations=100, num_colors=5):
    df = pd.read_excel(filepath)
    graph = build_graph(df)
    nodes = list(graph.keys())

    population = [create_individual(nodes, num_colors) for _ in range(population_size)]

    for _ in range(generations):
        population.sort(key=lambda ind: fitness(graph, ind))
        if fitness(graph, population[0]) == 0:
            break

        next_gen = population[:10]
        while len(next_gen) < population_size:
            parent1 = random.choice(population[:25])
            parent2 = random.choice(population[:25])
            child = crossover(parent1, parent2)
            mutate(child, num_colors)
            next_gen.append(child)
        population = next_gen

    best = population[0]
    return [(panel, f"Slot_{color + 1}") for panel, color in best.items()]
