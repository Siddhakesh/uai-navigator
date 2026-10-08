import React, { useState, useEffect } from 'react';
import './App.css';
import { ArrowUp, ArrowRight, ArrowDown, ArrowLeft, MapPin, CheckCircle, QrCode, Camera } from 'lucide-react';
import { Scanner } from '@yudiel/react-qr-scanner';
import { QRCodeSVG } from 'qrcode.react';
import Minimap from './components/Minimap';

const DIRECTIONS = [
  { id: 'north', direction: 'north', label: 'Academic Area', icon: ArrowUp },
  { id: 'east', direction: 'east', label: 'Hostel', icon: ArrowRight },
  { id: 'south', direction: 'south', label: 'Sports Area', icon: ArrowDown },
  { id: 'west', direction: 'west', label: 'Main Facilities', icon: ArrowLeft },
];

const LOCATIONS = [
  { id: 'uai_gate', label: 'UAI Gate' },
  { id: 'north', label: 'Academic Area' },
  { id: 'east', label: 'Hostel' },
  { id: 'south', label: 'Sports Area' },
  { id: 'west', label: 'Main Facilities' },
];

export default function App() {
  const [view, setView] = useState('home'); // scanner, home, navigating, arrived, admin-qr
  const [currentLocation, setCurrentLocation] = useState(null);
  const [selectedDirection, setSelectedDirection] = useState(null);
  const [videoError, setVideoError] = useState(false);

  useEffect(() => {
    // Check if the URL has a location parameter (e.g. ?loc=uai_gate)
    const params = new URLSearchParams(window.location.search);
    const locId = params.get('loc');
    
    if (locId) {
      const loc = LOCATIONS.find((l) => l.id === locId);
      if (loc) {
        setCurrentLocation(loc);
        setView('home');
        return;
      }
    }
    // If no valid location in URL, default to scanner
    setView('scanner');
  }, []);

  const handleSelectDirection = (dir) => {
    setSelectedDirection(dir);
    setVideoError(false);
    setView('navigating');
  };

  const handleScan = (result) => {
    if (result && result.length > 0) {
      const rawUrl = result[0].rawValue;
      try {
        const url = new URL(rawUrl);
        const locId = url.searchParams.get('loc');
        if (locId) {
          const loc = LOCATIONS.find((l) => l.id === locId);
          if (loc) {
            setCurrentLocation(loc);
            setView('home');
            // Update URL without reloading
            window.history.pushState({}, '', `?loc=${locId}`);
          }
        }
      } catch (e) {
        console.warn('Invalid QR Code URL scanned');
      }
    }
  };

  const getBaseUrl = () => {
    return window.location.origin + window.location.pathname;
  };

  return (
    <div className="app-container">
      {/* Background elements to match the reference HTML */}
      <div className="shade"></div>
      <div className="cloud c1"></div>
      <div className="cloud c2"></div>

      <div className="content">
        {view === 'scanner' && (
          <div className="scanner-view animate-in">
            <h1 className="title">Scan Campus Code</h1>
            <p className="subtitle mb-6">Point your camera at any UAI QR code</p>
            
            <div className="scanner-container">
              <Scanner 
                onScan={handleScan}
                onError={(error) => console.log(error?.message)}
                components={{ audio: false, onOff: true, torch: true, zoom: true, finder: true }}
              />
            </div>
            
            <div className="mt-8">
              <button 
                className="skip-btn" 
                style={{ padding: '12px 24px', opacity: 0.8 }}
                onClick={() => {
                  setCurrentLocation(LOCATIONS[0]);
                  setView('home');
                }}
              >
                Skip & Simulate Gate
              </button>
            </div>
            <button 
              className="admin-link mt-4" 
              onClick={() => setView('admin-qr')}
            >
              <QrCode size={16} /> Print QR Codes
            </button>
          </div>
        )}

        {view === 'admin-qr' && (
          <div className="admin-qr-view animate-in">
            <h2 className="title mb-6">Generate QR Codes</h2>
            <div className="qr-grid">
              {LOCATIONS.map((loc) => {
                const url = `${getBaseUrl()}?loc=${loc.id}`;
                return (
                  <div key={loc.id} className="qr-card">
                    <h3 className="qr-title">{loc.label}</h3>
                    <div className="qr-code-wrapper">
                      <QRCodeSVG value={url} size={150} level="H" />
                    </div>
                    <p className="qr-url">{url}</p>
                  </div>
                );
              })}
            </div>
            <button className="action-button mt-8" onClick={() => setView('scanner')}>
              Back to App
            </button>
          </div>
        )}

        {view === 'home' && currentLocation && (
          <div className="home-view animate-in">
            <div className="location-indicator">
              <span className="subtitle">You are at</span>
              <h2 className="current-location">
                <MapPin className="icon-gold" /> {currentLocation.label}
              </h2>
            </div>

            <div className="question-section">
              <h1 className="title">Where do you want to go?</h1>
              <p className="subtitle mb-6">Choose a direction</p>

              <div className="directions-grid">
                {DIRECTIONS.map((dir) => {
                  const Icon = dir.icon;
                  // Don't show the current location as a destination
                  if (dir.id === currentLocation.id) return null;
                  
                  return (
                    <button
                      key={dir.id}
                      className="direction-card"
                      onClick={() => handleSelectDirection(dir)}
                    >
                      <Icon className="dir-icon" size={48} />
                      <span className="dir-label">{dir.label}</span>
                    </button>
                  );
                })}
              </div>
            </div>
            
            <button 
              className="scan-another-btn mt-8" 
              onClick={() => {
                setView('scanner');
                window.history.pushState({}, '', window.location.pathname);
              }}
            >
              <Camera size={20} /> Scan Another QR
            </button>
          </div>
        )}

        {view === 'navigating' && selectedDirection && (
          <div className="navigating-view animate-in">
            <h2 className="nav-title">Route to {selectedDirection.label}</h2>
            
            <Minimap currentLocation={currentLocation} destination={selectedDirection} />
            
            <div className="video-container">
              {videoError ? (
                /* Fallback when no video file exists for this route */
                <div className="no-video-fallback">
                  <p className="ar-instruction">🚧 No video available for this route yet.</p>
                  <button 
                    className="skip-btn" 
                    onClick={() => setView('arrived')}
                  >
                    Skip to Destination
                  </button>
                </div>
              ) : (
                <>
                  <video 
                    key={`${currentLocation.id}_to_${selectedDirection.direction}`}
                    className="route-video"
                    autoPlay 
                    playsInline 
                    controls
                    onEnded={() => setView('arrived')}
                    onError={() => setVideoError(true)}
                  >
                    <source src={`/videos/${currentLocation.id}_to_${selectedDirection.direction}.mp4`} type="video/mp4" />
                    Your browser does not support the video tag.
                  </video>
                  
                  <div className="ar-overlay">
                    <p className="ar-instruction">Follow the path shown in the video...</p>
                    <button 
                      className="skip-btn" 
                      onClick={() => setView('arrived')}
                    >
                      Skip to Destination
                    </button>
                  </div>
                </>
              )}
            </div>
          </div>
        )}

        {view === 'arrived' && selectedDirection && (
          <div className="arrived-view animate-in">
            <CheckCircle className="success-icon" size={80} />
            <h1 className="title text-gold mt-4">You have arrived!</h1>
            <p className="subtitle text-lg mt-2 mb-8">{selectedDirection.label}</p>
            
            <button 
              className="action-button"
              onClick={() => {
                setView('home');
                setSelectedDirection(null);
              }}
            >
              Navigate Again
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
