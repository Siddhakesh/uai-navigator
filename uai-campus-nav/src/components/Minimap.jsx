import React, { useState, useEffect } from 'react';

// Rough coordinates (in percentages) based on the NEW annotated campus map image
const MAP_COORDS = {
  uai_gate: { x: 25, y: 10 },     // Main Gate (Top Left)
  north: { x: 53, y: 42 },        // Academic Area / Universal AI University (Center)
  east: { x: 72, y: 60 },         // Shades of Saffron / Boys Hostel (Right)
  south: { x: 70, y: 25 },        // Sports Area / Academic Ground (Top Right)
  west: { x: 12, y: 15 },         // Main Facilities / Cafe Orange (Top Left)
};

// Map Calibration: You MUST replace these placeholders with the actual 
// Latitude and Longitude of the Top-Left and Bottom-Right corners of your image.
// You can get these from Google Maps by right-clicking on those corners.
const MAP_BOUNDS = {
  topLeft: { lat: 18.9328, lng: 73.3168 },     // PLACEHOLDER: Top Left corner of the image
  bottomRight: { lat: 18.9300, lng: 73.3200 }  // PLACEHOLDER: Bottom Right corner of the image
};

export default function Minimap({ currentLocation, destination }) {
  const currCoords = currentLocation ? MAP_COORDS[currentLocation.id] || { x: 50, y: 50 } : { x: 50, y: 50 };
  const destCoords = destination ? MAP_COORDS[destination.id] || null : null;

  const [gpsPos, setGpsPos] = useState(null);

  // 1. Real GPS Tracking
  useEffect(() => {
    if (!navigator.geolocation) return;

    const watchId = navigator.geolocation.watchPosition(
      (position) => {
        const { latitude, longitude } = position.coords;
        
        // Convert Lat/Lng to X/Y Percentages on our static image
        const latRange = MAP_BOUNDS.topLeft.lat - MAP_BOUNDS.bottomRight.lat;
        const lngRange = MAP_BOUNDS.bottomRight.lng - MAP_BOUNDS.topLeft.lng;

        // Map projection math
        const yPercent = ((MAP_BOUNDS.topLeft.lat - latitude) / latRange) * 100;
        const xPercent = ((longitude - MAP_BOUNDS.topLeft.lng) / lngRange) * 100;

        // Clamp values to keep the marker inside the map borders
        const x = Math.max(0, Math.min(100, xPercent));
        const y = Math.max(0, Math.min(100, yPercent));

        setGpsPos({ x, y });
      },
      (err) => console.warn("GPS tracking error:", err.message),
      { enableHighAccuracy: true, maximumAge: 0, timeout: 5000 }
    );

    return () => navigator.geolocation.clearWatch(watchId);
  }, []);

  // Use real GPS if available, otherwise stay still at the start location
  const pos = gpsPos || currCoords;

  const [isExpanded, setIsExpanded] = useState(false);

  // Calculate rotation angle so the arrow points towards the destination
  let rotation = 0;
  if (destCoords) {
    const dx = destCoords.x - pos.x;
    const dy = destCoords.y - pos.y;
    rotation = Math.atan2(dy, dx) * (180 / Math.PI) + 90;
  }

  return (
    <div 
      className={`minimap-container ${isExpanded ? 'expanded' : ''}`}
      onClick={() => { if (!isExpanded) setIsExpanded(true); }}
    >
      <div className="minimap-border">
        {/* N indicator on top (hide when expanded) */}
        {!isExpanded && <div className="minimap-north">N</div>}
        
        <div className="minimap-inner">
          {/* Real map background */}
          <div className="minimap-map-bg"></div>
          
          {/* Player marker (arrow) */}
          <div 
            className={`minimap-player-marker ${gpsPos ? 'real-gps' : ''}`}
            style={{ 
              left: `${pos.x}%`, 
              top: `${pos.y}%`,
              transform: `translate(-50%, -50%) rotate(${rotation}deg)` 
            }}
          ></div>
          
          {/* Destination blip */}
          {destCoords && (
            <div 
              className="minimap-dest-marker"
              style={{ left: `${destCoords.x}%`, top: `${destCoords.y}%` }}
            ></div>
          )}
        </div>
      </div>
      
      {/* Close button for full screen map */}
      {isExpanded && (
        <button 
          className="minimap-close-btn"
          onClick={(e) => {
            e.stopPropagation();
            setIsExpanded(false);
          }}
        >
          Close Map
        </button>
      )}
    </div>
  );
}
