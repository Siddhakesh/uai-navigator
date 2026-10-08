import React from 'react';
import { DoorOpen, Droplets, Building2, Car, MapPin, CheckCircle2, Crosshair, ArrowUpRight } from 'lucide-react';
import { formatDistance } from '../utils/geo';

const ICON_MAP = {
  DoorOpen: DoorOpen,
  Droplets: Droplets,
  Building2: Building2,
  Car: Car,
};

export function ZoneCard({
  zone,
  isActiveZone,
  isNearest,
  userLat,
  userLng,
  onSetCurrentLocation,
  onOpenConfig
}) {
  const IconComponent = ICON_MAP[zone.icon] || MapPin;

  const hasCoords = zone.lat !== null && zone.lng !== null && !isNaN(zone.lat) && !isNaN(zone.lng);

  return (
    <div
      className={`relative rounded-2xl p-5 border transition-all duration-300 ${
        isActiveZone
          ? 'bg-gradient-to-b from-cyan-950/80 to-slate-900 border-cyan-500 shadow-xl shadow-cyan-500/10 ring-1 ring-cyan-500/50'
          : isNearest
          ? 'bg-gradient-to-b from-indigo-950/40 to-slate-900 border-indigo-500/60 shadow-lg'
          : 'bg-slate-900/60 hover:bg-slate-900 border-slate-800 hover:border-slate-700'
      }`}
    >
      {/* Top Header */}
      <div className="flex items-start justify-between gap-3 mb-3">
        <div className="flex items-center gap-3">
          <div
            className={`w-11 h-11 rounded-xl flex items-center justify-center transition ${
              isActiveZone
                ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-400/40'
                : 'bg-slate-800 text-slate-400 border border-slate-700'
            }`}
          >
            <IconComponent className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-bold text-white text-base tracking-tight">{zone.name}</h3>
            <span className="text-xs text-slate-400 block">{zone.description}</span>
          </div>
        </div>

        {/* Status Badge */}
        <div>
          {isActiveZone ? (
            <span className="inline-flex items-center gap-1 bg-emerald-950 border border-emerald-500/50 text-emerald-400 text-[11px] font-bold px-2.5 py-1 rounded-full">
              <CheckCircle2 className="w-3 h-3" />
              Inside Zone
            </span>
          ) : isNearest && hasCoords ? (
            <span className="inline-flex items-center gap-1 bg-indigo-950 border border-indigo-500/50 text-indigo-300 text-[11px] font-semibold px-2 py-0.5 rounded-full">
              Nearest
            </span>
          ) : !hasCoords ? (
            <span className="inline-flex items-center gap-1 bg-slate-800 text-slate-400 text-[11px] px-2 py-0.5 rounded-full border border-slate-700">
              Coords Unset
            </span>
          ) : null}
        </div>
      </div>

      {/* Coordinates / Distance Info */}
      <div className="bg-slate-950/60 rounded-xl p-3 border border-slate-800/80 mb-4 font-mono text-xs space-y-1.5">
        <div className="flex justify-between items-center text-slate-400">
          <span>Latitude:</span>
          <span className={hasCoords ? 'text-slate-200 font-semibold' : 'text-slate-500 italic'}>
            {hasCoords ? Number(zone.lat).toFixed(6) : 'Not configured'}
          </span>
        </div>
        <div className="flex justify-between items-center text-slate-400">
          <span>Longitude:</span>
          <span className={hasCoords ? 'text-slate-200 font-semibold' : 'text-slate-500 italic'}>
            {hasCoords ? Number(zone.lng).toFixed(6) : 'Not configured'}
          </span>
        </div>
        <div className="flex justify-between items-center text-slate-400 pt-1 border-t border-slate-800/60">
          <span>Geofence Radius:</span>
          <span className="text-cyan-400 font-semibold">{zone.radius || 30} meters</span>
        </div>
        <div className="flex justify-between items-center text-slate-400">
          <span>Live Distance:</span>
          <span className={`font-bold ${isActiveZone ? 'text-emerald-400' : 'text-cyan-300'}`}>
            {hasCoords ? formatDistance(zone.distance) : '—'}
          </span>
        </div>
      </div>

      {/* Quick Actions */}
      <div className="flex items-center gap-2">
        <button
          onClick={() => onSetCurrentLocation(zone.id)}
          disabled={!userLat || !userLng}
          className="flex-1 py-2 px-3 bg-slate-800 hover:bg-slate-700 disabled:opacity-50 disabled:cursor-not-allowed text-slate-200 rounded-lg text-xs font-medium flex items-center justify-center gap-1.5 border border-slate-700 transition"
          title="Save current GPS lat/lng to this zone"
        >
          <Crosshair className="w-3.5 h-3.5 text-cyan-400" />
          Set Current GPS Here
        </button>

        <button
          onClick={onOpenConfig}
          className="p-2 bg-slate-800/60 hover:bg-slate-700 text-slate-400 hover:text-slate-200 rounded-lg border border-slate-700 transition"
          title="Edit coordinates manually"
        >
          <ArrowUpRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
