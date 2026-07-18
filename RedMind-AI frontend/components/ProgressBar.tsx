'use client';

import { useScanStore } from '@/store/scanStore';

const SEGMENTS = 40;

export default function ProgressBar() {
  const current = useScanStore((s) => s.current);

  if (!current) return null;

  const pct = current.total ? Math.round((current.completed / current.total) * 100) : 0;
  const filledSegments = Math.round((pct / 100) * SEGMENTS);

  return (
    <div className="w-full">
      <div className="flex justify-between font-mono text-xs text-text-muted mb-1.5">
        <span>
          {current.completed}/{current.total} MODULES
          {current.status === 'running' && <span className="terminal-cursor" />}
        </span>
        <span className="text-red-glow font-semibold">{pct}%</span>
      </div>
      <div className="h-3.5 bg-panel-raised rounded-sm overflow-hidden flex gap-[2px] p-[2px] relative">
        {Array.from({ length: SEGMENTS }).map((_, i) => {
          const filled = i < filledSegments;
          return (
            <div
              key={i}
              className={`flex-1 rounded-[1px] transition-all duration-150 ${
                filled ? 'bg-red-primary shadow-[0_0_6px_#ff3333]' : 'bg-panel-hover'
              }`}
            />
          );
        })}
        {current.status === 'running' && (
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/10 to-transparent w-1/4 animate-scanline pointer-events-none" />
        )}
      </div>
      <div className="flex gap-4 mt-2 font-mono text-[11px] text-text-muted">
        <span className="text-critical">CRIT {current.sevCounts.CRITICAL}</span>
        <span className="text-high">HIGH {current.sevCounts.HIGH}</span>
        <span className="text-medium">MED {current.sevCounts.MEDIUM}</span>
        <span className="text-low">LOW {current.sevCounts.LOW}</span>
      </div>
    </div>
  );
}
