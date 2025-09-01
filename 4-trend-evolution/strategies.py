# strategies.py
import random
from collections import Counter

ACTIONS = ["Share", "Comment", "Ignore"]
TYPES = ["Commentator", "Conformist", "Skeptic", "FastSharer"]

def decide_action(user_type, i, G, actions_prev, exposed_now, params):
    """
    Връща действие на възел i за текущия рунд, на база:
    - тип (стратегия);
    - експозиция (exposed_now);
    - действия на съседите от предния рунд (actions_prev) – за Конформист/Скептик.
    """
    if not exposed_now:
        return None  # не е видял тренда

    if user_type == "Commentator":
        return "Comment"

    if user_type == "FastSharer":
        return "Share"

    neigh = list(G.neighbors(i))
    neigh_actions = [actions_prev.get(j) for j in neigh if actions_prev.get(j) in ACTIONS]
    reacted_neigh = [a for a in neigh_actions if a in ("Share", "Comment")]
    deg = max(1, len(neigh))

    if user_type == "Conformist":
        if not neigh_actions:
            return "Share"  # дефолт при липса на инфо
        counts = Counter(neigh_actions)
        # мнозинство, при равенство предпочита "Share"
        winner, _ = max(counts.items(), key=lambda kv: (kv[1], 1 if kv[0]=="Share" else 0))
        return winner

    if user_type == "Skeptic":
        tau = params.get("skeptic_tau", 0.3)
        frac = len(reacted_neigh) / deg
        return "Share" if frac >= tau else "Ignore"

    # fallback
    return "Ignore"
