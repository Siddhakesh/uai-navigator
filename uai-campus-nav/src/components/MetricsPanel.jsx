import React from 'react';
import { Satellite, Signal, Shield, Clock, Compass } from 'lucide-react';

export function MetricsPanel({ position, isLocating, permissionState, isSimulatorActive }) {
  const { latitude, longitude, accuracy, timestamp, heading, speed } = position;

  const formattedTime = timestamp ? new Date(timestamp).toLocaleTimeString() : 'N/A';

  return (
    <div className="bg-slate-900/70 border border-slate-800 rounded-2xl p-5 shadow-lg">
      <div className="flex items-center justify-between mb-4 border-b border-slate-800 pb-3">
        <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
          <Satellite className="w-4 h-4 text-cyan-400" />
          Live GPS Telemetry
        </h3>
        <span className="text-xs text-slate-400 font-mono flex items-center gap-1">
          <Clock className="w-3.5 h-3.5 text-slate-500" />
          Updated: {formattedTime}
        </span>
      </div>

      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 font-mono text-xs">
        {/* Latitude */}
        <div className="bg-slate-950/80 p-3 rounded-xl border border-slate-800">
          <span className="text-slate-500 block text-[10px] uppercase font-sans font-semibold mb-1">Latitude</span>
          <span className="text-slate-200 font-bold text-sm">
            {latitude !== null ? latitude.toFixed(6) : '—'}
          </span>
        </div>

        {/* Longitude */}
        <div className="bg-slate-950/80 p-3 rounded-xl border border-slate-800">
          <span className="text-slate-500 block text-[10px] uppercase font-sans font-semibold mb-1">Longitude</span>
          <span className="text-slate-200 font-bold text-sm">
            {longitude !== null ? longitude.toFixed(6) : '—'}
          </span>
        </div>

        {/* Accuracy */}
        <div className="bg-slate-950/80 p-3 rounded-xl border border-slate-800">
          <span className="text-slate-500 block text-[10px] uppercase font-sans font-semibold mb-1">Accuracy</span>
          <span className={`font-bold text-sm ${accuracy <= 15 ? 'text-emerald-400' : accuracy <= 50 ? 'text-amber-400' : 'text-rose-400'}`}>
            {accuracy !== null ? `±${accuracy} meters` : 'Acquiring...'}
          </span>
        </div>

        {/* Provider / Mode */}
        <div className="bg-slate-950/80 p-3 rounded-xl border border-slate-800">
          <span className="text-slate-500 block text-[10px] uppercase font-sans font-semibold mb-1">Signal Source</span>
          <span className="text-cyan-400 font-semibold text-xs flex items-center gap-1.5 mt-0.5">
            <Signal className="w-3.5 h-3.5 text-cyan-400" />
            {isSimulatorActive ? 'Simulator' : 'watchPosition'}
          </span>
        </div>
      </div>
    </div>
  );
}
