import planetary_computer
import pystac_client
import rioxarray
import folium
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt
from folium.plugins import MarkerCluster

# 📍 Define bounding box (Example: Nepal region)
bbox = [85.3, 27.5, 85.7, 28.0]

# 🔍 Query Planetary Computer for Sentinel-2 water data
catalog = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
search = catalog.search(collections=["sentinel-2-l2a"], bbox=bbox)
items = list(search.items())  # ✅ Use `items()` instead of deprecated `get_items()`
item = items[0]  # Get the first item safely
asset = planetary_computer.sign(item.assets["B03"])  # ✅ Using Blue band (water reflectance)

# 📊 Load raster data
water_data = rioxarray.open_rasterio(asset.href)

# 🔹 Analyze water reflectance values dynamically
plt.hist(water_data.squeeze().values.flatten(), bins=50, color='blue')
plt.xlabel("Reflectance")
plt.ylabel("Frequency")
plt.title("Histogram of Water Reflectance Values")
plt.show()

# ✅ Convert pixel values into water mask based on best threshold
threshold = 0.15  # Adjust based on histogram
water_mask = water_data.squeeze() < threshold

# 🔹 Convert pixel indices to real-world coordinates
coords = np.column_stack(np.where(water_mask))
lon_lat = [water_data.rio.transform * (x, y) for y, x in coords]
gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy([p[0] for p in lon_lat], [p[1] for p in lon_lat]))

# 🌍 Create Folium map centered at Nepal region
m = folium.Map(location=[27.7, 85.5], zoom_start=8)

# ✅ Use MarkerCluster for better visualization
marker_cluster = MarkerCluster().add_to(m)

for point in gdf.geometry:
    folium.Marker(location=[point.y, point.x], icon=folium.Icon(color="blue")).add_to(marker_cluster)

# 🖥️ Save map OR display interactively
m.save("water_detection_map.html")
print("✅ Water detection map saved as `water_detection_map.html`")

# ✅ If using Jupyter, display map interactively
try:
    from IPython.display import display
    display(m)
except ImportError:
    pass  # Skip interactive display outside Jupyter