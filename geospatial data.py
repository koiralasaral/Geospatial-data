import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Generate a mock elevation dataset
grid_size = 20
elevation = np.random.rand(grid_size, grid_size) * 1000  # Simulating altitude in meters

# Define permutations for transformation (simulating symmetries in elevation)
permutations = [
    lambda x: x,               # Identity transformation
    lambda x: np.flip(x, axis=0),  # Vertical reflection
    lambda x: np.flip(x, axis=1),  # Horizontal reflection
    lambda x: np.rot90(x),     # 90-degree rotation
    lambda x: np.rot90(x, 2),  # 180-degree rotation
]

fig, ax = plt.subplots(figsize=(6, 6))

# Animation function to visualize transformations dynamically
def update(frame):
    transformed_data = permutations[frame](elevation)
    ax.clear()
    ax.imshow(transformed_data, cmap='terrain')
    ax.set_title(f"Galois Group Transformation {frame + 1}")

ani = animation.FuncAnimation(fig, update, frames=len(permutations), interval=1000, repeat=True)
plt.show()