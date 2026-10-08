/**
 * Calculate Haversine distance between two latitude/longitude points in meters.
 */
export function calculateHaversineDistance(lat1, lon1, lat2, lon2) {
  if (
    lat1 === null || lat1 === undefined ||
    lon1 === null || lon1 === undefined ||
    lat2 === null || lat2 === undefined ||
    lon2 === null || lon2 === undefined
  ) {
    return null;
  }

  const R = 6371000; // Earth's mean radius in meters
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const radLat1 = toRad(lat1);
  const radLat2 = toRad(lat2);

  const a =
    Math.sin(dLat / 2) * Math.sin(dLat / 2) +
    Math.sin(dLon / 2) * Math.sin(dLon / 2) * Math.cos(radLat1) * Math.cos(radLat2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

  return Math.round(R * c); // Distance rounded to nearest meter
}

function toRad(degrees) {
  return (degrees * Math.PI) / 180;
}

/**
 * Format meters for clean UI display (e.g., 12m or 1.4km)
 */
export function formatDistance(meters) {
  if (meters === null || meters === undefined || isNaN(meters)) return 'N/A';
  if (meters < 1000) return `${meters} m`;
  return `${(meters / 1000).toFixed(2)} km`;
}

/**
 * Evaluate user's GPS position against active campus geofences.
 */
export function evaluateCampusGeofences(userLat, userLng, accuracy, geofences, accuracyThreshold = 50) {
  if (!userLat || !userLng) {
    return {
      status: 'NO_GPS',
      isAccurate: false,
      activeZone: null,
      nearestZone: null,
      distanceToNearest: null,
      configuredCount: 0,
      zoneDistances: []
    };
  }

  // Check accuracy threshold
  const isAccurate = accuracy !== null && accuracy !== undefined && accuracy <= accuracyThreshold;

  // Filter geofences that have valid lat/lng set
  const validGeofences = geofences.filter(
    (z) => z.lat !== null && z.lat !== undefined && z.lng !== null && z.lng !== undefined && !isNaN(z.lat) && !isNaN(z.lng)
  );

  if (validGeofences.length === 0) {
    return {
      status: 'NO_COORDINATES_SET',
      isAccurate,
      activeZone: null,
      nearestZone: null,
      distanceToNearest: null,
      configuredCount: 0,
      zoneDistances: geofences.map(z => ({ ...z, distance: null, isInside: false }))
    };
  }

  // Calculate distance to all zones
  const zoneDistances = geofences.map((zone) => {
    if (zone.lat === null || zone.lng === null || isNaN(zone.lat) || isNaN(zone.lng)) {
      return { ...zone, distance: null, isInside: false };
    }
    const dist = calculateHaversineDistance(userLat, userLng, Number(zone.lat), Number(zone.lng));
    const isInside = dist <= (zone.radius || 30);
    return { ...zone, distance: dist, isInside };
  });

  // Find nearest zone among valid ones
  const validDistances = zoneDistances.filter((z) => z.distance !== null);
  validDistances.sort((a, b) => a.distance - b.distance);

  const nearestZone = validDistances[0] || null;
  
  // Active zone is inside radius if accurate, otherwise nearest zone
  const activeZone = validDistances.find((z) => z.isInside) || nearestZone;

  return {
    status: isAccurate ? 'OK' : 'INACCURATE',
    isAccurate,
    activeZone: activeZone ? activeZone : null,
    nearestZone: nearestZone ? nearestZone : null,
    distanceToNearest: nearestZone ? nearestZone.distance : null,
    configuredCount: validGeofences.length,
    zoneDistances
  };
}
