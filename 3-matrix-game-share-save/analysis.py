# analysis.py
import numpy as np
import matplotlib.pyplot as plt

from simulation import run_all_pairings
from payoff import get_current_payoff_matrix

ACTIONS = ["Share", "Save", "Comment"]

def plot_bar(results, player: int = 1, title: str | None = None) -> None:
    """
    Стълбовидна диаграма за резултатите на даден играч.
    """
    names = list(results.keys())
    idx = 0 if player == 1 else 1

    pairs = []
    values = []
    for r in names:
        for c in names:
            pairs.append(f"{r}-{c}")
            values.append(results[r][c][idx])

    plt.figure(figsize=(9, 5))
    bars = plt.bar(pairs, values, color="skyblue", edgecolor="black")
    plt.xticks(rotation=45, ha="right")
    plt.ylabel(f"Полезност (Играч {player})")
    plt.title(title or f"Резултати по двойки стратегии (Играч {player})")

    # маркираме максимум(и) с друг цвят
    max_val = max(values)
    for bar, val in zip(bars, values):
        if val == max_val:
            bar.set_color("orange")

    plt.tight_layout()
    plt.show()

def compute_best_responses(matrix):
    """
    Връща BR1 и BR2 като речници:
    - BR1[col_action] = най-добрият ред (действие на Играч 1) срещу действието на Играч 2
    - BR2[row_action] = най-добрият стълб (действие на Играч 2) срещу действието на Играч 1
    """
    # BR1: за всяко действие на Играч 2 търсим реда с макс полезност за Играч 1
    br1 = {}
    for a2 in ACTIONS:
        best_a1 = max(ACTIONS, key=lambda a1: matrix[(a1, a2)][0])
        br1[a2] = best_a1

    # BR2: за всяко действие на Играч 1 търсим колоната с макс полезност за Играч 2
    br2 = {}
    for a1 in ACTIONS:
        best_a2 = max(ACTIONS, key=lambda a2: matrix[(a1, a2)][1])
        br2[a1] = best_a2

    return br1, br2

def pretty_print_br(br1, br2, label=""):
    print(f"\n--- Най-добри отговори {label} ---")
    print("BR1 (срещу действие на Играч 2):")
    for a2, a1 in br1.items():
        print(f"  ако Играч 2 избере {a2:>7} → Играч 1 най-добре {a1}")
    print("BR2 (срещу действие на Играч 1):")
    for a1, a2 in br2.items():
        print(f"  ако Играч 1 избере {a1:>7} → Играч 2 най-добре {a2}")
