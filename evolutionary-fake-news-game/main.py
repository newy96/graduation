# main.py

import networkx as nx
import random
from collections import Counter
import matplotlib.pyplot as plt

from payoff import PAYOFF_MATRIX
from replicator_dynamics import update_strategies

# Стъпка 1: Създаване на графа
def create_social_network(num_nodes=50, min_degree=3, max_degree=6):
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    for node in G.nodes():
        num_edges = random.randint(min_degree, max_degree)
        while G.degree[node] < num_edges:
            neighbor = random.randint(0, num_nodes - 1)
            if neighbor != node and not G.has_edge(node, neighbor):
                G.add_edge(node, neighbor)
    return G

# Стъпка 2: Инициализиране на стратегии
def initialize_strategies(G):
    strategies = {}
    choices = list(PAYOFF_MATRIX.keys())  # ['Share', 'Ignore', 'Report']
    for node in G.nodes():
        strategies[node] = random.choice(choices)
    return strategies

# Стъпка 3: Стартиране на симулацията
def run_simulation(G, strategies, iterations=10):
    for i in range(iterations):
        print(f"\n--- Итерация {i + 1} ---")
        count = Counter(strategies.values())
        print("Стратегии:", count)
        strategies = update_strategies(G, strategies)
    return strategies

# Стъпка 4: Визуализация (по избор)
def visualize_graph(G, strategies):
    color_map = {'Share': 'blue', 'Ignore': 'gray', 'Report': 'green'}
    node_colors = [color_map[strategies[node]] for node in G.nodes()]
    nx.draw(G, with_labels=False, node_color=node_colors, node_size=100)
    plt.title("Оцветяване на мрежата по стратегии")
    plt.show()

# Основен блок
if __name__ == "__main__":
    G = create_social_network()
    strategies = initialize_strategies(G)

    final_strategies = run_simulation(G, strategies, iterations=10)
    print("\nФинално разпределение:", Counter(final_strategies.values()))

    # Покажи графиката
    visualize_graph(G, final_strategies)
