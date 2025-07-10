from flask import Flask, request, jsonify
from flask_cors import CORS
import rasterio
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import traceback
from pyproj import Transformer
import os

app = Flask(__name__)

CORS(app)

# 🔁 Cargar datos al iniciar
try:
    heatflow_raster = rasterio.open('data/heatflow.tif')
    temperature_raster = rasterio.open('data/temperature.tif')
    tectonics_gdf = gpd.read_file('data/tectonics.geojson')

    if tectonics_gdf.crs != "EPSG:4326":
        tectonics_gdf = tectonics_gdf.to_crs("EPSG:4326")

    transformer_heatflow = Transformer.from_crs("EPSG:4326", heatflow_raster.crs, always_xy=True)
    transformer_temperature = Transformer.from_crs("EPSG:4326", temperature_raster.crs, always_xy=True)

    print("✅ Geospatial data loaded successfully.")
except Exception:
    print("❌ Failed to load geospatial data:")
    traceback.print_exc()

# 🔎 Función auxiliar para muestreo de ráster
def sample_raster(raster, transformer, lon, lat):
    try:
        x, y = transformer.transform(lon, lat)
        row, col = raster.index(x, y)
        band1 = raster.read(1)
        value = band1[row, col]
        if value == raster.nodata:
            return np.nan
        return float(value)
    except Exception as e:
        print(f"❌ Raster sampling error: {e}")
        return np.nan

# ⚠️ Verificar si el punto está en una falla tectónica
def point_in_tectonics(lon, lat):
    pt = Point(lon, lat)
    return tectonics_gdf.intersects(pt).any()

# ✅ Endpoint para calcular el puntaje y factibilidad
@app.route('/api/score', methods=['POST', 'OPTIONS'])
def calculate_score():
    if request.method == 'OPTIONS':
        return '', 204  # ✅ Necesario para que CORS no falle

    data = request.json or {}
    lon = data.get('lon')
    lat = data.get('lat')

    if lon is None or lat is None:
        return jsonify({"error": "Missing latitude or longitude."}), 400

    try:
        heatflow = sample_raster(heatflow_raster, transformer_heatflow, lon, lat)
        temperature = sample_raster(temperature_raster, transformer_temperature, lon, lat)

        if np.isnan(heatflow) or np.isnan(temperature):
            return jsonify({"error": "No valid data at this location."}), 400

        in_fault_zone = point_in_tectonics(lon, lat)

        heatflow_score = max(0, min(1, (heatflow - 40) / 80))   # 40–120 mW/m²
        temp_score = max(0, min(1, (temperature - 5) / 25))     # 5–30 °C
        fault_score = 1 if in_fault_zone else 0

        score = heatflow_score * 50 + temp_score * 40 + fault_score * 10

        print(f"📍 Sampling at lon={lon}, lat={lat}")
        print(f"  🔥 Heatflow = {heatflow}")
        print(f"  🌡️  Temperature = {temperature}")
        print(f"  ⚠️  In fault zone = {in_fault_zone}")
        print(f"  📊 Final Score = {score}")

        if score < 40:
            feasibility = "🔴 Low"
        elif score < 70:
            feasibility = "🟡 Medium"
        else:
            feasibility = "🟢 High"

        return jsonify({
            "score": round(score, 2),
            "feasible": feasibility
        })

    except Exception:
        traceback.print_exc()
        return jsonify({"error": "Internal server error."}), 500

# 🔧 Ejecutar localmente
if __name__ == '__main__':
    debug_mode = os.environ.get('FLASK_ENV', '').lower() == 'development'
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=debug_mode)






