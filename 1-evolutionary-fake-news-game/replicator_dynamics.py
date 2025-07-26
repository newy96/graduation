import random
from payoff import get_payoff

def update_strategies(graph, strategies):
    new_strategies = strategies.copy()

    # 1. Преглежда всеки възел от графа.
    for node in graph.nodes():
        neighbors = list(graph.neighbors(node))
        if not neighbors:
            continue  # Ако няма съседи, пропускаме

        current_strategy = strategies[node]
        current_payoff = get_payoff(current_strategy)

        # 2. Сравнява неговата стратегия с тези на съседите.
        neighbor_payoffs = [(n, get_payoff(strategies[n])) for n in neighbors]
        total = sum(payoff for _, payoff in neighbor_payoffs)
        if total == 0:
            continue  # Ако всички съседи имат 0 печалба, няма как да изберем

        # 3. Избира съсед с вероятност, пропорционална на текущата му печалба.
        probabilities = [payoff / total for _, payoff in neighbor_payoffs]
        chosen_neighbor = random.choices(
            [n for n, _ in neighbor_payoffs],
            weights=probabilities
        )[0]

        # 4. Приема стратегията на избрания съсед.
        new_strategies[node] = strategies[chosen_neighbor]

    return new_strategies
