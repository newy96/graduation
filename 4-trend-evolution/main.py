# main.py
import random
from collections import Counter
from network import make_small_world
from strategies import TYPES, ACTIONS
from simulation import run_simulation
from plots import (
    plot_strategies, plot_actions, plot_exposed_and_fitness,
    summarize_history, save_summary_to_csv,
    draw_network_by_type, draw_network_by_action
)

def initialize(G, seed_count=5, rng=None):
    """Инициализация: (1) разпределя типове приблизително равномерно; (2) сийдове."""
    rng = rng or random
    # 1) типове (равномерно)
    types = {}
    per = len(G) // len(TYPES)
    pool = []
    for t in TYPES:
        pool += [t] * per
    while len(pool) < len(G):
        pool.append(rng.choice(TYPES))
    # За детерминизъм: фиксиран ред по nodes() + фиксиран rng
    for i, node in enumerate(G.nodes()):
        types[node] = pool[i]

    # 2) начална експозиция/действие
    exposure = {node: False for node in G.nodes()}
    actions = {node: None for node in G.nodes()}

    # избираме seed_count възли с най-голяма степен
    deg_sorted = sorted(G.degree, key=lambda kv: kv[1], reverse=True)
    seeds = [node for node, _d in deg_sorted[:seed_count]]
    for s in seeds:
        exposure[s] = True
        actions[s] = "Share"  # палим тренда

    return types, exposure, actions

def main():
    # Единен RNG за възпроизводимост
    rng = random.Random(42)
    random.seed(42)

    # Baseline параметри (консистентни с exposure.py и payoff.py)
    params = dict(
        rho0=0.15,
        algo_local_threshold=0.40,   # q
        exp_boost_mult=1.50,         # boost за ЕКСПОЗИЦИЯТА (не е alpha)
        base_comment=3.0,
        base_share=2.0,
        base_ignore=0.0,
        local_bonus_per_reacted=0.5,
        local_bonus_cap=3.0,         # cap = +3.0
        utility_boost_alpha=3.0,     # α = +3.0 към ПОЛЕЗНОСТТА
        skeptic_tau=0.30,
        beta=1.0,
        epsilon=0.01,                # малък шум
        rng=rng,                     # подаваме RNG към exposure/fermi
    )

    # Мрежа и инициализация
    G = make_small_world(n=100, k=8, p=0.1, seed=42)
    types0, exposure0, actions0 = initialize(G, seed_count=5, rng=rng)

    # Симулация
    T = 30
    typesT, exposureT, actionsT, history = run_simulation(
        G, types0, exposure0, actions0, T=T, params=params
    )

    # Метрики
    summary = summarize_history(history, levels=(0.5, 0.8, 0.95), plateau_eps=0.01, plateau_k=3)

    # Конзолен отчет
    print("Финално разпределение на типове:", dict(Counter(typesT.values())))
    print("Финално разпределение на действия:", dict(Counter(a for a in actionsT.values() if a)))
    print("\n--- Метрики за обобщение ---")
    for k, v in summary.items():
        print(f"{k}: {v}")

    # По желание: запиши в CSV за директно вмъкване в дипломната
    save_summary_to_csv(summary, path="figures/summary_metrics.csv")

    # Графики + запис
    plot_strategies(history, save=True, path="figures/FigA_strategies.png")
    plot_actions(history, save=True, path="figures/FigB_actions.png")
    plot_exposed_and_fitness(history, save=True, path_prefix="figures/FigC")

    # Мрежови визуализации (след последния рунд)
    draw_network_by_type(G, typesT, title=f"Мрежа по тип (след T={T})")
    draw_network_by_action(G, actionsT, title=f"Мрежа по действие (след T={T})")

if __name__ == "__main__":
    main()
