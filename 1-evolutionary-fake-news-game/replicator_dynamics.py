# replicator_dynamics.py
import random
import math
from payoff import node_payoff

def update_strategies(G, strategies, beta: float = 1.0):
    """
    Една синхронна стъпка на имитационна репликаторна динамика.
    1) изчисляваме фитнес f_i за всички възли (сума срещу съседите);
    2) всеки възел избира случаен съсед j;
    3) приема неговата стратегия с вероятност 1/(1+exp(-(f_j - f_i)*beta)).
    """
    # 1) фитнеси за текущия профил на стратегиите
    fitness = {i: node_payoff(G, strategies, i) for i in G.nodes()}

    new_strategies = strategies.copy()

    for i in G.nodes():
        neigh = list(G.neighbors(i))
        if not neigh:
            continue

        j = random.choice(neigh)            # съсед за сравнение
        fi = fitness[i]
        fj = fitness[j]

        # 2) Fermi-вероятност за приемане на стратегията на j
        p_adopt = 1.0 / (1.0 + math.exp(-(fj - fi) * beta))

        if random.random() < p_adopt:
            new_strategies[i] = strategies[j]

    return new_strategies
