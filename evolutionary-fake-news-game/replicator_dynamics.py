# файл: replicator_dynamics.py
import random
from collections import Counter
from payoff import get_payoff

def update_strategies(graph, strategies):
    new_strategies = strategies.copy()
    for node in graph.nodes():
        neighbors = list(graph.neighbors(node))
        if not neighbors:
            continue

        current_strategy = strategies[node]
        current_payoff = get_payoff(current_strategy)

        neighbor_payoffs = [(n, get_payoff(strategies[n])) for n in neighbors]
        total = sum(payoff for _, payoff in neighbor_payoffs)
        if total == 0:
            continue

        probabilities = [payoff / total for _, payoff in neighbor_payoffs]
        chosen_neighbor = random.choices([n for n, _ in neighbor_payoffs], weights=probabilities)[0]
        new_strategies[node] = strategies[chosen_neighbor]

    return new_strategies
