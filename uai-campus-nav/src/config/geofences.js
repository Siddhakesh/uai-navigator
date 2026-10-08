/**
 * UAI CAMPUS GEOFENCE CONFIGURATION
 * 
 * IMPORTANT: Real coordinates should be added here when available,
 * or configured directly via the UI Geofence Settings panel.
 * 
 * Set `lat` and `lng` to floating point numbers (e.g. 19.0760, 72.8777).
 * Set `radius` in meters (default fallback is 30m if unspecified).
 */

export const INITIAL_GEOFENCES = [
  {
    id: 'main-gate',
    name: 'UAI Main Gate',
    icon: 'DoorOpen',
    lat: null, // Replace with real latitude (e.g. 19.123456)
    lng: null, // Replace with real longitude (e.g. 72.987654)
    radius: 30, // Geofence radius in meters
    description: 'Main campus entry & security check point',
    tag: 'Gate 1',
    color: 'emerald'
  },
  {
    id: 'fountain',
    name: 'UAI Fountain',
    icon: 'Droplets',
    lat: null, // Replace with real latitude
    lng: null, // Replace with real longitude
    radius: 25, // Geofence radius in meters
    description: 'Central campus courtyard water fountain plaza',
    tag: 'Plaza',
    color: 'cyan'
  },
  {
    id: 'hostel',
    name: 'Hostel',
    icon: 'Building2',
    lat: null, // Replace with real latitude
    lng: null, // Replace with real longitude
    radius: 35, // Geofence radius in meters
    description: 'Student residential quarters & mess complex',
    tag: 'Block A-D',
    color: 'amber'
  },
  {
    id: 'parking',
    name: 'Parking',
    icon: 'Car',
    lat: null, // Replace with real latitude
    lng: null, // Replace with real longitude
    radius: 40, // Geofence radius in meters
    description: 'Visitor and student vehicle parking grounds',
    tag: 'Zone P1',
    color: 'indigo'
  }
];

// Threshold in meters beyond which location is considered inaccurate for precise zone locking
export const ACCURACY_THRESHOLD_METERS = 50;
