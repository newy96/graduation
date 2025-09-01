# plots.py
import os
import matplotlib.pyplot as plt
import networkx as nx

def _series_from_counts(history_list, keys):
    T = len(history_list)
    series = {k: [0] * T for k in keys}
    for t, cnt in enumerate(history_list):
        total = sum(cnt.values()) if cnt else 0
        for k in keys:
            series[k][t] = (cnt.get(k, 0) / total) if total > 0 else 0.0
    return series

def _get_exposed_series(history: dict):
    """Поддържа и двата ключа за съвместимост: exposed_ratio / exposed_share."""
    return history.get("exposed_ratio") or history.get("exposed_share") or []

def plot_strategies(history, keys=("Commentator","Conformist","Skeptic","FastSharer"),
                    save=False, path="figures/FigA_strategies.png"):
    series = _series_from_counts(history["strategy_counts"], keys)
    it = range(1, len(history["strategy_counts"]) + 1)
    plt.figure(figsize=(8, 5))
    for k in keys:
        plt.plot(it, series[k], marker='o', linewidth=2, label=k)
    plt.xlabel("Итерация"); plt.ylabel("Дял от популацията")
    plt.title("Динамика на стратегиите")
    plt.grid(True, alpha=0.3); plt.legend(); plt.tight_layout()
    if save:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.show()

def plot_actions(history, keys=("Share","Comment","Ignore"),
                 save=False, path="figures/FigB_actions.png"):
    series = _series_from_counts(history["action_counts"], keys)
    it = range(1, len(history["action_counts"]) + 1)
    plt.figure(figsize=(8, 5))
    for k in keys:
        plt.plot(it, series[k], marker='o', linewidth=2, label=k)
    plt.xlabel("Итерация"); plt.ylabel("Дял от действията (сред реагиралите)")
    plt.title("Динамика на действията")
    plt.grid(True, alpha=0.3); plt.legend(); plt.tight_layout()
    if save:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        plt.savefig(path, dpi=300, bbox_inches='tight')
    plt.show()

def plot_exposed_and_fitness(history, save=False, path_prefix="figures/FigC"):
    exposed = _get_exposed_series(history)
    it = range(1, len(exposed) + 1)

    # C1: експозиция
    plt.figure(figsize=(8, 4.5))
    plt.plot(it, exposed, marker='o', linewidth=2, label="Дял експонирани")
    plt.xlabel("Итерация"); plt.ylabel("Дял"); plt.title("Разпространение (експозиция)")
    plt.grid(True, alpha=0.3); plt.tight_layout()
    if save:
        os.makedirs(os.path.dirname(path_prefix), exist_ok=True)
        plt.savefig(f"{path_prefix}_exposed.png", dpi=300, bbox_inches='tight')
    plt.show()

    # C2: средна полезност
    it2 = range(1, len(history["mean_fitness"]) + 1)
    plt.figure(figsize=(8, 4.5))
    plt.plot(it2, history["mean_fitness"], marker='o', linewidth=2)
    plt.xlabel("Итерация"); plt.ylabel("Средна полезност")
    plt.title("Еволюция на средната полезност")
    plt.grid(True, alpha=0.3); plt.tight_layout()
    if save:
        os.makedirs(os.path.dirname(path_prefix), exist_ok=True)
        plt.savefig(f"{path_prefix}_fitness.png", dpi=300, bbox_inches='tight')
    plt.show()

# --- Метрики за обобщение ---

def summarize_history(history, levels=(0.5, 0.8, 0.95), plateau_eps=0.01, plateau_k=3):
    """
    Връща ключови метрики върху кривата на експозицията:
      - final_coverage
      - time_to_{L} за L в levels
      - peak_growth и peak_growth_iter
      - auc (средно покритие)
      - plateau_iter (по избор)
    """
    exposed = list(_get_exposed_series(history))
    T = len(exposed)
    if T == 0:
        return {}

    # 1) финално покритие
    final_coverage = exposed[-1]

    # 2) времена до нива (напр. 50%, 80%, 95%)
    times = {}
    for L in levels:
        tL = next((i + 1 for i, x in enumerate(exposed) if x >= L), None)
        times[f"time_to_{int(L * 100)}"] = tL

    # 3) пик на растеж
    diffs = [exposed[t] - exposed[t - 1] for t in range(1, T)]
    if diffs:
        peak_growth = max(diffs)
        peak_growth_iter = diffs.index(peak_growth) + 2  # +2: дифът е от t-1 към t (1-базирано)
    else:
        peak_growth, peak_growth_iter = 0.0, None

    # 4) AUC (средно покритие)
    auc = sum(exposed) / T

    # 5) плато (k последователни малки приращения)
    plateau_iter = None
    if len(diffs) >= plateau_k:
        for t in range(plateau_k - 1, len(diffs)):
            window = diffs[t - (plateau_k - 1): t + 1]
            if all(abs(d) <= plateau_eps for d in window):
                plateau_iter = t + 1  # 1-базиран индекс на "текущата" итерация
                break

    summary = {
        "final_coverage": final_coverage,
        "auc": auc,
        "peak_growth": peak_growth,
        "peak_growth_iter": peak_growth_iter,
        "plateau_iter": plateau_iter,
        **times
    }
    return summary

def save_summary_to_csv(summary: dict, path="figures/summary_metrics.csv"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    import csv
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["metric", "value"])
        for k, v in summary.items():
            writer.writerow([k, v])

def draw_network_by_type(G, types, title="Мрежа по тип (стратегия)"):
    color_map = {
        "Commentator": "tab:orange",
        "Conformist":  "tab:blue",
        "Skeptic":     "tab:gray",
        "FastSharer":  "tab:green",
    }
    pos = nx.spring_layout(G, seed=42)
    node_colors = [color_map.get(types[v], "tab:red") for v in G.nodes()]
    nx.draw(G, pos, node_color=node_colors, node_size=80, edge_color="#cccccc", with_labels=False)
    plt.title(title); plt.tight_layout(); plt.show()

def draw_network_by_action(G, actions, title="Мрежа по действие (последен рунд)"):
    color_map = {"Share": "tab:blue", "Comment": "tab:orange", "Ignore": "tab:gray", None: "#dddddd"}
    pos = nx.spring_layout(G, seed=42)
    node_colors = [color_map.get(actions[v], "#dddddd") for v in G.nodes()]
    nx.draw(G, pos, node_color=node_colors, node_size=80, edge_color="#cccccc", with_labels=False)
    plt.title(title); plt.tight_layout(); plt.show()
