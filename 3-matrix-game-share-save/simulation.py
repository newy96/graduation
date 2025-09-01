# simulation.py
# Симулация на игра между стратегии + турнир всички-срещу-всички.

from typing import Dict, Tuple, List
from strategies import STRATEGIES
from payoff import get_payoff


def simulate_game(strategy1_name: str, strategy2_name: str, rounds: int = 10) -> Tuple[int, int]:
    """Симулация на многократна игра между две стратегии (сумирани точки за rounds)."""
    strat1 = STRATEGIES[strategy1_name]
    strat2 = STRATEGIES[strategy2_name]

    history1: List[str] = []
    history2: List[str] = []
    score1, score2 = 0, 0

    for _ in range(rounds):
        move1 = strat1(history1, history2)
        move2 = strat2(history2, history1)
        u1, u2 = get_payoff(move1, move2)
        score1 += u1
        score2 += u2
        history1.append(move1)
        history2.append(move2)

    return score1, score2

def run_all_pairings(rounds: int = 10) -> Dict[str, Dict[str, Tuple[int, int]]]:
    """
    Пуска всички двойки стратегии и връща вложен речник:
    results[strat1][strat2] = (score1, score2)
    """
    names = list(STRATEGIES.keys())
    results: Dict[str, Dict[str, Tuple[int, int]]] = {n: {} for n in names}

    print("=== Резултати от симулацията ===\n")
    for n1 in names:
        for n2 in names:
            s1, s2 = simulate_game(n1, n2, rounds)
            results[n1][n2] = (s1, s2)
            print(f"{n1} vs {n2} → Играч 1: {s1} | Играч 2: {s2}")
    return results
