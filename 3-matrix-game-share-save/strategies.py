# strategies.py
# Дефиниции на чисти стратегии и регистър по име.

from typing import List, Callable, Dict

Action = str
History = List[Action]
StrategyFn = Callable[[History, History], Action]

def share(_: History, __: History) -> Action:
    return "Share"

def save(_: History, __: History) -> Action:
    return "Save"

def comment(_: History, __: History) -> Action:
    return "Comment"

STRATEGIES: Dict[str, StrategyFn] = {
    "Share": share,
    "Save": save,
    "Comment": comment,
}
