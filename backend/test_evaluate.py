from app import evaluate_site

# Lista de coordenadas (lat, lon) variadas: zonas montañosas, costeras, áridas, etc.
test_coords = [
    (38.5, -122.5),   # Napa Valley, CA (área geotérmica conocida)
    (64.8, -147.7),   # Fairbanks, Alaska
    (-22.9, -68.2),   # Atacama, Chile
    (10.5, -66.9),    # Caracas, Venezuela (fuera de zona de calor alto)
    (35.7, 139.7),    # Tokio, Japón (zona tectónica activa)
    (-1.3, 36.8),     # Nairobi, Kenia (área de Rift)
    (47.6, -122.3),   # Seattle, WA
    (0.0, 0.0),       # Océano Atlántico, punto fuera de cobertura (para probar errores)
]

print("=== Prueba de Evaluación de Sitios Geotérmicos ===\n")

for lat, lon in test_coords:
    print(f"📍 Lat: {lat}, Lon: {lon}")
    result = evaluate_site(lat, lon)

    if "error" in result:
        print(f"  ❌ Error: {result['error']}")
    else:
        print(f"  🔥 Heatflow: {result['heatflow']}")
        print(f"  🌡️  Temperature: {result['temperature']}")
        print(f"  ⚠️  En zona de falla tectónica: {'Sí' if result['in_fault_zone'] else 'No'}")
        print(f"  📊 Score: {result['score']} → Factibilidad: {result['feasible']}")
    print("-" * 50)
