import React, { useState } from 'react';
import { X, Save, RotateCcw, Crosshair, Check, FileCode, Info } from 'lucide-react';

export function GeofenceConfigModal({
  isOpen,
  onClose,
  geofences,
  onSaveGeofences,
  userLat,
  userLng,
  onResetToDefaults
}) {
  const [formData, setFormData] = useState(geofences);
  const [savedSuccess, setSavedSuccess] = useState(false);

  if (!isOpen) return null;

  const handleInputChange = (id, field, value) => {
    setFormData((prev) =>
      prev.map((g) => {
        if (g.id === id) {
          const val = value === '' ? null : value;
          return { ...g, [field]: val };
        }
        return g;
      })
    );
  };

  const handleSetUserLocation = (id) => {
    if (userLat && userLng) {
      handleInputChange(id, 'lat', userLat.toFixed(6));
      handleInputChange(id, 'lng', userLng.toFixed(6));
    }
  };

  const handleSave = () => {
    const updated = formData.map((g) => ({
      ...g,
      lat: g.lat !== null && g.lat !== '' ? parseFloat(g.lat) : null,
      lng: g.lng !== null && g.lng !== '' ? parseFloat(g.lng) : null,
      radius: g.radius !== null && g.radius !== '' ? parseInt(g.radius, 10) : 30,
    }));
    onSaveGeofences(updated);
    setSavedSuccess(true);
    setTimeout(() => {
      setSavedSuccess(false);
      onClose();
    }, 800);
  };

  const handleReset = () => {
    onResetToDefaults();
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-md animate-fade-in">
      <div className="bg-slate-900 border border-slate-700 w-full max-w-2xl rounded-2xl shadow-2xl overflow-hidden flex flex-col max-h-[90vh]">
        {/* Modal Header */}
        <div className="px-6 py-4 border-b border-slate-800 flex items-center justify-between bg-slate-950/60">
          <div>
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              ⚙️ Geofence Coordinates Setup
            </h2>
            <p className="text-xs text-slate-400">
              Configure latitude, longitude & radius for the 4 UAI campus zones
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto space-y-6 flex-1">
          <div className="bg-cyan-950/40 border border-cyan-500/30 rounded-xl p-3.5 text-xs text-cyan-200 flex items-start gap-2.5">
            <Info className="w-4 h-4 text-cyan-400 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold mb-0.5">Configuration Options:</p>
              <p className="text-slate-300">
                You can edit coordinates directly in <code className="bg-slate-900 px-1.5 py-0.5 rounded text-cyan-300 font-mono">src/config/geofences.js</code> or use this form. Changes saved here persist instantly in your session.
              </p>
            </div>
          </div>

          <div className="space-y-4">
            {formData.map((zone) => (
              <div
                key={zone.id}
                className="bg-slate-950/80 border border-slate-800 rounded-xl p-4 space-y-3"
              >
                <div className="flex items-center justify-between">
                  <span className="font-bold text-slate-200 text-sm flex items-center gap-2">
                    <span className="w-2.5 h-2.5 rounded-full bg-cyan-400"></span>
                    {zone.name}
                  </span>
                  <button
                    onClick={() => handleSetUserLocation(zone.id)}
                    disabled={!userLat || !userLng}
                    className="text-[11px] px-2.5 py-1 bg-slate-800 hover:bg-slate-700 disabled:opacity-40 text-cyan-300 rounded-md border border-slate-700 flex items-center gap-1 transition"
                  >
                    <Crosshair className="w-3 h-3" />
                    Use Live GPS Coords
                  </button>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <div>
                    <label className="block text-[10px] font-semibold uppercase text-slate-400 mb-1">
                      Latitude
                    </label>
                    <input
                      type="number"
                      step="any"
                      placeholder="e.g. 19.076000"
                      value={zone.lat ?? ''}
                      onChange={(e) => handleInputChange(zone.id, 'lat', e.target.value)}
                      className="w-full bg-slate-900 border border-slate-700 focus:border-cyan-500 rounded-lg px-3 py-1.5 text-xs text-white font-mono outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-[10px] font-semibold uppercase text-slate-400 mb-1">
                      Longitude
                    </label>
                    <input
                      type="number"
                      step="any"
                      placeholder="e.g. 72.877700"
                      value={zone.lng ?? ''}
                      onChange={(e) => handleInputChange(zone.id, 'lng', e.target.value)}
                      className="w-full bg-slate-900 border border-slate-700 focus:border-cyan-500 rounded-lg px-3 py-1.5 text-xs text-white font-mono outline-none"
                    />
                  </div>

                  <div>
                    <label className="block text-[10px] font-semibold uppercase text-slate-400 mb-1">
                      Radius (Meters)
                    </label>
                    <input
                      type="number"
                      placeholder="30"
                      value={zone.radius ?? ''}
                      onChange={(e) => handleInputChange(zone.id, 'radius', e.target.value)}
                      className="w-full bg-slate-900 border border-slate-700 focus:border-cyan-500 rounded-lg px-3 py-1.5 text-xs text-white font-mono outline-none"
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Modal Footer */}
        <div className="px-6 py-3.5 border-t border-slate-800 bg-slate-950/80 flex items-center justify-between gap-3">
          <button
            onClick={handleReset}
            className="px-3.5 py-2 text-xs font-semibold text-slate-400 hover:text-rose-400 flex items-center gap-1.5 transition"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            Reset to Config File Defaults
          </button>

          <div className="flex items-center gap-2">
            <button
              onClick={onClose}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-semibold transition"
            >
              Cancel
            </button>
            <button
              onClick={handleSave}
              className="px-5 py-2 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white rounded-xl text-xs font-bold shadow-lg shadow-cyan-600/20 flex items-center gap-1.5 transition"
            >
              {savedSuccess ? (
                <>
                  <Check className="w-4 h-4 text-emerald-300" /> Saved!
                </>
              ) : (
                <>
                  <Save className="w-4 h-4" /> Save Geofences
                </>
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
