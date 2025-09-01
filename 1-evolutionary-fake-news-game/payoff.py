# 3x3 PAYOFF_MATRIX, с новите стратегии (Share, Ignore, Report)
PAYOFF_MATRIX = {
    ('Share', 'Share'):  (1.0, 1.0),
    ('Share', 'Ignore'): (1.0, 0.1),
    ('Share', 'Report'): (1.0, 0.7),

    ('Ignore', 'Share'):  (0.1, 1.0),
    ('Ignore', 'Ignore'): (0.1, 0.1),
    ('Ignore', 'Report'): (0.1, 0.7),

    ('Report', 'Share'):  (0.7, 1.0),
    ('Report', 'Ignore'): (0.7, 0.1),
    ('Report', 'Report'): (0.7, 0.7),
}

ACTIONS = ['Share', 'Ignore', 'Report']  # за инициализация/визуализация

def get_payoff(a: str, b: str):
    """Печалба за двойката (a,b) -> (π_A, π_B)."""
    return PAYOFF_MATRIX.get((a, b), (0.0, 0.0))

def node_payoff(G, strategies, node: int) -> float:
    """Сумарна печалба на възел node спрямо всички съседи: f_i = Σ_j π1(s_i, s_j)."""
    s_i = strategies[node]
    total = 0.0
    for j in G.neighbors(node):
        pi_i, _ = get_payoff(s_i, strategies[j])
        total += pi_i
    return total

if __name__ == "__main__":
    for a in ACTIONS:
        for b in ACTIONS:
            print(f"{a} vs {b}: {get_payoff(a,b)}")