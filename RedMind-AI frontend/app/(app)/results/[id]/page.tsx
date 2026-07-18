"use client";

import { useEffect, useState, useMemo } from "react";
import { useParams, useRouter } from "next/navigation";
import { useScanStore } from "@/store/scanStore";
import { ScanRecord, CheckResult, Severity } from "@/lib/types";
import { getVulnName } from "@/lib/catalog";
import SeverityBadge from "@/components/SeverityBadge";
import {
  ShieldAlert,
  Clock,
  Target,
  Layers,
  ChevronDown,
  ChevronRight,
  Download,
  ArrowLeft,
  AlertTriangle,
  Info,
  Globe,
  Key,
  Bug,
  Network,
  FileWarning,
  TerminalSquare,
  CheckCircle2,
} from "lucide-react";

// ─── Severity order & colours ────────────────────────────────────────────────
const SEV_ORDER: Severity[] = ["CRITICAL", "HIGH", "MEDIUM", "LOW", "INFO"];
const SEV_COLORS: Record<Severity, string> = {
  CRITICAL: "text-critical",
  HIGH: "text-high",
  MEDIUM: "text-medium",
  LOW: "text-low",
  INFO: "text-info",
};
const SEV_BG: Record<Severity, string> = {
  CRITICAL: "bg-critical/10 border-critical/30",
  HIGH: "bg-high/10 border-high/30",
  MEDIUM: "bg-medium/10 border-medium/30",
  LOW: "bg-low/10 border-low/30",
  INFO: "bg-info/10 border-info/30",
};
const SEV_BAR: Record<Severity, string> = {
  CRITICAL: "bg-critical",
  HIGH: "bg-high",
  MEDIUM: "bg-medium",
  LOW: "bg-low",
  INFO: "bg-info",
};

// ─── Risk gauge ───────────────────────────────────────────────────────────────
function RiskGauge({ score }: { score: number }) {
  const pct = Math.min(100, score);
  const color =
    score >= 75
      ? "#ff0033"
      : score >= 45
        ? "#ff6600"
        : score >= 20
          ? "#ffb700"
          : "#3ea6ff";
  const label =
    score >= 75
      ? "CRITICAL RISK"
      : score >= 45
        ? "HIGH RISK"
        : score >= 20
          ? "MEDIUM RISK"
          : "LOW RISK";
  const r = 52,
    cx = 64,
    cy = 64;
  const circ = 2 * Math.PI * r;
  const dash = (pct / 100) * circ;

  return (
    <div className="flex flex-col items-center gap-2">
      <svg width={128} height={128} className="rotate-[-90deg]">
        <circle
          cx={cx}
          cy={cy}
          r={r}
          fill="none"
          stroke="rgba(255,26,26,0.1)"
          strokeWidth={10}
        />
        <circle
          cx={cx}
          cy={cy}
          r={r}
          fill="none"
          stroke={color}
          strokeWidth={10}
          strokeDasharray={`${dash} ${circ - dash}`}
          strokeLinecap="round"
          style={{
            filter: `drop-shadow(0 0 6px ${color})`,
            transition: "stroke-dasharray 0.8s ease",
          }}
        />
      </svg>
      <div className="text-center -mt-2">
        <div className="font-display text-4xl font-bold" style={{ color }}>
          {score}
        </div>
        <div className="text-xs font-mono tracking-widest" style={{ color }}>
          {label}
        </div>
      </div>
    </div>
  );
}

// ─── Severity bar chart ───────────────────────────────────────────────────────
function SevBar({ counts }: { counts: Record<Severity, number> }) {
  const total = Object.values(counts).reduce((a, b) => a + b, 0);
  return (
    <div className="space-y-2 w-full">
      {SEV_ORDER.map((sev) => (
        <div key={sev} className="flex items-center gap-3">
          <span
            className={`w-16 text-right text-[11px] font-mono ${SEV_COLORS[sev]}`}
          >
            {sev}
          </span>
          <div className="flex-1 h-2 bg-panel-raised rounded-full overflow-hidden">
            <div
              className={`h-full rounded-full transition-all duration-700 ${SEV_BAR[sev]}`}
              style={{
                width: total ? `${(counts[sev] / total) * 100}%` : "0%",
                opacity: 0.85,
              }}
            />
          </div>
          <span className="w-5 text-xs font-mono text-text-muted text-right">
            {counts[sev]}
          </span>
        </div>
      ))}
    </div>
  );
}

// ─── Finding detail renderer ──────────────────────────────────────────────────
function FindingRow({
  finding,
  index,
}: {
  finding: Record<string, any>;
  index: number;
}) {
  const [aiFix, setAiFix] = useState("");
  const [loadingAI, setLoadingAI] = useState(false);

  async function generateAIFix() {
    setLoadingAI(true);

    try {
      const response = await fetch("http://localhost:8000/remediation", {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          vulnerability: {
            issue: finding.issue,

            severity: finding.severity || "UNKNOWN",

            evidence: finding.evidence,

            payload: finding.payload,

            target: finding.url,
          },
        }),
      });

      const data = await response.json();

      setAiFix(data.remediation);
    } catch (error) {
      setAiFix("Unable to generate AI remediation.");
    }

    setLoadingAI(false);
  }

  const entries = Object.entries(finding).filter(
    ([k]) => !["id", "ai_remediation"].includes(k),
  );

  return (
    <div className="border border-hairline rounded bg-void p-3 space-y-3 font-mono text-xs">
      <div className="text-text-muted">Finding #{index + 1}</div>

      {entries.map(([key, val]) => (
        <div key={key} className="flex gap-2 flex-wrap">
          <span className="text-text-muted shrink-0 capitalize">
            {key.replace(/_/g, " ")}:
          </span>

          <span className="text-text-primary break-all">
            {Array.isArray(val)
              ? val.join(", ")
              : typeof val === "object"
                ? JSON.stringify(val)
                : String(val)}
          </span>
        </div>
      ))}

      <button
        onClick={generateAIFix}
        disabled={loadingAI}
        className="
        mt-3
        border
        border-red-primary
        text-red-primary
        px-4
        py-2
        rounded
        font-mono
        text-xs
        hover:bg-red-primary/10
        transition
        "
      >
        {loadingAI ? "GENERATING AI FIX..." : "🤖 GENERATE AI REMEDIATION"}
      </button>

      {aiFix && (
        <div
          className="
        mt-4
        border
        border-red-primary/30
        bg-red-primary/5
        rounded
        p-4
        whitespace-pre-wrap
        text-text-primary
        "
        >
          <div
            className="
          text-red-primary
          font-bold
          mb-3
          "
          >
            REDMIND AI REMEDIATION
          </div>

          {aiFix}
        </div>
      )}
    </div>
  );
}

// ─── Module card ──────────────────────────────────────────────────────────────
function ModuleCard({
  moduleId,
  result,
  defaultOpen,
}: {
  moduleId: string;
  result: CheckResult;
  defaultOpen: boolean;
}) {
  const [open, setOpen] = useState(defaultOpen);
  const name = getVulnName(moduleId);
  const hitCount = result.findings?.length ?? 0;

  return (
    <div
      className={`border rounded-md overflow-hidden transition-all ${SEV_BG[result.severity]}`}
    >
      {/* Header */}
      <button
        onClick={() => setOpen((o) => !o)}
        className="w-full flex items-center gap-3 px-4 py-3 text-left hover:bg-white/5 transition-colors"
      >
        <span className="shrink-0">
          {open ? <ChevronDown size={14} /> : <ChevronRight size={14} />}
        </span>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span
              className={`font-mono text-xs ${SEV_COLORS[result.severity]}`}
            >
              {moduleId}
            </span>
            <span className="font-display font-semibold text-sm">{name}</span>
          </div>
        </div>
        <div className="flex items-center gap-3 shrink-0">
          {result.summary && (
            <span className="text-[10px] font-mono text-text-muted hidden sm:block">
              {result.summary.tested_requests} req ·{" "}
              {result.summary.positive_hits} hit
            </span>
          )}
          <SeverityBadge severity={result.severity} />
          <span
            className={`text-xs font-mono font-bold ${SEV_COLORS[result.severity]}`}
          >
            {hitCount} {hitCount === 1 ? "finding" : "findings"}
          </span>
        </div>
      </button>

      {/* Body */}
      {open && (
        <div className="px-4 pb-4 space-y-2 border-t border-hairline/50">
          {result.findings?.map((f, i) => (
            <FindingRow key={i} finding={f} index={i} />
          ))}
        </div>
      )}
    </div>
  );
}

// ─── Category group ───────────────────────────────────────────────────────────
function CategorySection({
  severity,
  modules,
}: {
  severity: Severity;
  modules: { moduleId: string; result: CheckResult }[];
}) {
  const [collapsed, setCollapsed] = useState(false);

  return (
    <section className="space-y-3">
      <button
        onClick={() => setCollapsed((c) => !c)}
        className="flex items-center gap-3 w-full"
      >
        <span
          className={`font-display text-lg font-bold ${SEV_COLORS[severity]}`}
        >
          {severity}
        </span>
        <span
          className={`text-xs font-mono px-2 py-0.5 rounded border ${SEV_BG[severity]} ${SEV_COLORS[severity]}`}
        >
          {modules.length} module{modules.length !== 1 ? "s" : ""}
        </span>
        <div className="flex-1 h-px bg-hairline" />
        {collapsed ? (
          <ChevronRight size={14} className="text-text-muted" />
        ) : (
          <ChevronDown size={14} className="text-text-muted" />
        )}
      </button>

      {!collapsed && (
        <div className="space-y-2">
          {modules.map(({ moduleId, result }, i) => (
            <ModuleCard
              key={moduleId}
              moduleId={moduleId}
              result={result}
              defaultOpen={severity === "CRITICAL" && i === 0}
            />
          ))}
        </div>
      )}
    </section>
  );
}

// ─── CVSS-style summary pills ─────────────────────────────────────────────────
const STAT_ICONS: Record<string, React.ReactNode> = {
  Target: <Target size={14} />,
  Duration: <Clock size={14} />,
  Profile: <Layers size={14} />,
  Findings: <Bug size={14} />,
};

// ─── Main page ────────────────────────────────────────────────────────────────
export default function ResultsPage() {
  const params = useParams();
  const router = useRouter();
  const { current, history, hydrate } = useScanStore();
  const [scan, setScan] = useState<ScanRecord | null>(null);
  const [activeFilter, setActiveFilter] = useState<Severity | "ALL">("ALL");

  // Hydrate on mount, then resolve the right scan
  useEffect(() => {
    hydrate();
  }, [hydrate]);

  useEffect(() => {
    if (!params?.id) return;
    const id = Array.isArray(params.id) ? params.id[0] : params.id;
    // Check current first, then history
    if (current?.id === id) {
      setScan(current);
      return;
    }
    const found = history.find((h) => h.id === id);
    if (found) setScan(found);
    else if (current) setScan(current); // fallback: show latest
  }, [params?.id, current, history]);

  const grouped = useMemo(() => {
    if (!scan) return {};
    const map: Record<Severity, { moduleId: string; result: CheckResult }[]> = {
      CRITICAL: [],
      HIGH: [],
      MEDIUM: [],
      LOW: [],
      INFO: [],
    };
    for (const r of scan.results) {
      map[r.result.severity]?.push(r);
    }
    return map;
  }, [scan]);

  const filteredSevs = useMemo(
    () =>
      SEV_ORDER.filter(
        (s) =>
          grouped[s]?.length > 0 &&
          (activeFilter === "ALL" || activeFilter === s),
      ),
    [grouped, activeFilter],
  );

  const totalFindings = useMemo(
    () =>
      scan?.results.reduce(
        (acc, r) => acc + (r.result.findings?.length ?? 0),
        0,
      ) ?? 0,
    [scan],
  );

  if (!scan) {
    return (
      <div className="flex flex-col items-center justify-center h-64 gap-4 text-text-muted font-mono">
        <AlertTriangle size={32} className="text-medium" />
        <p className="text-sm">No scan results found. Run a scan first.</p>
        <button
          onClick={() => router.push("/scan")}
          className="text-red-glow text-sm flex items-center gap-1 hover:underline"
        >
          <ArrowLeft size={14} /> Back to Scan
        </button>
      </div>
    );
  }

  const formattedDate = new Date(scan.date).toLocaleString("en-GB", {
    day: "2-digit",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });

  return (
    <div className="space-y-8 pb-16">
      {/* ── Back nav ── */}
      <button
        onClick={() => router.back()}
        className="flex items-center gap-1.5 text-sm font-mono text-text-muted hover:text-text-primary transition-colors"
      >
        <ArrowLeft size={14} /> BACK
      </button>

      {/* ── Page header ── */}
      <header className="space-y-1">
        <div className="flex items-center gap-2 text-xs font-mono text-text-muted">
          <span>SCAN ID</span>
          <span className="text-red-dim">{scan.id}</span>
          <span className="ml-2 px-1.5 py-0.5 rounded border border-hairline text-[10px] uppercase">
            {scan.status}
          </span>
        </div>
        <h1 className="font-display text-3xl font-bold tracking-wide text-glow text-red-glow">
          ASSESSMENT RESULTS
        </h1>
        <p className="font-mono text-sm text-text-muted">{scan.target}</p>
      </header>

      {/* ── Summary row ── */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          {
            label: "RISK SCORE",
            value: scan.riskScore,
            color:
              scan.riskScore >= 75
                ? "text-critical"
                : scan.riskScore >= 45
                  ? "text-high"
                  : "text-medium",
          },
          { label: "SEC SCORE", value: scan.secScore, color: "text-low" },
          {
            label: "TOTAL FINDINGS",
            value: totalFindings,
            color: "text-text-primary",
          },
          {
            label: "DURATION",
            value: scan.duration || "—",
            color: "text-text-muted",
          },
        ].map((s) => (
          <div
            key={s.label}
            className="bg-panel border border-hairline rounded-md p-5 flex flex-col gap-1"
          >
            <span className="text-[10px] font-mono text-text-muted tracking-widest">
              {s.label}
            </span>
            <span className={`text-3xl font-display font-bold ${s.color}`}>
              {s.value}
            </span>
          </div>
        ))}
      </div>

      {/* ── Two-column: gauge + sev breakdown + meta ── */}
      <div className="grid md:grid-cols-3 gap-4">
        {/* Risk gauge */}
        <div className="bg-panel border border-hairline rounded-md p-6 flex flex-col items-center justify-center gap-6">
          <div className="text-xs font-mono text-text-muted tracking-widest">
            OVERALL RISK
          </div>
          <RiskGauge score={scan.riskScore} />
        </div>

        {/* Severity breakdown */}
        <div className="bg-panel border border-hairline rounded-md p-6 space-y-4">
          <div className="text-xs font-mono text-text-muted tracking-widest">
            FINDINGS BY SEVERITY
          </div>
          <SevBar counts={scan.sevCounts} />
          <div className="grid grid-cols-5 gap-1 pt-2">
            {SEV_ORDER.map((s) => (
              <div key={s} className="text-center">
                <div
                  className={`text-xl font-display font-bold ${SEV_COLORS[s]}`}
                >
                  {scan.sevCounts[s]}
                </div>
                <div className="text-[9px] font-mono text-text-muted">
                  {s.slice(0, 4)}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Scan meta */}
        <div className="bg-panel border border-hairline rounded-md p-6 space-y-4">
          <div className="text-xs font-mono text-text-muted tracking-widest">
            SCAN DETAILS
          </div>
          <div className="space-y-3 font-mono text-sm">
            {[
              { icon: <Target size={13} />, label: "Target", val: scan.target },
              { icon: <Clock size={13} />, label: "Date", val: formattedDate },
              {
                icon: <Layers size={13} />,
                label: "Profile",
                val: scan.scanType.toUpperCase(),
              },
              {
                icon: <TerminalSquare size={13} />,
                label: "Checks run",
                val: `${scan.completed} / ${scan.total}`,
              },
              {
                icon: <Bug size={13} />,
                label: "Modules hit",
                val: scan.results.length,
              },
              {
                icon: <ShieldAlert size={13} />,
                label: "Risk score",
                val: scan.riskScore,
              },
            ].map(({ icon, label, val }) => (
              <div key={label} className="flex items-start gap-2">
                <span className="text-text-muted mt-0.5 shrink-0">{icon}</span>
                <span className="text-text-muted w-24 shrink-0">{label}</span>
                <span className="text-text-primary break-all">{val}</span>
              </div>
            ))}
          </div>
          {scan.notes && (
            <div className="border-t border-hairline pt-3 text-xs font-mono text-text-muted">
              <span className="text-text-muted">Notes: </span>
              {scan.notes}
            </div>
          )}
        </div>
      </div>

      {/* ── Findings section ── */}
      <div className="space-y-5">
        <div className="flex items-center justify-between flex-wrap gap-3">
          <h2 className="font-display text-xl font-bold">
            VULNERABILITY FINDINGS
          </h2>

          {/* Severity filter pills */}
          <div className="flex items-center gap-2 flex-wrap">
            {(["ALL", ...SEV_ORDER] as (Severity | "ALL")[]).map((sev) => (
              <button
                key={sev}
                onClick={() => setActiveFilter(sev)}
                className={`text-[11px] font-mono px-3 py-1 rounded border transition-all ${
                  activeFilter === sev
                    ? sev === "ALL"
                      ? "border-red-primary bg-red-primary/10 text-red-glow"
                      : `${SEV_BG[sev as Severity]} ${SEV_COLORS[sev as Severity]}`
                    : "border-hairline text-text-muted hover:border-red-dim"
                }`}
              >
                {sev}
                {sev !== "ALL" && scan.sevCounts[sev as Severity] > 0 && (
                  <span className="ml-1 opacity-70">
                    {scan.sevCounts[sev as Severity]}
                  </span>
                )}
              </button>
            ))}
          </div>
        </div>

        {scan.results.length === 0 ? (
          <div className="bg-panel border border-hairline rounded-md p-10 flex flex-col items-center gap-3 text-text-muted font-mono text-sm">
            <CheckCircle2 size={32} className="text-low" />
            No exploitable findings detected across {scan.completed} checks.
          </div>
        ) : (
          <div className="space-y-6">
            {filteredSevs.map((sev) => (
              <CategorySection
                key={sev}
                severity={sev}
                modules={grouped[sev]}
              />
            ))}
          </div>
        )}
      </div>

      {/* ── Executive summary strip ── */}
      <div className="bg-panel border border-hairline rounded-md p-6 space-y-4">
        <div className="flex items-center gap-2">
          <FileWarning size={16} className="text-red-glow" />
          <span className="text-xs font-mono text-text-muted tracking-widest uppercase">
            Executive Summary
          </span>
        </div>
        <p className="font-mono text-sm text-text-primary leading-relaxed">
          Automated assessment of{" "}
          <span className="text-red-glow">{scan.target}</span> completed{" "}
          {scan.duration ? `in ${scan.duration}` : ""} across{" "}
          <span className="text-text-primary">
            {scan.completed} security checks
          </span>
          .{" "}
          {scan.sevCounts.CRITICAL > 0 && (
            <span className="text-critical">
              {scan.sevCounts.CRITICAL} critical-severity vulnerabilities
              require immediate remediation.{" "}
            </span>
          )}
          {scan.sevCounts.HIGH > 0 && (
            <span className="text-high">
              {scan.sevCounts.HIGH} high-severity issues should be addressed
              within 72 hours.{" "}
            </span>
          )}
          {scan.sevCounts.MEDIUM > 0 && (
            <span className="text-medium">
              {scan.sevCounts.MEDIUM} medium-severity findings scheduled for
              next sprint.{" "}
            </span>
          )}
          Risk score of{" "}
          <span
            className={
              scan.riskScore >= 75
                ? "text-critical"
                : scan.riskScore >= 45
                  ? "text-high"
                  : "text-medium"
            }
          >
            {scan.riskScore}/100
          </span>{" "}
          indicates{" "}
          {scan.riskScore >= 75
            ? "critical exposure requiring immediate incident response."
            : scan.riskScore >= 45
              ? "significant attack surface requiring urgent attention."
              : "moderate risk manageable through standard patching cycles."}{" "}
          Full technical details and reproduction steps are documented per
          finding above.
        </p>
        <div className="flex items-center justify-between pt-2 border-t border-hairline">
          <span className="text-xs font-mono text-text-muted">
            Generated by RedMind-AI VAPT Engine · {formattedDate}
          </span>
          <button
            onClick={() => window.print()}
            className="flex items-center gap-2 text-xs font-mono text-text-muted hover:text-text-primary border border-hairline hover:border-red-dim px-4 py-2 rounded transition-all"
          >
            <Download size={13} /> EXPORT REPORT
          </button>
        </div>
      </div>
    </div>
  );
}
