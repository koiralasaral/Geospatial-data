import planetary_computer
import pystac_client
import rioxarray
import folium
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

# Define bounding box (Example: Nepal region)
bbox = [85.3, 27.5, 85.7, 28.0]

# Query Planetary Computer for Sentinel-2 water data
catalog = pystac_client.Client.open("https://planetarycomputer.microsoft.com/api/stac/v1")
search = catalog.search(collections=["sentinel-2-l2a"], bbox=bbox)
search = catalog.search(collections=["sentinel-2-l2a"], bbox=[85.3, 27.5, 85.7, 28.0])
items = list(search.items())  # Use items() instead of get_items()
item = items[0]  # Get the first item safely
asset = planetary_computer.sign(item.assets["B03"])  # Blue band (water reflectance)

# Load raster data
water_data = rioxarray.open_rasterio(asset.href)

# Convert to a mask where water is detected
threshold = 0.15  # Adjust for water detection sensitivity
water_mask = water_data.squeeze() < threshold

# Convert mask to GeoDataFrame for Folium overlay
gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(*np.where(water_mask)))
# Create Folium map centered at Nepal region
m = folium.Map(location=[27.7, 85.5], zoom_start=8)

# Add detected water points
for point in gdf.geometry:
    folium.CircleMarker(
        location=[point.y, point.x],
        radius=2,
        color="blue",
        fill=True,
        fill_color="blue",
    ).add_to(m)

# Display map
m.save("water_detection_map.html")
print("Water detection map saved as water_detection_map.html")
