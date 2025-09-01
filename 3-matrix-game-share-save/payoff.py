# payoff.py
# Единствен източник на истината за платежната матрица + помощни функции.

from typing import Dict, Tuple

# Базова платежна матрица (Таблица 1)
PAYOFF_MATRIX: Dict[Tuple[str, str], Tuple[int, int]] = {
    ("Share",   "Share"):   (3, 3),
    ("Share",   "Save"):    (2, 4),
    ("Share",   "Comment"): (4, 2),

    ("Save",    "Share"):   (4, 2),
    ("Save",    "Save"):    (2, 2),
    ("Save",    "Comment"): (3, 3),

    ("Comment", "Share"):   (2, 4),
    ("Comment", "Save"):    (3, 3),
    ("Comment", "Comment"): (5, 5),
}

def get_payoff(action_a: str, action_b: str) -> Tuple[int, int]:
    """Връща полезностите (u1, u2) за двойка действия (ред=Играч1, колона=Играч2)."""
    return PAYOFF_MATRIX.get((action_a, action_b), (0, 0))

def set_payoff_matrix(new_matrix: Dict[Tuple[str, str], Tuple[int, int]]) -> None:
    """Подмяна на матрицата (за параметрични сценарии)."""
    global PAYOFF_MATRIX
    PAYOFF_MATRIX = new_matrix

def get_current_payoff_matrix() -> Dict[Tuple[str, str], Tuple[int, int]]:
    """Връща текущата матрица (удобно за deepcopy в анализи)."""
    return PAYOFF_MATRIX
