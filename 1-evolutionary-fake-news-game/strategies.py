import random
import networkx as nx
from graph_model import generate_social_graph

# Създаване на графа (50 възела със съседи между 3 и 6)
G = generate_social_graph()

# Дефиниция на стратегиите
strategies = ['Share', 'Ignore', 'Report']

# Начално присвояване на стратегии (на случаен принцип)
strategy_assignment = {}
for node in G.nodes():
    strategy_assignment[node] = random.choice(strategies)

# Стойности на ангажираност (payoff)
payoff_matrix = {
    'Share': 1.0,
    'Ignore': 0.1,
    'Report': 0.7
}

# Показване на първите 10 възела със стратегия
print("Начално разпределение на стратегии:")
for node in list(G.nodes())[:10]:
    print(f"Потребител {node}: {strategy_assignment[node]}")
