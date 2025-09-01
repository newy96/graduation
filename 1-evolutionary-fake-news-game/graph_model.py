import networkx as nx
import random

# Генериране на графа
def generate_social_graph(n=50, min_neighbors=3, max_neighbors=6):
    G = nx.Graph()
    G.add_nodes_from(range(n))

    for node in G.nodes():
        num_neighbors = random.randint(min_neighbors, max_neighbors)
        neighbors = random.sample([n for n in G.nodes() if n != node], num_neighbors)
        for neighbor in neighbors:
            G.add_edge(node, neighbor)

    return G
