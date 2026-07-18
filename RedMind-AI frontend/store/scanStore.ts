import { create } from "zustand";
import { ScanRecord, ScanType, SevCounts } from "@/lib/types";

const HISTORY_KEY = "rm_scan_history";
const LAST_KEY = "rm_last_results";

function loadHistory(): ScanRecord[] {
  if (typeof window === "undefined") return [];

  try {
    return JSON.parse(localStorage.getItem(HISTORY_KEY) || "[]");
  } catch {
    return [];
  }
}

function loadLast(): ScanRecord | null {
  if (typeof window === "undefined") return null;

  try {
    return JSON.parse(localStorage.getItem(LAST_KEY) || "null");
  } catch {
    return null;
  }
}

function computeRiskScore(c: SevCounts): number {
  return Math.min(
    100,
    c.CRITICAL * 25 + c.HIGH * 12 + c.MEDIUM * 6 + c.LOW * 2 + c.INFO * 0.5,
  );
}

interface ScanStore {
  current: ScanRecord | null;

  history: ScanRecord[];

  aborted: boolean;

  logs: string[];

  startScan: (
    target: string,
    modules: string[],
    scanType: ScanType,
    notes?: string,
  ) => Promise<void>;

  abortScan: () => void;

  clearHistory: () => void;

  hydrate: () => void;
}

export const useScanStore = create<ScanStore>((set, get) => ({
  current: null,

  history: [],

  aborted: false,

  logs: [],

  hydrate: () => {
    set({
      history: loadHistory(),

      current: loadLast(),
    });
  },

  abortScan: () => {
    set({
      aborted: true,
    });
  },

  clearHistory: () => {
    localStorage.removeItem(HISTORY_KEY);

    set({
      history: [],
    });
  },

  startScan: async (target, modules, scanType, notes = "") => {
    const id = crypto.randomUUID();

    const startTime = Date.now();

    const initial: ScanRecord = {
      id,

      target,

      scanType,

      date: new Date().toISOString(),

      status: "running",

      results: [],

      completed: 0,

      total: modules.length,

      sevCounts: {
        CRITICAL: 0,

        HIGH: 0,

        MEDIUM: 0,

        LOW: 0,

        INFO: 0,
      },

      riskScore: 0,

      secScore: 100,

      duration: "",

      notes,
    };

    set({
      current: initial,

      aborted: false,

      logs: [`▶ Target: ${target}`, `▶ Profile: ${scanType}`],
    });

    const ws = new WebSocket(
      process.env.NEXT_PUBLIC_WS_URL || "ws://localhost:8000/ws",
    );

    ws.onopen = () => {
      ws.send(
        JSON.stringify({
          target,

          modules,

          scanType,

          notes,
        }),
      );
    };

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);

      // Progress update

      if (data.type === "progress") {
        set((state) => {
          if (!state.current) return state;

          return {
            current: {
              ...state.current,

              completed: Math.floor((data.value / 100) * state.current.total),
            },

            logs: [...state.logs, data.message || ""],
          };
        });
      }

      // Console logs

      if (data.type === "log") {
        set((state) => ({
          logs: [...state.logs, data.message],
        }));
      }

      // Final result

      if (data.type === "result") {
        const result = data.data;

        set((state) => {
          if (!state.current) return state;

          const findings: any[] = [];

          const sevCounts: SevCounts = {
            ...state.current.sevCounts,
          };

          if (result.results) {
            result.results.forEach((r: any) => {
              const output = r.output;

              if (
                output &&
                Array.isArray(output.findings) &&
                output.findings.length > 0
              ) {
                findings.push({
                  moduleId: output.check_id || r.id || "unknown",

                  result: {
                    ...output,

                    summary: output.summary || {},

                    findings: output.findings.map((f: any) => ({
                      issue: f.issue || "Unknown issue",

                      parameter: f.parameter || "",

                      payload: f.payload || "",

                      url: f.url || "",

                      evidence: f.evidence || "",

                      confidence: f.confidence || "N/A",

                      description: f.description || "",

                      remediation: f.remediation || "",

                      references: f.references || [],
                    })),
                  },
                });

                const sev = String(
                  output.severity || "INFO",
                ).toUpperCase() as keyof SevCounts;

                if (sevCounts[sev] !== undefined) {
                  sevCounts[sev] += 1;
                }
              }
            });
          }

          const riskScore = computeRiskScore(sevCounts);

          const durationSec = Math.round((Date.now() - startTime) / 1000);

          const finished: ScanRecord = {
            ...state.current,

            status: "complete",

            completed: state.current.total,

            results: findings,

            sevCounts,

            riskScore,

            secScore: Math.max(
              0,

              100 - riskScore,
            ),

            duration: `${Math.floor(durationSec / 60)}m ${durationSec % 60}s`,
          };

          const history = [finished, ...state.history].slice(0, 50);

          localStorage.setItem(
            LAST_KEY,

            JSON.stringify(finished),
          );

          localStorage.setItem(
            HISTORY_KEY,

            JSON.stringify(history),
          );

          return {
            current: finished,

            history,

            logs: [
              ...state.logs,

              `✅ Scan completed — ${findings.length} findings`,
            ],
          };
        });
      }

      // Backend error

      if (data.type === "error") {
        set((state) => ({
          logs: [...state.logs, `❌ ${data.message}`],
        }));
      }
    };

    ws.onerror = () => {
      set((state) => ({
        logs: [...state.logs, "❌ WebSocket connection failed"],
      }));
    };

    ws.onclose = () => {
      set((state) => ({
        logs: [...state.logs, "🔌 Connection closed"],
      }));
    };
  },
}));
