# payoff.py
# Полезност = база(действие) + локален бонус + (евентуален) boost при локален пик.

from __future__ import annotations
from typing import Mapping, Any

Action = str  # "Share" / "Comment" / "Ignore"

def compute_fitness(
    G,
    actions_t: Mapping[int, Action],
    params: Mapping[str, Any],
) -> dict[int, float]:
    # Бази по действие (baseline)
    base_comment = float(params.get("base_comment", 3.0))
    base_share   = float(params.get("base_share",   2.0))
    base_ignore  = float(params.get("base_ignore",  0.0))

    # Локален бонус и лимит (baseline cap = +3.0)
    local_bonus_per = float(params.get("local_bonus_per_reacted", 0.5))
    bonus_cap       = float(params.get("local_bonus_cap", 3.0))

    # Условие за локален пик и бонус точки α (към полезността)
    q      = float(params.get("algo_local_threshold", params.get("q", 0.40)))
    alpha  = float(params.get("utility_boost_alpha", 3.0))

    base_map = {
        "Comment": base_comment,
        "Share":   base_share,
        "Ignore":  base_ignore,
        None:      0.0,
    }

    fitness: dict[int, float] = {}
    for i in G.nodes():
        act = actions_t.get(i)
        score = base_map.get(act, base_ignore)

        # Начисляваме локален бонус и boost САМО ако възелът е действал
        if act in ("Share", "Comment"):
            neigh = list(G.neighbors(i))
            deg = len(neigh)
            reacted = sum(1 for j in neigh if actions_t.get(j) in ("Share", "Comment"))

            # локален бонус с горна граница
            score += min(bonus_cap, local_bonus_per * reacted)

            # алгоритмичен boost при локален пик
            if deg > 0 and (reacted / deg) >= q:
                score += alpha

        fitness[i] = float(score)

    return fitness
