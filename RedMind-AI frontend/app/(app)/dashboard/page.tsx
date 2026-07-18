'use client';

import { useEffect } from 'react';
import Link from 'next/link';
import { useScanStore } from '@/store/scanStore';
import SeverityBadge from '@/components/SeverityBadge';
import { Crosshair, ArrowRight } from 'lucide-react';

export default function DashboardPage() {
  const { current, history, hydrate } = useScanStore();

  useEffect(() => {
    hydrate();
  }, [hydrate]);

  return (
    <div className="space-y-8">
      <header>
        <h1 className="font-display text-3xl font-bold tracking-wide text-glow text-red-glow">
          THREAT OVERVIEW
        </h1>
        <p className="text-text-muted text-sm mt-1">
          RedMind-AI automated vulnerability assessment console.
        </p>
      </header>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'CRITICAL', value: current?.sevCounts.CRITICAL ?? 0, color: 'text-critical' },
          { label: 'HIGH', value: current?.sevCounts.HIGH ?? 0, color: 'text-high' },
          { label: 'MEDIUM', value: current?.sevCounts.MEDIUM ?? 0, color: 'text-medium' },
          { label: 'LOW', value: current?.sevCounts.LOW ?? 0, color: 'text-low' },
        ].map((s) => (
          <div
            key={s.label}
            className="bg-panel border border-hairline rounded-md p-5 flex flex-col gap-1"
          >
            <span className="text-xs font-mono text-text-muted">{s.label}</span>
            <span className={`text-3xl font-display font-bold ${s.color}`}>{s.value}</span>
          </div>
        ))}
      </div>

      <div className="bg-panel border border-hairline rounded-md p-6 flex items-center justify-between">
        <div>
          <h2 className="font-display text-lg font-semibold">Launch a new assessment</h2>
          <p className="text-text-muted text-sm mt-1">
            Run automated checks against a live target.
          </p>
        </div>
        <Link
          href="/scan"
          className="flex items-center gap-2 bg-red-primary hover:bg-red-glow transition-colors text-void font-mono font-semibold px-5 py-2.5 rounded-md"
        >
          <Crosshair size={18} /> NEW SCAN
        </Link>
      </div>

      <div>
        <div className="flex items-center justify-between mb-3">
          <h2 className="font-display text-lg font-semibold">Recent Scans</h2>
          <Link href="/history" className="text-sm text-red-glow flex items-center gap-1 hover:underline">
            View all <ArrowRight size={14} />
          </Link>
        </div>
        <div className="border border-hairline rounded-md overflow-hidden">
          {history.length === 0 && (
            <div className="p-6 text-center text-text-muted font-mono text-sm">
              No scans recorded yet.
            </div>
          )}
          {history.slice(0, 5).map((h) => (
            <Link
              key={h.id}
              href={`/results/${h.id}`}
              className="flex items-center justify-between px-4 py-3 border-b border-hairline last:border-b-0 hover:bg-panel-raised transition-colors"
            >
              <div className="min-w-0">
                <div className="text-sm truncate">{h.target}</div>
                <div className="text-xs text-text-muted font-mono">
                  {new Date(h.date).toLocaleString()} · {h.scanType}
                </div>
              </div>
              <div className="flex items-center gap-3 shrink-0">
                <span className="text-xs font-mono text-text-muted">{h.duration}</span>
                <span className="text-sm font-mono text-red-glow">Risk {h.riskScore}</span>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </div>
  );
}
