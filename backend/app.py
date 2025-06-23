from flask import Flask, request, jsonify
from flask_cors import CORS
import rasterio
import geopandas as gpd
from shapely.geometry import Point
import numpy as np
import traceback
from pyproj import Transformer

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes (allow frontend access)

# Load raster and vector data on startup
try:
    heatflow_raster = rasterio.open('data/heatflow.tif')
    temperature_raster = rasterio.open('data/temperature.tif')
    tectonics_gdf = gpd.read_file('data/tectonics.geojson')

    # Ensure tectonic data uses WGS84 (lat/lon)
    if tectonics_gdf.crs != "EPSG:4326":
        tectonics_gdf = tectonics_gdf.to_crs("EPSG:4326")

    # Define coordinate transformers
    transformer_heatflow = Transformer.from_crs("EPSG:4326", heatflow_raster.crs, always_xy=True)
    transformer_temperature = Transformer.from_crs("EPSG:4326", temperature_raster.crs, always_xy=True)

    print("✅ Geospatial data loaded successfully.")
except Exception:
    print("❌ Failed to load geospatial data:")
    traceback.print_exc()

# Function to sample value from raster
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

# Function to check if point intersects tectonic zone
def point_in_tectonics(lon, lat):
    pt = Point(lon, lat)
    return tectonics_gdf.intersects(pt).any()

# Main scoring endpoint
@app.route('/api/score', methods=['POST'])
def calculate_score():
    data = request.json
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

        # Normalized scores (0 to 1 range)
        heatflow_score = max(0, min(1, (heatflow - 40) / 80))   # Assuming useful range: 40–120 mW/m²
        temp_score = max(0, min(1, (temperature - 5) / 25))     # Assuming useful range: 5–30 °C
        fault_score = 1 if in_fault_zone else 0

        # Weighted total score
        score = heatflow_score * 50 + temp_score * 40 + fault_score * 10

        print(f"Sampling at lon={lon}, lat={lat}:")
        print(f"  🔥 Heatflow = {heatflow}")
        print(f"  🌡️  Temperature = {temperature}")
        print(f"  ⚠️  In tectonic fault zone = {in_fault_zone}")
        print(f"  Final Score = {score}")

        # Determine feasibility level
        if score < 40:
            feasibility = "Low"
        elif score < 70:
            feasibility = "Medium"
        else:
            feasibility = "High"

        return jsonify({
            "score": round(score, 2),
            "feasible": feasibility
        })

    except Exception:
        traceback.print_exc()
        return jsonify({"error": "Internal server error."}), 500

        

# Run the app
if __name__ == '__main__':
    app.run(port=5001, debug=True)



