import matplotlib.pyplot as plt
import networkx as nx
import time

# Define field extensions (ℚ → ℚ(√2) → ℚ(√2, i))
extensions = [
    ("ℚ", "ℚ(√2)"), 
    ("ℚ(√2)", "ℚ(√2, i)"),
    ("ℚ", "ℚ(i)"),
    ("ℚ(i)", "ℚ(√2, i)")
]

G = nx.DiGraph()
fig, ax = plt.subplots(figsize=(6, 6))

for idx, (a, b) in enumerate(extensions):
    G.add_edge(a, b)
    ax.clear()
    nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray', font_size=12, ax=ax)
    plt.pause(0.8)

plt.show()