import { AttackDef } from './types';

// Base named entries (mirrors the original dashboard's ATTACK_CATALOG for RM-CHK-001..056)
const NAMED: AttackDef[] = [
  { id: 'RM-CHK-001', name: 'Exposed Setup/Install Endpoint', cat: 'Injection', sev: 'CRITICAL' },
  { id: 'RM-CHK-002', name: 'SQL Injection', cat: 'Injection', sev: 'CRITICAL' },
  { id: 'RM-CHK-003', name: 'Cross-Site Scripting (XSS)', cat: 'Injection', sev: 'HIGH' },
  { id: 'RM-CHK-004', name: 'Open Redirect', cat: 'Injection', sev: 'MEDIUM' },
  { id: 'RM-CHK-005', name: 'Directory Listing Enabled', cat: 'Info Disclosure', sev: 'LOW' },
  { id: 'RM-CHK-006', name: 'Dangerous HTTP Methods', cat: 'Network', sev: 'MEDIUM' },
  { id: 'RM-CHK-007', name: 'Clickjacking (X-Frame-Options)', cat: 'Headers', sev: 'MEDIUM' },
  { id: 'RM-CHK-008', name: 'Insecure Cookie Configuration', cat: 'Authentication', sev: 'HIGH' },
  { id: 'RM-CHK-009', name: 'Server Banner Disclosure', cat: 'Network', sev: 'LOW' },
  { id: 'RM-CHK-010', name: 'Sensitive Path Exposure', cat: 'Info Disclosure', sev: 'HIGH' },
  { id: 'RM-CHK-012', name: 'Subdomain Takeover Risk', cat: 'Network', sev: 'HIGH' },
  { id: 'RM-CHK-013', name: 'Missing HSTS Header', cat: 'Network', sev: 'MEDIUM' },
  { id: 'RM-CHK-014', name: 'Weak TLS Configuration', cat: 'Network', sev: 'HIGH' },
  { id: 'RM-CHK-017', name: 'CORS Misconfiguration', cat: 'Headers', sev: 'MEDIUM' },
  { id: 'RM-CHK-018', name: 'Path Traversal', cat: 'Injection', sev: 'CRITICAL' },
  { id: 'RM-CHK-019', name: 'Command Injection', cat: 'Injection', sev: 'CRITICAL' },
  { id: 'RM-CHK-036', name: 'Open Ports Scan', cat: 'Network', sev: 'INFO' },
  { id: 'RM-CHK-037', name: 'SSL Certificate Expiry', cat: 'Network', sev: 'MEDIUM' },
  { id: 'RM-CHK-038', name: 'Mixed Content (HTTP in HTTPS)', cat: 'Network', sev: 'MEDIUM' },
  { id: 'RM-CHK-039', name: 'HTTP to HTTPS Redirect Missing', cat: 'Network', sev: 'MEDIUM' },
  { id: 'RM-CHK-040', name: 'Insecure DNS Configuration', cat: 'Network', sev: 'MEDIUM' },
  { id: 'RM-CHK-041', name: 'Unrestricted File Upload', cat: 'File Upload', sev: 'CRITICAL' },
  { id: 'RM-CHK-042', name: 'File Extension Bypass', cat: 'File Upload', sev: 'HIGH' },
  { id: 'RM-CHK-043', name: 'MIME Type Mismatch', cat: 'File Upload', sev: 'MEDIUM' },
  { id: 'RM-CHK-044', name: 'API Key Exposure', cat: 'API Security', sev: 'CRITICAL' },
  { id: 'RM-CHK-045', name: 'Unauthenticated API Endpoint', cat: 'API Security', sev: 'HIGH' },
  { id: 'RM-CHK-046', name: 'API Rate Limiting Missing', cat: 'API Security', sev: 'MEDIUM' },
  { id: 'RM-CHK-047', name: 'GraphQL Introspection Enabled', cat: 'API Security', sev: 'MEDIUM' },
  { id: 'RM-CHK-048', name: 'REST API Enumeration', cat: 'API Security', sev: 'LOW' },
  { id: 'RM-CHK-049', name: 'Mass Assignment Vulnerability', cat: 'API Security', sev: 'HIGH' },
  { id: 'RM-CHK-050', name: 'IDOR in API', cat: 'API Security', sev: 'HIGH' },
  { id: 'RM-CHK-051', name: 'WordPress Version Disclosure', cat: 'CMS/Framework', sev: 'LOW' },
  { id: 'RM-CHK-052', name: 'WordPress Outdated Plugins', cat: 'CMS/Framework', sev: 'HIGH' },
  { id: 'RM-CHK-053', name: 'Drupal Version Exposure', cat: 'CMS/Framework', sev: 'LOW' },
  { id: 'RM-CHK-054', name: 'Joomla Admin Panel Exposed', cat: 'CMS/Framework', sev: 'HIGH' },
  { id: 'RM-CHK-055', name: 'Laravel Debug Mode Active', cat: 'CMS/Framework', sev: 'CRITICAL' },
  { id: 'RM-CHK-056', name: 'Django Secret Key Exposed', cat: 'CMS/Framework', sev: 'CRITICAL' },
];

const CATS = ['Injection', 'Authentication', 'Headers', 'Info Disclosure', 'Network',
  'File Upload', 'API Security', 'CMS/Framework', 'Business Logic', 'Cryptography',
  'Access Control', 'DoS'];
const SEVS: AttackDef['sev'][] = ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO'];

function buildCatalog(): AttackDef[] {
  const known = new Set(NAMED.map((a) => a.id));
  const catalog = [...NAMED];
  for (let i = 1; i <= 179; i++) {
    const id = 'RM-CHK-' + String(i).padStart(3, '0');
    if (!known.has(id)) {
      catalog.push({ id, name: `Security Check #${i}`, cat: CATS[i % CATS.length], sev: SEVS[i % SEVS.length] });
    }
  }
  return catalog.sort((a, b) => a.id.localeCompare(b.id));
}

export const ATTACK_CATALOG: AttackDef[] = buildCatalog();
export const ALL_CATEGORIES = [...new Set(ATTACK_CATALOG.map((a) => a.cat))].sort();

export const MODULES_FULL = ATTACK_CATALOG.map((a) => a.id);
export const MODULES_QUICK = MODULES_FULL.slice(0, 20);
export const MODULES_WEB = MODULES_FULL.slice(0, 60);
export const MODULES_NETWORK = [
  'RM-CHK-009', 'RM-CHK-013', 'RM-CHK-014', 'RM-CHK-015', 'RM-CHK-016', 'RM-CHK-017',
  'RM-CHK-018', 'RM-CHK-019', 'RM-CHK-020', 'RM-CHK-036', 'RM-CHK-037', 'RM-CHK-038',
  'RM-CHK-039', 'RM-CHK-040',
];

export function getVulnName(id: string): string {
  return ATTACK_CATALOG.find((a) => a.id === id)?.name || id;
}
