# exposure.py
# Определя кои възли ще видят тренда на t+1 (експозиция).
# ВАЖНО: 'alpha' (+3.0) е бонус към ПОЛЕЗНОСТТА и се прилага в payoff.py,
# тук ползваме отделен параметър 'exp_boost_mult' за експозицията.

from __future__ import annotations
from typing import Mapping, MutableMapping, Any
import random

Action = str  # "Share" / "Comment" / "Ignore"

def update_exposure(
    G,
    exposure_t: Mapping[int, bool],
    actions_t: Mapping[int, Action],
    params: Mapping[str, Any],
) -> dict[int, bool]:
    """
    Обновява експозицията: кой ще види тренда на t+1.
    Вероятността да види зависи от броя реагирали съседи и boost при локален пик.

    Параметри (params):
      - rho0 (float)                : базова видимост, по подразбиране 0.15
      - algo_local_threshold / q    : праг за локален дял реагирали съседи, по подразбиране 0.40
      - exp_boost_mult (float)      : множител върху rho0 при локален пик, по подразбиране 1.50
      - rng (random.Random | None)  : опционален RNG за възпроизводимост

    Бележка:
      'utility_boost_alpha' (+3.0) се използва в payoff.py за бонус към полезността,
      НЕ се използва тук.
    """
    rho0 = float(params.get("rho0", 0.15))
    q = float(params.get("algo_local_threshold", params.get("q", 0.40)))
    exp_boost_mult = float(params.get("exp_boost_mult", 1.50))

    rng = params.get("rng")
    if not isinstance(rng, random.Random):
        rng = random  # пада обратно към глобалния ГПСЧ

    exposure_next: dict[int, bool] = dict(exposure_t)  # персистентна експозиция

    for i in G.nodes():
        # Веднъж експониран -> остава експониран
        if exposure_t.get(i, False):
            exposure_next[i] = True
            continue

        neigh = list(G.neighbors(i))
        deg = len(neigh)
        if deg == 0:
            continue

        reacted = sum(1 for j in neigh if actions_t.get(j) in ("Share", "Comment"))
        if reacted == 0:
            continue

        frac = reacted / deg
        rho = rho0 * (exp_boost_mult if frac >= q else 1.0)
        rho = max(0.0, min(1.0, rho))  # безопасен интервал [0,1]

        # Шанс да види поне веднъж, ако има 'reacted' независими „контакти“
        p = 1.0 - (1.0 - rho) ** reacted

        if rng.random() < p:
            exposure_next[i] = True

    return exposure_next
