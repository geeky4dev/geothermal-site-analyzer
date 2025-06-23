# backend/data/generate_mock_rasters.py
import numpy as np
import rasterio
from rasterio.transform import from_origin
import json

def create_mock_raster(filename, width, height, value_range):
    data = np.random.uniform(value_range[0], value_range[1], (height, width)).astype('float32')
    transform = from_origin(-180, 90, 0.5, 0.5)  # geo reference (lon/lat)
    new_dataset = rasterio.open(
        filename, 'w', driver='GTiff',
        height=height, width=width,
        count=1, dtype='float32',
        crs='EPSG:4326',
        transform=transform,
    )
    new_dataset.write(data, 1)
    new_dataset.close()

# Generar heatflow y temperature mocks
create_mock_raster('heatflow.tif', 720, 360, (50, 150))
create_mock_raster('temperature.tif', 720, 360, (10, 35))

# Crear geojson mock tectonics (polígonos simples)
tectonics = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {"fault_zone": True},
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [-10, 0], [-10, 10], [0, 10], [0, 0], [-10, 0]
                ]]
            }
        }
    ]
}

with open('tectonics.geojson', 'w') as f:
    json.dump(tectonics, f)   # Surface temperature