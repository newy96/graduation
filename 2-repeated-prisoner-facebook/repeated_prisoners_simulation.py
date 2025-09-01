import random
from collections import defaultdict

# ----- ДЕЙСТВИЯ -----
ACTIONS = ["Like", "Ignore", "Comment"]

# ----- PAYOFF МАТРИЦА (симетрична) -----
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

# ----- СТРАТЕГИИ -----
def tit_for_tat(my_history, opp_history):
    return opp_history[-1] if opp_history else "Like"

def always_cooperate(*_):
    return random.choice(["Like", "Comment"])

def always_defect(*_):
    return "Ignore"

def random_strategy(*_):
    return random.choice(ACTIONS)

STRATEGIES = {
    "Tit-for-Tat": tit_for_tat,
    "Always Cooperate": always_cooperate,
    "Always Defect": always_defect,
    "Random": random_strategy
}

# ----- ДВУИГРАЧНА СИМУЛАЦИЯ -----
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

def run_all_pairings(rounds=10):
    results = defaultdict(dict)
    names = list(STRATEGIES.keys())
    print("=== Резултати от симулацията ===\n")
    for i in range(len(names)):
        for j in range(len(names)):
            n1, n2 = names[i], names[j]
            s1, s2 = simulate_game(n1, n2, rounds)
            results[n1][n2] = (s1, s2)
            print(f"{n1} vs {n2} → {s1} : {s2}")
    return results

# ----- ПОПУЛАЦИОНЕН ТУРНИР (N ИГРАЧИ) -----
def make_population(N=50, assignment="even"):
    names = list(STRATEGIES.keys())
    players = []
    if assignment == "even":
        per = N // len(names)
        pool = []
        for nm in names:
            pool += [nm] * per
        while len(pool) < N:
            pool.append(random.choice(names))
        random.shuffle(pool)
        for i in range(N):
            players.append({"id": i, "strategy": pool[i], "score": 0})
    else:
        for i in range(N):
            players.append({"id": i, "strategy": random.choice(names), "score": 0})
    return players

def form_random_pairs(players):
    ids = [p["id"] for p in players]
    random.shuffle(ids)
    pairs = []
    for k in range(0, len(ids) - 1, 2):
        pairs.append((ids[k], ids[k+1]))
    return pairs

def play_pair(players_dict, id1, id2, rounds_per_pair=10):
    name1 = players_dict[id1]["strategy"]
    name2 = players_dict[id2]["strategy"]
    strat1 = STRATEGIES[name1]
    strat2 = STRATEGIES[name2]
    history1, history2 = [], []
    s1, s2 = 0, 0
    for _ in range(rounds_per_pair):
        m1 = strat1(history1, history2)
        m2 = strat2(history2, history1)
        p1, p2 = PAYOFF_MATRIX[(m1, m2)]
        s1 += p1
        s2 += p2
        history1.append(m1)
        history2.append(m2)
    players_dict[id1]["score"] += s1
    players_dict[id2]["score"] += s2
    return s1, s2

def simulate_population_tournament(N=50, meta_rounds=10, rounds_per_pair=10, assignment="even", seed=42):
    random.seed(seed)
    players = make_population(N=N, assignment=assignment)
    players_dict = {p["id"]: p for p in players}
    for t in range(1, meta_rounds + 1):
        pairs = form_random_pairs(players)
        print(f"\n=== Мета-рунуд {t} | Двойки: {len(pairs)} ===")
        for (i, j) in pairs:
            s1, s2 = play_pair(players_dict, i, j, rounds_per_pair=rounds_per_pair)
            print(f"  {players_dict[i]['strategy']}({i}) vs {players_dict[j]['strategy']}({j}) -> {s1}:{s2}")

    from collections import defaultdict as _dd
    by_strategy = _dd(list)
    for p in players:
        by_strategy[p["strategy"]].append(p["score"])

    print("\n=== Обобщение по стратегия ===")
    for name, scores in by_strategy.items():
        total = sum(scores)
        avg = total / max(1, len(scores))
        print(f"{name}: общо={total}, средно на играч={avg:.2f}, брой играчи={len(scores)}")

    top5 = sorted(players, key=lambda x: x["score"], reverse=True)[:5]
    print("\n=== Топ 5 играчи ===")
    for p in top5:
        print(f"id={p['id']}, strat={p['strategy']}, score={p['score']}")

    return players, by_strategy

# ----- ЕДИНСТВЕНА ТОЧКА ЗА СТАРТ -----
# в зависимост от MODE-a се изпълнява различна логика в задачата
if __name__ == "__main__":
    random.seed(42)
    MODE = "population"  # "pairings" или "population"

    if MODE == "pairings":
        run_all_pairings(rounds=10)
    else:  # MODE == "population"
        simulate_population_tournament(
            N=50,
            meta_rounds=10,
            rounds_per_pair=10,
            assignment="even",
            seed=42
        )
