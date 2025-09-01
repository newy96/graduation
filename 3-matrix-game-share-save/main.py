# main.py
# Примерна входна точка: базова симулация + визуализация.

from simulation import run_all_pairings
from analysis import plot_bar, compute_best_responses, pretty_print_br
from payoff import get_current_payoff_matrix

def main() -> None:
    # Базова симулация по Таблица 1
    results = run_all_pairings(rounds=10)
    plot_bar(results, player=1, title="Базова матрица — Играч 1")
    # Ако искаш и за Играч 2:
    # plot_bar(results, player=2, title="Базова матрица — Играч 2")

    # Показваме най-добрите отговори (BR) за базовата матрица – полезно за NE
    matrix = get_current_payoff_matrix()
    br1, br2 = compute_best_responses(matrix)
    pretty_print_br(br1, br2, label="(база)")

if __name__ == "__main__":
    main()
