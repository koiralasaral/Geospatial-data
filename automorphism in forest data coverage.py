import planetary_computer
import pystac_client
import rioxarray
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define search parameters
catalog = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
search = catalog.search(collections=["sentinel-2-l2a"], bbox=[85.3, 27.5, 85.7, 28.0])  # Example Nepal region
item = next(search.items())
asset = planetary_computer.sign(item.assets["B08"])  # Near-Infrared Band

# Load raster data
ndvi = rioxarray.open_rasterio(asset.href)

# Define transformations (simulating Galois automorphisms)
transformations = [
    lambda x: x,               # Identity transformation
    lambda x: np.flip(x, axis=0),  # Vertical inversion
    lambda x: np.flip(x, axis=1),  # Horizontal inversion
    lambda x: np.rot90(x),     # 90-degree rotation
    lambda x: np.rot90(x, 2),  # 180-degree rotation
]

fig, ax = plt.subplots(figsize=(6, 6))

# Animation function to visualize transformations dynamically
def update(frame):
    transformed_ndvi = transformations[frame](ndvi.squeeze())
    ax.clear()
    ax.imshow(transformed_ndvi, cmap='Greens')
    ax.set_title(f"Automorphism {frame + 1}")

ani = animation.FuncAnimation(fig, update, frames=len(transformations), interval=1000, repeat=True)
plt.show()