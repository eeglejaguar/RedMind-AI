import { Severity } from '@/lib/types';

const STYLES: Record<Severity, string> = {
  CRITICAL: 'bg-critical/15 text-critical border-critical/50',
  HIGH: 'bg-high/15 text-high border-high/50',
  MEDIUM: 'bg-medium/15 text-medium border-medium/50',
  LOW: 'bg-low/15 text-low border-low/50',
  INFO: 'bg-info/15 text-info border-info/50',
};

export default function SeverityBadge({ severity }: { severity: Severity }) {
  return (
    <span
      className={`inline-block px-2 py-0.5 rounded border text-[11px] font-mono font-semibold tracking-wider ${STYLES[severity]}`}
    >
      {severity}
    </span>
  );
}
