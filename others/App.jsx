import React from 'react'
import MapInput from "./components/MapInput";
import 'leaflet/dist/leaflet.css'

function App() {
  return (
    <div>
      {/* CORRECCIÓN AQUÍ: style como un objeto JavaScript */}
      <h1 style={{ color: '#8CC43C' }}>🌋 Geothermal Site Feasibility Analyzer</h1>
      <h2>Evaluate the feasibility of a geothermal site based on location input.</h2>
      {/* CORRECCIÓN AQUÍ: style como un objeto JavaScript */}
      <h2 style={{ color: '#8CC43C' }}>Select the Location with click on the map to get a feasibility score using geological, terrain and climate data. </h2>
      
      <MapInput />
      <h2>How the Feasibility Score Works:</h2>
      <h4>1. Extracts Geospatial Data at That Point:<br/>
📊 Heat Flow (Higher heat flow = better geothermal potential). <br/>
🌡️ Surface Temperature (Moderate surface temperature is preferred). <br/>
🌍 Tectonic Activity: Checks if the point is near a tectonic plate boundary (Closer = higher geothermal likelihood).<br/><br/>

2. Calculate Score (Weighted) = Heat Flow (50%) + Surface Temperature (30%) + Tectonic Activity (20%).<br/><br/>


3. Normalizes Each Factor (Each value is converted to a 0–1 scale).<br/><br/>

3. Calculates Feasibility Level using adjustable weights.<br/>

feasibility = 0.5 * heat_flow_score + 0.3 * tectonic_score + 0.2 * temp_score<br/><br/>

4. Assigns Feasibility Level: The total score (between 0 and 1) is classified into:<br/>

🔴 Low Feasibility (0.0 – 0.4)<br/>
🟡 Medium Feasibility (0.4 – 0.7)<br/>
🟢 High Feasibility (0.7 – 1.0)<br/></h4>
<h4>
5. Example of locations showing their geothermal feasibility scores:<br/>
🟢 High Geothermal Potential (Score: 80–100)<br/>
📍 Location: Napa Valley, California, USA (38.5, -122.5)<br/>
🔥 High heat flow (near The Geysers geothermal field)<br/>
⚠️ Close to tectonic fault zones (San Andreas)<br/>
🌡️ Mild surface temperature<br/>
✅ → Score ≈ 85–95 → Feasibility: High<br/><br/>

🟡 Medium Geothermal Potential (Score: 40–79)<br/>
📍 Location: Nairobi, Kenya (-1.3, 36.8)<br/>
🔥 Moderate to high heat flow (Great Rift Valley)<br/>
⚠️ Some tectonic activity<br/>
🌡️ Warm temperatures<br/>
✅ → Score ≈ 65–75 → Feasibility: Medium<br/><br/>

🔴 Low Geothermal Potential (Score: 0–39)<br/>
📍 Location: Fairbanks, Alaska, USA (64.8, -147.7)
🔥 Low heat flow<br/>
⚠️ Far from tectonic faults<br/>
❄️ Cold surface temperature<br/>
✅ → Score ≈ 20–30 → Feasibility: Low<br/>
</h4>
    </div>
  )
}

export default App

