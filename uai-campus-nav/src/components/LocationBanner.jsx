import React from 'react';
import { MapPin, Navigation, AlertTriangle, Loader2, Sparkles, SlidersHorizontal, Info } from 'lucide-react';
import { formatDistance } from '../utils/geo';

export function LocationBanner({
  evaluationResult,
  isLocating,
  error,
  accuracy,
  onOpenConfig,
  isSimulatorActive
}) {
  const { status, activeZone, nearestZone, isAccurate, configuredCount } = evaluationResult;

  // Case 1: Permission error or browser error
  if (error && !isSimulatorActive) {
    return (
      <div className="bg-rose-950/50 border border-rose-800/80 rounded-2xl p-6 text-center shadow-xl backdrop-blur-sm relative overflow-hidden">
        <div className="absolute -top-12 -right-12 w-36 h-36 bg-rose-500/10 rounded-full blur-2xl"></div>
        <div className="w-12 h-12 rounded-2xl bg-rose-900/60 border border-rose-700/50 flex items-center justify-center mx-auto mb-3 text-rose-400">
          <AlertTriangle className="w-6 h-6" />
        </div>
        <h3 className="text-lg font-bold text-rose-200 mb-1">GPS Access Required</h3>
        <p className="text-sm text-rose-300/80 max-w-md mx-auto mb-4">{error.message}</p>
        <p className="text-xs text-slate-400">
          Please enable device location permissions in your browser or switch on the <strong className="text-purple-300">Testing Sandbox</strong> to simulate campus locations.
        </p>
      </div>
    );
  }

  // Case 2: Inaccurate position or initial GPS acquisition (Requirement: "If the location is inaccurate, show: Getting your precise location...")
  if (isLocating || !isAccurate || accuracy === null || accuracy > 50) {
    return (
      <div className="relative overflow-hidden bg-gradient-to-r from-amber-950/60 via-slate-900 to-slate-950 border border-amber-500/30 rounded-2xl p-6 sm:p-8 text-center shadow-2xl backdrop-blur-md">
        {/* Animated Radar Pulse Background */}
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-20">
          <div className="w-64 h-64 rounded-full border border-amber-400 animate-pulse-ring"></div>
          <div className="w-40 h-40 rounded-full border border-amber-400 animate-pulse-ring" style={{ animationDelay: '0.6s' }}></div>
        </div>

        <div className="relative z-10 flex flex-col items-center">
          <div className="relative mb-4">
            <div className="w-16 h-16 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 shadow-lg shadow-amber-500/10">
              <Loader2 className="w-8 h-8 animate-spin text-amber-400" />
            </div>
            <span className="absolute -bottom-1 -right-1 flex h-4 w-4">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-amber-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-4 w-4 bg-amber-500"></span>
            </span>
          </div>

          <h2 className="text-xl sm:text-2xl font-extrabold text-amber-200 tracking-tight mb-2">
            Getting your precise location...
          </h2>
          <p className="text-sm text-slate-300 max-w-md mx-auto leading-relaxed">
            {accuracy !== null
              ? `Current GPS accuracy is ±${accuracy}m. Waiting for high-precision satellite lock (< 50m).`
              : 'Acquiring satellite position locks...'}
          </p>

          <div className="mt-4 inline-flex items-center gap-2 bg-slate-900/80 px-3.5 py-1.5 rounded-full border border-slate-700/60 text-xs text-slate-400">
            <Info className="w-3.5 h-3.5 text-amber-400" />
            <span>Ensure location high accuracy is enabled on your device</span>
          </div>
        </div>
      </div>
    );
  }

  // Case 3: No coordinates set in geofences yet
  if (configuredCount === 0) {
    return (
      <div className="bg-gradient-to-r from-slate-900 via-indigo-950/40 to-slate-900 border border-cyan-500/30 rounded-2xl p-6 sm:p-8 text-center shadow-2xl relative overflow-hidden">
        <div className="w-14 h-14 rounded-2xl bg-cyan-950 border border-cyan-500/40 flex items-center justify-center mx-auto mb-4 text-cyan-400 shadow-lg shadow-cyan-500/10">
          <SlidersHorizontal className="w-7 h-7" />
        </div>
        <h2 className="text-xl sm:text-2xl font-bold text-white mb-2">
          Geofence Coordinates Pending
        </h2>
        <p className="text-sm text-slate-300 max-w-lg mx-auto mb-6 leading-relaxed">
          The 4 campus zones (<span className="text-cyan-300 font-medium">UAI Main Gate, UAI Fountain, Hostel, Parking</span>) are ready, but their real latitude/longitude coordinates have not been entered yet.
        </p>
        <div className="flex flex-wrap items-center justify-center gap-3">
          <button
            onClick={onOpenConfig}
            className="px-5 py-2.5 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-semibold rounded-xl text-sm shadow-lg shadow-cyan-600/30 transition flex items-center gap-2"
          >
            <SlidersHorizontal className="w-4 h-4" />
            Configure Real Coordinates Now
          </button>
        </div>
      </div>
    );
  }

  // Case 4: Valid GPS & active/nearest zone found! (Requirement: "📍 You are currently near UAI Main Gate")
  const targetZone = activeZone || nearestZone;
  const isInside = targetZone && targetZone.isInside;

  return (
    <div className="relative overflow-hidden bg-gradient-to-br from-slate-900 via-slate-900/90 to-cyan-950/40 border border-cyan-500/40 rounded-2xl p-6 sm:p-8 shadow-2xl backdrop-blur-md">
      {/* Decorative Glow */}
      <div className="absolute top-0 right-0 w-80 h-80 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none"></div>
      <div className="absolute bottom-0 left-0 w-64 h-64 bg-indigo-500/10 rounded-full blur-3xl pointer-events-none"></div>

      <div className="relative z-10 flex flex-col items-center text-center">
        {/* Status Badge */}
        <div className="mb-3">
          {isInside ? (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-emerald-950/90 border border-emerald-500/50 text-emerald-300 text-xs font-semibold tracking-wide uppercase shadow-sm">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
              Inside Campus Zone
            </span>
          ) : (
            <span className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-cyan-950/90 border border-cyan-500/50 text-cyan-300 text-xs font-semibold tracking-wide uppercase shadow-sm">
              <Navigation className="w-3 h-3 text-cyan-400" />
              Nearest Campus Zone
            </span>
          )}
        </div>

        {/* PRIMARY DISPLAY MANDATED BY USER PROMPT */}
        <div className="my-2">
          <h2 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight flex flex-wrap items-center justify-center gap-2">
            <span className="text-3xl sm:text-4xl">📍</span>
            <span>You are currently near</span>
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 via-teal-300 to-indigo-300 underline decoration-cyan-500/50 decoration-wavy decoration-2">
              {targetZone ? targetZone.name : 'Campus'}
            </span>
          </h2>
        </div>

        {/* Zone Distance Subtitle */}
        {targetZone && (
          <p className="mt-2 text-sm sm:text-base text-slate-300 max-w-md">
            {isInside ? (
              <span className="text-emerald-400 font-medium flex items-center justify-center gap-1">
                <Sparkles className="w-4 h-4" /> You are within the {targetZone.radius}m geofence radius of {targetZone.name}.
              </span>
            ) : (
              <span>
                Approximately <strong className="text-cyan-300 font-semibold">{formatDistance(targetZone.distance)}</strong> away from {targetZone.name} (Geofence radius: {targetZone.radius}m).
              </span>
            )}
          </p>
        )}
      </div>
    </div>
  );
}
