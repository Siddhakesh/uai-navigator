import React from 'react';
import { Play, RotateCcw, Radio, Sparkles, Navigation, AlertCircle } from 'lucide-react';

export function SimulatorControl({
  geofences,
  isSimulatorActive,
  onSimulate,
  onResetToRealGPS
}) {
  // Preset demo coordinates for testing
  const DEMO_COORDS = {
    'main-gate': { lat: 19.076000, lng: 72.877700 },
    'fountain': { lat: 19.076800, lng: 72.878500 },
    'hostel': { lat: 19.077500, lng: 72.879200 },
    'parking': { lat: 19.075200, lng: 72.876500 },
  };

  const handleTeleportToZone = (zone) => {
    // If zone has real coordinates, use those, else use demo reference
    const lat = zone.lat !== null ? zone.lat : DEMO_COORDS[zone.id]?.lat || 19.076000;
    const lng = zone.lng !== null ? zone.lng : DEMO_COORDS[zone.id]?.lng || 72.877700;
    
    // Pass high precision (8 meters accuracy)
    onSimulate(lat, lng, 8);
  };

  const handleSimulateInaccurateSignal = () => {
    // Pass low precision accuracy (> 65 meters) to trigger "Getting your precise location..."
    const lat = 19.076000;
    const lng = 72.877700;
    onSimulate(lat, lng, 75);
  };

  return (
    <div className="bg-gradient-to-r from-purple-950/60 via-slate-900 to-slate-950 border border-purple-500/40 rounded-2xl p-5 shadow-xl">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 mb-4 pb-3 border-b border-purple-500/20">
        <div>
          <h3 className="text-sm font-bold text-purple-200 flex items-center gap-2">
            <Radio className="w-4 h-4 text-purple-400 animate-pulse" />
            Testing Sandbox & Teleport Simulator
          </h3>
          <p className="text-xs text-slate-400">
            Test geofence zone detection without walking around campus!
          </p>
        </div>

        {isSimulatorActive ? (
          <button
            onClick={onResetToRealGPS}
            className="px-3 py-1.5 bg-purple-900/80 hover:bg-purple-800 text-purple-200 rounded-lg text-xs font-semibold flex items-center gap-1.5 border border-purple-500/50 transition"
          >
            <RotateCcw className="w-3.5 h-3.5 text-purple-300" />
            Switch Back to Live Satellite GPS
          </button>
        ) : (
          <span className="text-[11px] text-slate-400 italic">
            Currently using live device GPS
          </span>
        )}
      </div>

      {/* Quick Teleport Buttons */}
      <div className="space-y-3">
        <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
          1-Click Teleport to Zone:
        </span>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2">
          {geofences.map((zone) => (
            <button
              key={zone.id}
              onClick={() => handleTeleportToZone(zone)}
              className="px-3 py-2 bg-slate-900 hover:bg-purple-950/80 border border-slate-800 hover:border-purple-500/50 text-slate-200 rounded-xl text-xs font-medium text-left flex items-center justify-between transition group"
            >
              <span className="truncate">{zone.name}</span>
              <Play className="w-3 h-3 text-purple-400 group-hover:translate-x-0.5 transition-transform" />
            </button>
          ))}
        </div>

        {/* Test Inaccurate Signal */}
        <div className="pt-2 flex items-center gap-2">
          <button
            onClick={handleSimulateInaccurateSignal}
            className="px-3 py-1.5 bg-amber-950/60 hover:bg-amber-900/80 border border-amber-500/40 text-amber-300 rounded-lg text-xs font-medium flex items-center gap-1.5 transition"
          >
            <AlertCircle className="w-3.5 h-3.5 text-amber-400" />
            Test Inaccurate GPS Signal (&gt;50m Accuracy)
          </button>
        </div>
      </div>
    </div>
  );
}
