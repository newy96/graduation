PAYOFF_MATRIX = {
    ('Like', 'Like'): (2, 2),
    ('Like', 'Ignore'): (0, 1),
    ('Like', 'Comment'): (1, 3),
    ('Ignore', 'Like'): (1, 0),
    ('Ignore', 'Ignore'): (0, 0),
    ('Ignore', 'Comment'): (-1, 2),
    ('Comment', 'Like'): (3, 1),
    ('Comment', 'Ignore'): (2, -1),
    ('Comment', 'Comment'): (3, 3),
}

def get_payoff(action_a: str, action_b: str):
    return PAYOFF_MATRIX.get((action_a, action_b), (0, 0))
