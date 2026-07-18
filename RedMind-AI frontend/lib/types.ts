export type Severity = 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'INFO';

export interface Finding {
  [key: string]: any;
}

export interface CheckResult {
  check_id?: string;
  module_id?: string;
  severity: Severity;
  target?: string;
  dangerous?: boolean;
  findings: Finding[];
  summary?: { tested_requests: number; positive_hits: number };
  error?: string;
}

export interface AttackDef {
  id: string;
  name: string;
  cat: string;
  sev: Severity;
}

export type ScanType = 'quick' | 'web' | 'network' | 'custom' | 'full';
export type ScanStatus = 'idle' | 'running' | 'complete' | 'aborted';

export interface SevCounts {
  CRITICAL: number;
  HIGH: number;
  MEDIUM: number;
  LOW: number;
  INFO: number;
}

export interface ScanRecord {
  id: string;
  target: string;
  scanType: ScanType;
  date: string;
  status: ScanStatus;
  results: { moduleId: string; result: CheckResult }[];
  completed: number;
  total: number;
  sevCounts: SevCounts;
  riskScore: number;
  secScore: number;
  duration: string;
  notes?: string;
}