# plots.py
import matplotlib.pyplot as plt

def plot_strategy_frequencies(history, strategies=('Share', 'Ignore', 'Report')):
    """
    Чертае дела на стратегиите по итерации.
    history: списък от (Counter, mean_fit), връщан от run_simulation().
    """
    T = len(history)
    iters = list(range(1, T + 1))

    # Брой по итерации
    series = {s: [] for s in strategies}
    totals = []

    for counts, _ in history:
        total_now = sum(counts.values())
        totals.append(total_now)
        for s in strategies:
            series[s].append(counts.get(s, 0))

    # Дял (нормализираме по размер на популацията)
    shares = {s: [series[s][t] / totals[t] for t in range(T)] for s in strategies}

    plt.figure(figsize=(8, 5))
    for s in strategies:
        plt.plot(iters, shares[s], marker='o', linewidth=2, label=s)
    plt.xlabel("Итерация")
    plt.ylabel("Дял от популацията")
    plt.title("Динамика на стратегиите във времето")
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_avg_fitness(history):
    """Чертае средната успеваемост по итерации."""
    iters = list(range(1, len(history) + 1))
    avg_fit = [mean for _counts, mean in history]

    plt.figure(figsize=(8, 4.5))
    plt.plot(iters, avg_fit, marker='o', linewidth=2)
    plt.xlabel("Итерация")
    plt.ylabel("Средна успеваемост ȳ")
    plt.title("Еволюция на средната успеваемост")
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()
