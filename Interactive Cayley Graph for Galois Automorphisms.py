import networkx as nx
import matplotlib.pyplot as plt
from ipywidgets import interact, IntSlider

# Galois Group for x² - 2 (ℚ(√2))
G = nx.DiGraph()
G.add_edge("Identity", "Swap √2 ↔ -√2")

# Interactive function
def plot_graph(frame):
    plt.figure(figsize=(5, 5))
    nx.draw(G, with_labels=True, node_color=['lightblue', 'lightcoral'], font_size=12)
    plt.title(f"Galois Group Action {frame}")
    plt.show()

interact(plot_graph, frame=IntSlider(min=0, max=1, step=1, value=0))