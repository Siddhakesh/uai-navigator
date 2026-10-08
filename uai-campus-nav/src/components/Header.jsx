import React from 'react';
import { Compass, Settings, ShieldAlert, Wifi, Radio, SlidersHorizontal } from 'lucide-react';

export default function Header({
  isLocating,
  permissionState,
  isSimulatorActive,
  accuracy,
  onOpenConfig,
  onToggleSimulator,
  showSimulator
}) {
  const getAccuracyBadge = () => {
    if (accuracy === null || accuracy === undefined) {
      return <span className="bg-slate-800 text-slate-400 px-2.5 py-1 rounded-full text-xs font-mono">GPS Pending</span>;
    }
    if (accuracy <= 15) {
      return (
        <span className="bg-emerald-950/80 border border-emerald-500/30 text-emerald-400 px-2.5 py-1 rounded-full text-xs font-mono flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          Accuracy ±{accuracy}m (High)
        </span>
      );
    }
    if (accuracy <= 50) {
      return (
        <span className="bg-amber-950/80 border border-amber-500/30 text-amber-400 px-2.5 py-1 rounded-full text-xs font-mono flex items-center gap-1.5">
          <span className="w-2 h-2 rounded-full bg-amber-400 animate-pulse"></span>
          Accuracy ±{accuracy}m (Moderate)
        </span>
      );
    }
    return (
      <span className="bg-rose-950/80 border border-rose-500/30 text-rose-400 px-2.5 py-1 rounded-full text-xs font-mono flex items-center gap-1.5">
        <span className="w-2 h-2 rounded-full bg-rose-400 animate-pulse"></span>
        Accuracy ±{accuracy}m (Low)
      </span>
    );
  };

  return (
    <header className="bg-slate-900/90 backdrop-blur-md border-b border-slate-800 sticky top-0 z-40 px-4 py-3.5 transition-all">
      <div className="max-w-5xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
        {/* Brand */}
        <div className="flex items-center gap-3 w-full sm:w-auto justify-between sm:justify-start">
          <div className="flex items-center gap-2.5">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-cyan-600 to-indigo-600 flex items-center justify-center shadow-lg shadow-cyan-500/20">
              <Compass className="w-5 h-5 text-white animate-radar" />
            </div>
            <div>
              <h1 className="text-lg font-bold text-white tracking-tight flex items-center gap-2">
                UAI Campus Navigator
                <span className="text-[10px] uppercase font-bold tracking-widest px-2 py-0.5 rounded bg-cyan-950 border border-cyan-500/40 text-cyan-400">
                  Phase 1 GPS
                </span>
              </h1>
              <p className="text-xs text-slate-400">Live Campus Geofence Location Engine</p>
            </div>
          </div>

          {/* Mobile Config buttons */}
          <div className="flex items-center gap-2 sm:hidden">
            <button
              onClick={onOpenConfig}
              className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-300 transition"
              title="Configure Geofences"
            >
              <Settings className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Right Status & Actions */}
        <div className="flex items-center gap-3 w-full sm:w-auto justify-between sm:justify-end">
          {/* Simulator indicator flag */}
          {isSimulatorActive && (
            <span className="bg-purple-950/80 border border-purple-500/40 text-purple-300 text-xs px-2.5 py-1 rounded-full font-medium flex items-center gap-1.5 shadow-sm">
              <Radio className="w-3.5 h-3.5 text-purple-400 animate-pulse" />
              GPS Simulator Active
            </span>
          )}

          {!isSimulatorActive && getAccuracyBadge()}

          {/* Action buttons */}
          <div className="hidden sm:flex items-center gap-2">
            <button
              onClick={onToggleSimulator}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 border transition ${
                showSimulator
                  ? 'bg-purple-600/30 border-purple-500/50 text-purple-200'
                  : 'bg-slate-800/80 hover:bg-slate-700 border-slate-700 text-slate-300'
              }`}
            >
              <SlidersHorizontal className="w-3.5 h-3.5" />
              {showSimulator ? 'Hide Test Panel' : 'Testing Sandbox'}
            </button>

            <button
              onClick={onOpenConfig}
              className="px-3.5 py-1.5 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white rounded-lg text-xs font-medium flex items-center gap-1.5 shadow-md shadow-cyan-600/20 transition"
            >
              <Settings className="w-3.5 h-3.5" />
              Configure Geofences
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
