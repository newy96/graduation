# main.py - Основен скрипт за симулация на еволюционната игра
import networkx as nx
import random
from collections import Counter
import matplotlib.pyplot as plt

from plots import plot_strategy_frequencies, plot_avg_fitness
from payoff import ACTIONS, node_payoff
from replicator_dynamics import update_strategies

def create_social_network(num_nodes=50, min_degree=3, max_degree=6):
    G = nx.Graph()
    G.add_nodes_from(range(num_nodes))
    for node in G.nodes():
        target_deg = random.randint(min_degree, max_degree)
        while G.degree[node] < target_deg:
            nb = random.randint(0, num_nodes - 1)
            if nb != node and not G.has_edge(node, nb):
                G.add_edge(node, nb)
    return G

def initialize_strategies(G):
    return {node: random.choice(ACTIONS) for node in G.nodes()}

def avg_fitness(G, strategies):
    return sum(node_payoff(G, strategies, i) for i in G.nodes()) / G.number_of_nodes()

def run_simulation(G, strategies, iterations=20, beta=1.0):
    history = []
    for t in range(1, iterations + 1):
        counts = Counter(strategies.values())
        mean_fit = avg_fitness(G, strategies)
        print(f"\n--- Итерация {t} ---")
        print("Честоти:", dict(counts))
        print(f"Средна успеваемост ȳ = {mean_fit:.3f}")
        history.append((counts, mean_fit))

        strategies = update_strategies(G, strategies, beta=beta)
    return strategies, history

def visualize_graph(G, strategies):
    color_map = {'Share': 'tab:blue', 'Ignore': 'tab:gray', 'Report': 'tab:green'}
    node_colors = [color_map[strategies[v]] for v in G.nodes()]
    pos = nx.spring_layout(G, seed=42)
    nx.draw(G, pos, with_labels=False, node_color=node_colors, node_size=90, edge_color="#cccccc")
    plt.title("Мрежа, оцветена по стратегия")
    plt.show()

if __name__ == "__main__":
    G = create_social_network()
    strategies = initialize_strategies(G)

    final_strategies, history = run_simulation(G, strategies, iterations=20, beta=1.0)
    print("\nФинално разпределение:", Counter(final_strategies.values()))

    # Фигури „динамика във времето“
    plot_strategy_frequencies(history)
    plot_avg_fitness(history)

    # По избор: рисунка на мрежата
    visualize_graph(G, final_strategies)
