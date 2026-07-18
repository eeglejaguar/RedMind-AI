'use client';

import { useState } from 'react';
import { ScanRecord } from '@/lib/types';
import { getVulnName } from '@/lib/catalog';
import SeverityBadge from './SeverityBadge';

export default function ResultsTable({ scan }: { scan: ScanRecord }) {
  const [expanded, setExpanded] = useState<string | null>(null);

  if (scan.results.length === 0) {
    return (
      <div className="text-text-muted font-mono text-sm p-6 text-center border border-hairline rounded-md">
        No findings recorded for this scan.
      </div>
    );
  }

  return (
    <div className="border border-hairline rounded-md overflow-hidden">
      {scan.results.map(({ moduleId, result }) => {
        const isOpen = expanded === moduleId;
        return (
          <div key={moduleId} className="border-b border-hairline last:border-b-0">
            <button
              onClick={() => setExpanded(isOpen ? null : moduleId)}
              className={`w-full flex items-center justify-between px-4 py-3 text-left hover:bg-panel-raised transition-colors ${
                result.severity === 'CRITICAL' ? 'animate-flashborder border-l-2' : ''
              }`}
            >
              <div className="flex items-center gap-3 min-w-0">
                <span className="font-mono text-xs text-text-muted shrink-0">{moduleId}</span>
                <span className="truncate text-sm">{getVulnName(moduleId)}</span>
              </div>
              <div className="flex items-center gap-3 shrink-0">
                <span className="text-xs text-text-muted font-mono">
                  {result.findings.length} finding(s)
                </span>
                <SeverityBadge severity={result.severity} />
              </div>
            </button>
            {isOpen && (
              <pre className="bg-void px-4 py-3 text-xs font-mono text-text-muted overflow-x-auto">
                {JSON.stringify(result.findings, null, 2)}
              </pre>
            )}
          </div>
        );
      })}
    </div>
  );
}
