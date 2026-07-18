/**
 * RedMind-AI — Mock API layer (demo mode)
 *
 * In production this will call the real FastAPI backend.
 * For the demo build, every runModule() call resolves from /public/data.json,
 * keyed on the active target. A realistic per-module delay is injected so
 * the scan console and progress bar behave exactly as they would against a
 * live backend.
 *
 * To switch to the real backend, replace this file with the original api.ts.
 */

import { CheckResult } from './types';

// ─── Data cache ────────────────────────────────────────────────────────────────

let _cache: Record<string, any> | null = null;

async function getData(): Promise<Record<string, any>> {
  if (_cache) return _cache;
  const res = await fetch('/data.json');
  _cache = await res.json();
  return _cache!;
}

// ─── Target resolution ────────────────────────────────────────────────────────

/**
 * Map any target URL the user types to one of the three demo datasets.
 * Priority: exact label match → keyword heuristic → random assignment.
 */
function resolveTarget(target: string, targets: Record<string, any>): string {
  const t = target.toLowerCase();

  // Exact label match
  for (const [key, val] of Object.entries(targets)) {
    if (t.includes(val.label)) return key;
  }

  // Keyword heuristics
  if (t.includes('bank') || t.includes('finance') || t.includes('pay')) return 'demo-banking';
  if (t.includes('blog') || t.includes('news') || t.includes('wp') || t.includes('wordpress')) return 'demo-blog';
  if (t.includes('shop') || t.includes('store') || t.includes('ecom') || t.includes('cart')) return 'demo-ecommerce';

  // Default: cycle through targets based on target string length
  const keys = Object.keys(targets);
  return keys[target.length % keys.length];
}

// ─── Module runner ────────────────────────────────────────────────────────────

export async function runModule(moduleId: string, target: string): Promise<CheckResult> {
  const data = await getData();
  const { targets, moduleDelays } = data;

  const targetKey = resolveTarget(target, targets);
  const dataset = targets[targetKey];

  // Find a finding for this moduleId, if any
  const match = dataset.findings.find((f: any) => f.moduleId === moduleId);

  // Simulate realistic per-module latency
  const sev = match?.severity ?? 'INFO';
  const delay = (moduleDelays[sev] ?? moduleDelays.default) + Math.random() * 300;
  await new Promise((r) => setTimeout(r, delay));

  if (!match) {
    return {
      check_id: moduleId,
      module_id: moduleId,
      severity: 'INFO',
      target,
      dangerous: false,
      findings: [],
      summary: {
        tested_requests: Math.floor(Math.random() * 20) + 2,
        positive_hits: 0,
      },
    };
  }

  return {
    check_id: moduleId,
    module_id: moduleId,
    severity: match.severity,
    target,
    dangerous: match.severity === 'CRITICAL' || match.severity === 'HIGH',
    findings: match.findings,
    summary: match.summary ?? { tested_requests: 10, positive_hits: match.findings.length },
  };
}

// Kept for any import that references API_URL
export const API_URL = '(mock)';
