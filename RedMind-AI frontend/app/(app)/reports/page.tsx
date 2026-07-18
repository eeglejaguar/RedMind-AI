'use client';

import { useEffect } from 'react';
import { useScanStore } from '@/store/scanStore';
import { getVulnName } from '@/lib/catalog';
import SeverityBadge from '@/components/SeverityBadge';

export default function ReportsPage() {
  const { current, hydrate } = useScanStore();

  useEffect(() => {
    hydrate();
  }, [hydrate]);

  if (!current) {
    return (
      <div className="text-text-muted font-mono text-sm">
        No scan data available. Run a scan to generate a report.
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <header>
        <h1 className="font-display text-3xl font-bold tracking-wide text-red-glow text-glow">
          ASSESSMENT REPORT
        </h1>
        <p className="text-text-muted text-sm mt-1 font-mono">
          {current.target} · {new Date(current.date).toLocaleString()}
        </p>
      </header>

      <div className="bg-panel border border-hairline rounded-md p-6 space-y-2">
        <div className="flex justify-between text-sm">
          <span className="text-text-muted">Overall risk score</span>
          <span className="text-red-glow font-mono font-bold">{current.riskScore} / 100</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-text-muted">Security score</span>
          <span className="font-mono font-bold">{current.secScore} / 100</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-text-muted">Modules executed</span>
          <span className="font-mono">{current.completed} / {current.total}</span>
        </div>
        <div className="flex justify-between text-sm">
          <span className="text-text-muted">Duration</span>
          <span className="font-mono">{current.duration}</span>
        </div>
      </div>

      <div className="space-y-2">
        <h2 className="font-display font-semibold text-lg">Findings summary</h2>
        {current.results.map(({ moduleId, result }) => (
          <div
            key={moduleId}
            className="flex items-center justify-between bg-panel border border-hairline rounded px-4 py-3"
          >
            <div>
              <div className="text-xs font-mono text-text-muted">{moduleId}</div>
              <div className="text-sm">{getVulnName(moduleId)}</div>
            </div>
            <SeverityBadge severity={result.severity} />
          </div>
        ))}
        {current.results.length === 0 && (
          <div className="text-text-muted font-mono text-sm p-4">No findings recorded.</div>
        )}
      </div>
    </div>
  );
}
