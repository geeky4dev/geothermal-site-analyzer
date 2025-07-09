import React from 'react'
import MapInput from "./components/MapInput"
import 'leaflet/dist/leaflet.css'

function App() {
  return (
    <div style={{ padding: '1rem', fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ color: '#8CC43C', marginBottom: '0.2rem' }}>
        🌋 Geothermal Site Feasibility Analyzer
      </h1>
      <h2 style={{ marginTop: 0, fontWeight: 'normal' }}>
        Evaluate the feasibility of a geothermal site based on location input.
      </h2>
      <h2 style={{ color: '#8CC43C', marginTop: '0.5rem', fontWeight: 'bold' }}>
        Select the Location with a click on the map to get a feasibility score using geological, terrain and climate data.
      </h2>

      <MapInput />

      <h4>Example of locations showing their geothermal feasibility scores:</h4>

      <table
        border="1"
        style={{
          borderCollapse: 'collapse',
          width: '100%',
          textAlign: 'left',
          marginTop: '1rem',
          fontSize: '0.9rem',
        }}
      >
        <thead>
          <tr>
            <th>🔴 Low Potential</th>
            <th>🟡 Medium Potential</th>
            <th>🟢 High Potential</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>
              📍 <strong>Fairbanks, Alaska, USA</strong><br />
              (64.8, -147.7)<br />
              🔥 Low heat flow<br />
              ⚠️ Far from tectonic faults<br />
              ❄️ Cold surface temperature<br />
              ✅ Score ≈ 20–30 → <strong>Feasibility: Low</strong>
            </td>
            <td>
              📍 <strong>Nairobi, Kenya</strong><br />
              (-1.3, 36.8)<br />
              🔥 Moderate to high heat flow<br />
              ⚠️ Some tectonic activity<br />
              🌡️ Warm temperatures<br />
              ✅ Score ≈ 65–75 → <strong>Feasibility: Medium</strong>
            </td>
            <td>
              📍 <strong>Napa Valley, California, USA</strong><br />
              (38.5, -122.5)<br />
              🔥 High heat flow (near The Geysers)<br />
              ⚠️ Close to tectonic fault zones<br />
              🌡️ Mild surface temperature<br />
              ✅ Score ≈ 85–95 → <strong>Feasibility: High</strong>
            </td>
          </tr>
        </tbody>
      </table>

      <h2>How the Feasibility Score Works:</h2>
      <h4>
        1. Extracts Geospatial Data at That Point:
      </h4>
      <ul>
        <li>📊 Heat Flow (Higher heat flow = better geothermal potential).</li>
        <li>🌡️ Surface Temperature (Moderate surface temperature is preferred).</li>
        <li>🌍 Tectonic Activity: Checks if the point is near a tectonic plate boundary (Closer = higher geothermal likelihood).</li>
      </ul>

      <h4>2. Calculate Score (Weighted):</h4>
      <p>Score = Heat Flow (50%) + Surface Temperature (30%) + Tectonic Activity (20%)</p>

      <h4>3. Normalizes Each Factor:</h4>
      <p>Each value is converted to a 0–1 scale.</p>

      <h4>4. Calculates Feasibility Level using adjustable weights:</h4>
      <p>
        feasibility = 0.5 * heat_flow_score + 0.3 * tectonic_score + 0.2 * temp_score
      </p>

      <h4>5. Assigns Feasibility Level:</h4>
      <ul>
        <li>🔴 Low Feasibility (0.0 – 0.4)</li>
        <li>🟡 Medium Feasibility (0.4 – 0.7)</li>
        <li>🟢 High Feasibility (0.7 – 1.0)</li>
      </ul>

    </div>
  )
}

export default App



