import { useState, useEffect, useRef, useCallback } from 'react';

/**
 * Custom Hook for real-time continuous GPS tracking using watchPosition()
 * Supports live GPS watch & simulated test coordinates.
 */
export function useGeolocation(options = {}) {
  const {
    enableHighAccuracy = true,
    timeout = 15000,
    maximumAge = 0,
  } = options;

  const [position, setPosition] = useState({
    latitude: null,
    longitude: null,
    accuracy: null,
    heading: null,
    speed: null,
    altitude: null,
    timestamp: null,
  });

  const [error, setError] = useState(null);
  const [isLocating, setIsLocating] = useState(true);
  const [permissionState, setPermissionState] = useState('prompt'); // 'prompt', 'granted', 'denied'
  const [isSimulatorActive, setIsSimulatorActive] = useState(false);
  const watchIdRef = useRef(null);

  // Check initial permission status if Permission API available
  useEffect(() => {
    if (navigator.permissions && navigator.permissions.query) {
      navigator.permissions
        .query({ name: 'geolocation' })
        .then((result) => {
          setPermissionState(result.state);
          result.onchange = () => {
            setPermissionState(result.state);
          };
        })
        .catch(() => {
          // Permissions API query not supported for geolocation in some browsers
        });
    }
  }, []);

  // Success handler for watchPosition
  const handleSuccess = useCallback((pos) => {
    // If simulator is active, ignore real GPS updates
    setIsSimulatorActive((simActive) => {
      if (!simActive) {
        setPosition({
          latitude: pos.coords.latitude,
          longitude: pos.coords.longitude,
          accuracy: Math.round(pos.coords.accuracy),
          heading: pos.coords.heading,
          speed: pos.coords.speed,
          altitude: pos.coords.altitude,
          timestamp: pos.timestamp || Date.now(),
        });
        setError(null);
        setIsLocating(false);
        setPermissionState('granted');
      }
      return simActive;
    });
  }, []);

  // Error handler for watchPosition
  const handleError = useCallback((err) => {
    let errorMessage = 'An unknown geolocation error occurred.';
    switch (err.code) {
      case err.PERMISSION_DENIED:
        errorMessage = 'Location access denied by user or browser.';
        setPermissionState('denied');
        break;
      case err.POSITION_UNAVAILABLE:
        errorMessage = 'Location information is unavailable.';
        break;
      case err.TIMEOUT:
        errorMessage = 'Location request timed out. Retrying...';
        break;
      default:
        break;
    }
    setError({ code: err.code, message: errorMessage });
    setIsLocating(false);
  }, []);

  // Start watchPosition
  const startWatching = useCallback(() => {
    if (!navigator.geolocation) {
      setError({ code: 0, message: 'Geolocation is not supported by your browser.' });
      setIsLocating(false);
      return;
    }

    setIsLocating(true);
    setError(null);

    // Clear existing watch if any
    if (watchIdRef.current !== null) {
      navigator.geolocation.clearWatch(watchIdRef.current);
    }

    watchIdRef.current = navigator.geolocation.watchPosition(
      handleSuccess,
      handleError,
      {
        enableHighAccuracy,
        timeout,
        maximumAge,
      }
    );
  }, [enableHighAccuracy, timeout, maximumAge, handleSuccess, handleError]);

  // Initialize GPS listener on mount
  useEffect(() => {
    startWatching();

    return () => {
      if (watchIdRef.current !== null) {
        navigator.geolocation.clearWatch(watchIdRef.current);
      }
    };
  }, [startWatching]);

  // Function to simulate a specific position (for testing geofences inside UI)
  const setSimulatedPosition = useCallback((lat, lng, accuracy = 8) => {
    setIsSimulatorActive(true);
    setIsLocating(false);
    setError(null);
    setPosition({
      latitude: lat,
      longitude: lng,
      accuracy: accuracy,
      heading: 0,
      speed: 0,
      altitude: 10,
      timestamp: Date.now(),
    });
  }, []);

  // Function to reset simulator back to live GPS
  const resetToRealGPS = useCallback(() => {
    setIsSimulatorActive(false);
    startWatching();
  }, [startWatching]);

  return {
    position,
    error,
    isLocating,
    permissionState,
    isSimulatorActive,
    startWatching,
    setSimulatedPosition,
    resetToRealGPS,
  };
}
