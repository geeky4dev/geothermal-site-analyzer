import rasterio
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
from pyproj import Transformer

# Cargar tectonics solo una vez y reproyectar a EPSG:4326 si es necesario
tectonics = gpd.read_file("data/tectonics.geojson")
if tectonics.crs != "EPSG:4326":
    tectonics = tectonics.to_crs("EPSG:4326")

def read_raster_value(filepath, lat, lon):
    with rasterio.open(filepath) as src:
        # Transformar coordenadas de EPSG:4326 a la CRS del raster
        transformer = Transformer.from_crs("EPSG:4326", src.crs, always_xy=True)
        x, y = transformer.transform(lon, lat)
        coords = [(x, y)]
        for val in src.sample(coords):
            return float(val[0]) if val[0] is not None else np.nan

def evaluate_site(lat, lon):
    heatflow = read_raster_value("data/heatflow.tif", lat, lon)
    temp = read_raster_value("data/temperature.tif", lat, lon)

    if np.isnan(heatflow) or np.isnan(temp):
        print(f"⚠️ Datos inválidos para lat={lat}, lon={lon}")
        return 0.0, False

    # Normalización de valores
    heatflow_score = (heatflow - 50) / (150 - 50)
    temp_score = (temp - 10) / (40 - 10)

    heatflow_score = np.clip(heatflow_score, 0, 1)
    temp_score = np.clip(temp_score, 0, 1)

    # Verificar intersección con fallas tectónicas
    point = Point(lon, lat)
    point_gdf = gpd.GeoDataFrame(geometry=[point], crs="EPSG:4326")
    intersects_fault = tectonics.intersects(point_gdf.loc[0, 'geometry']).any()
    fault_score = 1.0 if intersects_fault else 0.0

    # Cálculo final con ponderaciones
    final_score = heatflow_score * 0.4 + temp_score * 0.3 + fault_score * 0.3
    final_score = round(final_score, 2)
    feasible = final_score > 0.6  # Umbral de factibilidad

    # Debugging
    print("────────────────────────────")
    print(f"Lat: {lat}, Lon: {lon}")
    print(f"Heatflow raw: {heatflow}, Temp raw: {temp}")
    print(f"Heatflow score: {heatflow_score}, Temp score: {temp_score}")
    print(f"Intersecta falla: {intersects_fault} → Fault score: {fault_score}")
    print(f"Final score: {final_score}, Feasible: {feasible}")
    print("────────────────────────────")

    return final_score, feasible
