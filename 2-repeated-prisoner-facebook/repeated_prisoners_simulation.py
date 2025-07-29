import random
from collections import defaultdict

# Дефиниция на възможните действия
ACTIONS = ["Like", "Ignore", "Comment"]

# Матрица на полезностите (payoff) – симетрична
PAYOFF_MATRIX = {
    ("Like", "Like"): (2, 2),
    ("Like", "Ignore"): (0, 0),
    ("Like", "Comment"): (1, 2),
    ("Ignore", "Like"): (0, 0),
    ("Ignore", "Ignore"): (0, 0),
    ("Ignore", "Comment"): (-1, 1),
    ("Comment", "Like"): (2, 1),
    ("Comment", "Ignore"): (1, -1),
    ("Comment", "Comment"): (3, 3),
}

# Дефиниция на стратегиите
def tit_for_tat(my_history, opp_history):
    return opp_history[-1] if opp_history else "Like"

def always_cooperate(*_):
    return random.choice(["Like", "Comment"])

def always_defect(*_):
    return "Ignore"

def random_strategy(*_):
    return random.choice(ACTIONS)

# Свързване на стратегии по име
STRATEGIES = {
    "Tit-for-Tat": tit_for_tat,
    "Always Cooperate": always_cooperate,
    "Always Defect": always_defect,
    "Random": random_strategy
}

# Симулация на игра между две стратегии
def simulate_game(strategy1_name, strategy2_name, rounds=10):
    strat1 = STRATEGIES[strategy1_name]
    strat2 = STRATEGIES[strategy2_name]
    
    history1, history2 = [], []
    score1, score2 = 0, 0

    for _ in range(rounds):
        move1 = strat1(history1, history2)
        move2 = strat2(history2, history1)

        payoff1, payoff2 = PAYOFF_MATRIX[(move1, move2)]
        score1 += payoff1
        score2 += payoff2

        history1.append(move1)
        history2.append(move2)

    return score1, score2

# Стартиране на симулацията между всички двойки стратегии
def run_all_pairings(rounds=10):
    results = defaultdict(dict)
    strategy_names = list(STRATEGIES.keys())

    print("=== Резултати от симулацията ===\n")
    for i in range(len(strategy_names)):
        for j in range(len(strategy_names)):
            name1 = strategy_names[i]
            name2 = strategy_names[j]

            score1, score2 = simulate_game(name1, name2, rounds)
            results[name1][name2] = (score1, score2)

            print(f"{name1} vs {name2} → {score1} : {score2}")
    return results

if __name__ == "__main__":
    run_all_pairings(rounds=10)
