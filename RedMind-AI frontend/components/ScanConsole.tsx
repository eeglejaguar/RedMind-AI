'use client';

import { useEffect, useRef } from 'react';
import { useScanStore } from '@/store/scanStore';

export default function ScanConsole() {
  const logs = useScanStore((s) => s.logs);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [logs]);

  function colorFor(line: string) {
    if (line.startsWith('✔') && line.includes('CRITICAL')) return 'text-critical';
    if (line.startsWith('✔') && line.includes('HIGH')) return 'text-high';
    if (line.startsWith('✔') && line.includes('MEDIUM')) return 'text-medium';
    if (line.startsWith('✔')) return 'text-low';
    if (line.startsWith('✗')) return 'text-critical';
    if (line.startsWith('⏹')) return 'text-medium';
    if (line.startsWith('✅')) return 'text-red-glow font-semibold';
    if (line.startsWith('▶')) return 'text-text-primary';
    return 'text-text-muted';
  }

  return (
    <div
      ref={scrollRef}
      className="bg-void border border-hairline rounded-md p-4 h-72 overflow-y-auto font-mono text-[13px] leading-6 grid-bg"
    >
      {logs.length === 0 && (
        <div className="text-text-muted italic">Awaiting scan initiation…</div>
      )}
      {logs.map((line, i) => (
        <div key={i} className={`fade-in-line whitespace-pre-wrap ${colorFor(line)}`}>
          {line}
        </div>
      ))}
    </div>
  );
}
