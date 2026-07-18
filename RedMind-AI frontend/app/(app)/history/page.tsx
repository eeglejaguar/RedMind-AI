'use client';

import { useEffect } from 'react';
import Link from 'next/link';
import { useScanStore } from '@/store/scanStore';
import { Trash2 } from 'lucide-react';

export default function HistoryPage() {
  const { history, hydrate, clearHistory } = useScanStore();

  useEffect(() => {
    hydrate();
  }, [hydrate]);

  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <div>
          <h1 className="font-display text-3xl font-bold tracking-wide text-red-glow text-glow">
            SCAN HISTORY
          </h1>
          <p className="text-text-muted text-sm mt-1">Last {history.length} scans (max 50, stored locally).</p>
        </div>
        {history.length > 0 && (
          <button
            onClick={clearHistory}
            className="flex items-center gap-2 text-xs font-mono text-critical border border-critical/40 hover:bg-critical/10 px-3 py-2 rounded"
          >
            <Trash2 size={14} /> CLEAR HISTORY
          </button>
        )}
      </header>

      <div className="border border-hairline rounded-md overflow-hidden">
        {history.length === 0 && (
          <div className="p-8 text-center text-text-muted font-mono text-sm">No scans yet.</div>
        )}
        {history.map((h) => (
          <Link
            key={h.id}
            href={`/results/${h.id}`}
            className="flex items-center justify-between px-4 py-3 border-b border-hairline last:border-b-0 hover:bg-panel-raised transition-colors"
          >
            <div className="min-w-0">
              <div className="text-sm truncate">{h.target}</div>
              <div className="text-xs text-text-muted font-mono">
                {new Date(h.date).toLocaleString()} · {h.scanType} · {h.status}
              </div>
            </div>
            <div className="flex items-center gap-4 shrink-0 font-mono text-xs">
              <span className="text-critical">C{h.sevCounts.CRITICAL}</span>
              <span className="text-high">H{h.sevCounts.HIGH}</span>
              <span className="text-medium">M{h.sevCounts.MEDIUM}</span>
              <span className="text-red-glow">Risk {h.riskScore}</span>
              <span className="text-text-muted">{h.duration}</span>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
}
