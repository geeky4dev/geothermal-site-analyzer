import React, { useState } from 'react'
import { MapContainer, TileLayer, Marker, useMapEvents } from 'react-leaflet'
import axios from 'axios'

function LocationMarker({ onSelect }) {
  const [position, setPosition] = useState(null)

  useMapEvents({
    click(e) {
      setPosition(e.latlng)
      onSelect(e.latlng)
    },
  })

  return position === null ? null : (
    <Marker position={position}></Marker>
  )
}

export default function MapInput() {
  const [score, setScore] = useState(null)
  const [feasibility, setFeasibility] = useState(null)
  const [error, setError] = useState(null)

  const handleSelect = async (latlng) => {
    setError(null)
    try {
      const res = await axios.post('http://localhost:5001/api/score', {
        lat: latlng.lat,
        lon: latlng.lng,
      })
      setScore(res.data.score)
      setFeasibility(res.data.feasible)  // "Low", "Medium", or "High"
    } catch (e) {
      setError('Error fetching data')
    }
  }

  const renderScoreLabel = (score) => {
    if (score < 40) return 'Low geothermal potential (0–39)'
    if (score < 70) return 'Moderate geothermal potential (40–69)'
    return 'High geothermal potential (70–100)'
  }

  const renderFeasibilityLabel = (feasibility) => {
    if (feasibility === 'Low') return 'Low feasibility: not favorable conditions'
    if (feasibility === 'Medium') return 'Medium feasibility: partially favorable conditions'
    if (feasibility === 'High') return 'High feasibility: favorable conditions'
    return ''
  }

  return (
    <>
      <MapContainer center={[0, 0]} zoom={2} style={{ height: '400px', width: '100%' }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />
        <LocationMarker onSelect={handleSelect} />
      </MapContainer>
      <div style={{ marginTop: '1em' }}>
        {score !== null && (
          <p>
            <strong>Score:</strong> {score} <br />
            <small>{renderScoreLabel(score)}</small>
          </p>
        )}
        {feasibility !== null && (
          <p>
            <strong>Feasibility:</strong> {feasibility} <br />
            <small>{renderFeasibilityLabel(feasibility)}</small>
          </p>
        )}
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </div>
    </>
  )
}





