import networkx as nx
import matplotlib.pyplot as plt
import random

# 1. Създаваме празен неориентиран граф
G = nx.Graph()

# 2. Добавяме 50 възела (потребители)
G.add_nodes_from(range(50))

# 3. Свързваме всеки възел с 3 до 6 други случайни възела
for node in G.nodes:
    num_edges = random.randint(3, 6)  # Случаен брой връзки
    possible_neighbors = list(set(G.nodes) - {node} - set(G.neighbors(node)))
    new_neighbors = random.sample(possible_neighbors, min(num_edges, len(possible_neighbors)))
    
    for neighbor in new_neighbors:
        G.add_edge(node, neighbor)

# 4. Визуализираме графа
plt.figure(figsize=(10, 10))
nx.draw(G, with_labels=True, node_color="skyblue", node_size=500, font_size=8)
plt.title("Симулация на социална мрежа с 50 потребителя")
plt.show()
