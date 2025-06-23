# visualize_rasters.py
import rasterio
import matplotlib.pyplot as plt
import numpy as np

def plot_raster(filepath, title):
    with rasterio.open(filepath) as src:
        data = src.read(1)
        bounds = src.bounds
        extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]

        plt.figure(figsize=(10, 6))
        plt.imshow(data, extent=extent, cmap="inferno", origin="upper")
        plt.colorbar(label="Valor")
        plt.title(title)
        plt.xlabel("Longitud")
        plt.ylabel("Latitud")
        plt.grid(True)
        plt.show()

plot_raster("data/heatflow.tif", "Heat Flow (mW/m²)")
plot_raster("data/temperature.tif", "Temperatura (°C a profundidad)")
