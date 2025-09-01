# network.py
import networkx as nx

def make_small_world(n=100, k=8, p=0.1, seed=42,
                     ensure_connected=True, max_tries=10, largest_cc_fallback=True):
    """
    Генерира Watts–Strogatz small-world граф.
    - Валидира k (четно, 0<k<n)
    - По желание гарантира свързаност:
        * пробва до max_tries пъти да генерира свързан граф
        * ако не успее и largest_cc_fallback=True → връща най-голямата компонента
    Връща граф с цели етикети 0..N-1 (стабилни за reproducibility).
    """
    if not (0 < k < n) or (k % 2 != 0):
        raise ValueError("Параметърът k трябва да е четен и да удовлетворява 0 < k < n.")

    # Опитваме до max_tries да получим свързан граф (WS не гарантира свързаност при всяко p)
    for _ in range(max_tries):
        G = nx.watts_strogatz_graph(n=n, k=k, p=p, seed=seed)
        if not ensure_connected or nx.is_connected(G):
            # нормализиране на етикетите за стабилност (и последователност с други модули)
            return nx.convert_node_labels_to_integers(G, first_label=0)

    # fallback: най-голямата свързана компонента (ако е позволено)
    if largest_cc_fallback:
        cc = max(nx.connected_components(G), key=len)
        G_cc = G.subgraph(cc).copy()
        return nx.convert_node_labels_to_integers(G_cc, first_label=0)

    # ако не настояваме за свързаност – връщаме последния G
    return nx.convert_node_labels_to_integers(G, first_label=0)
