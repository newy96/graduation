# simulation.py
import random
import math
from collections import Counter
from strategies import ACTIONS, TYPES, decide_action
from exposure import update_exposure
from payoff import compute_fitness

def fermi_imitation(G, types_t, fitness, beta=1.0, epsilon=0.0, rng=None):
    """
    Имитация по правило на Fermi: i сравнява със случаен съсед j.
    Приема стратегията на j с вероятност 1/(1+exp(-(f_j - f_i)*beta)).
    epsilon – малък шум (мутация).
    """
    rng = rng or random
    new_types = types_t.copy()
    for i in G.nodes():
        neigh = list(G.neighbors(i))
        if not neigh:
            continue
        j = rng.choice(neigh)
        fi, fj = fitness.get(i, 0.0), fitness.get(j, 0.0)
        p = 1.0 / (1.0 + math.exp(-(fj - fi) * beta))
        if rng.random() < p:
            new_types[i] = types_t[j]
        # малка случайна промяна (мутация)
        if epsilon > 0 and rng.random() < epsilon:
            # по желание: не мутирай към същия тип
            candidates = [t for t in TYPES if t != new_types[i]] or TYPES
            new_types[i] = rng.choice(candidates)
    return new_types

def one_step(G, types_t, exposure_t, actions_t, params):
    """
    Една стъпка: 1) експозиция t+1; 2) действия t+1; 3) фитнес(t+1); 4) еволюция към t+1.
    Връща (types_{t+1}, exposure_{t+1}, actions_{t+1}, fitness_{t+1}).
    """
    rng = params.get("rng")

    # 1) експозиция (персистентна)
    exposure_next = update_exposure(G, exposure_t, actions_t, params)

    # 2) действия (на база експозиция и тип)
    actions_next = {}
    for i in G.nodes():
        exposed_now = exposure_next.get(i, False)
        actions_next[i] = decide_action(types_t[i], i, G, actions_t, exposed_now, params)

    # 3) фитнес за текущия рунд (по действията t+1)
    fitness = compute_fitness(G, actions_next, params)

    # 4) еволюция (Fermi)
    beta = params.get("beta", 1.0)
    epsilon = params.get("epsilon", 0.0)
    types_next = fermi_imitation(G, types_t, fitness, beta=beta, epsilon=epsilon, rng=rng)

    return types_next, exposure_next, actions_next, fitness

def run_simulation(G, types_0, exposure_0, actions_0, T=30, params=None):
    """
    Върти T стъпки и връща история за графики и анализ.
    """
    params = params or {}
    types, exposure, actions = types_0, exposure_0, actions_0

    history = {
        "strategy_counts": [],  # Counter по тип
        "action_counts":   [],  # Counter по действие
        "exposed_ratio":   [],  # дял експонирани
        "mean_fitness":    []   # средна полезност
    }

    for _ in range(T):
        types, exposure, actions, fitness = one_step(G, types, exposure, actions, params)

        sc = Counter(types.values())
        ac = Counter(a for a in actions.values() if a is not None)

        # нормализирай броячите за стабилни графики (по желание)
        for a in ACTIONS:
            ac.setdefault(a, 0)
        for t in TYPES:
            sc.setdefault(t, 0)

        exposed_ratio = sum(1 for v in exposure.values() if v) / G.number_of_nodes()
        mean_fit = (sum(fitness.values()) / G.number_of_nodes()) if fitness else 0.0

        history["strategy_counts"].append(sc)
        history["action_counts"].append(ac)
        history["exposed_ratio"].append(exposed_ratio)
        history["mean_fitness"].append(mean_fit)

    return types, exposure, actions, history
